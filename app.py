from flask import Flask, request, render_template, redirect, url_for, session
import boto3

app = Flask(__name__)

# S3 configuration
S3_BUCKET = 'upload-image-s3-midterm'

# AWS Cognito configuration
COGNITO_REGION = 'us-east-2'
COGNITO_USER_POOL_ID = 'us-east-2_vTK8m5hGU'
COGNITO_APP_CLIENT_ID = '94l5v01kqckjsueshr2kvd7di'

cognito_client = boto3.client('cognito-idp', region_name=COGNITO_REGION)

s3 = boto3.client('s3')

dynamodb = boto3.client('dynamodb', region_name = 'us-east-2')

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    if 'Mozilla' in user_agent:  # Check if 'Mozilla' is present in the User-Agent header
        return render_template('index.html')
    else:
        return 'Hello, terminal user!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Authenticate user with Cognito
        try:
            response = cognito_client.initiate_auth(
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password
                },
                ClientId=COGNITO_APP_CLIENT_ID
            )
            # session['access_token'] = response['AuthenticationResult']['AccessToken']
            return redirect(url_for('index'))  # Redirect to index page after successful login
        except Exception as e:
            error_message = str(e)
            return render_template('login.html', error_message=error_message)

    return render_template('login.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return 'No file part'
    
    file = request.files['image']
    
    if file.filename == '':
        return 'No selected file'

    # Upload image to S3
    try:
        s3.upload_fileobj(file, S3_BUCKET, file.filename)
        # return 'Image uploaded successfully'
        # return display_responses(file.filename)
        return redirect(url_for('display_responses', filename=file.filename))
    
    except Exception as e:
        return f'Error uploading image: {str(e)}'
    
@app.route('/display-responses/<filename>')
def display_responses(filename):
    response = dynamodb.get_item(
            TableName='store-image-data',
            Key={
                'meta-data': {'S': filename}
            }
        )
    
    item = response.get('Item')
    
    return render_template('display_responses.html', item=item)

if __name__ == '__main__':
    app.run(debug=True)
