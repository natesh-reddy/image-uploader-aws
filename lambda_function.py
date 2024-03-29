import json
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')
db = boto3.client('dynamodb', region_name = 'us-east-2')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    
    response = s3.get_object(Bucket=bucket, Key=key)
    print("CONTENT TYPE: " + response['ContentType'])
    # item = {'file_name': key, 'content_type': response['ContentType']}
    
    item = {
        'meta-data': {'S': str(key)},
        'content_type': {'S': str(response['ContentType'])},
        'date': {'S': str(response['LastModified'])},
        'size': {'N': str(response['ContentLength']/1024)}
    }
    response2 = db.put_item(TableName='store-image-data', Item=item)
    print("response2", response2)
    # print("response:", response['LastModified'], response['ContentLength'])
    return response['ContentType']

