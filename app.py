from flask import Flask, request, render_template, redirect, url_for
import boto3

app = Flask(__name__)

# S3 configuration
S3_BUCKET = 'upload-image-s3-midterm'


s3 = boto3.client('s3')

dynamodb = boto3.client('dynamodb')

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    if 'Mozilla' in user_agent:  # Check if 'Mozilla' is present in the User-Agent header
        return render_template('index.html')
    else:
        return 'Hello, terminal user!'

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
