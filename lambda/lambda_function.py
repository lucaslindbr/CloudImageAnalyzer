import json
import urllib.parse
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event, indent=2))

    try:
        # Get the object from the S3 trigger event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        
        # Get the object metadata to find size and type based on S3 event
        response = s3.head_object(Bucket=bucket, Key=key)
        
        content_type = response['ContentType']
        size_bytes = response['ContentLength']
        
        logger.info(f"--- IMAGE UPLOAD METADATA ---")
        logger.info(f"Bucket: {bucket}")
        logger.info(f"File Key: {key}")
        logger.info(f"Size (Bytes): {size_bytes}")
        logger.info(f"Type (ContentType): {content_type}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Successfully processed image',
                'file_name': key,
                'content_type': content_type,
                'size': size_bytes
            })
        }
    except Exception as e:
        logger.error(f"Error getting object {key} from bucket {bucket}. Exception: {str(e)}")
        raise e
