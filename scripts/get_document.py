
import boto3


def get_document(bucket, key):
    """
    get a document from S3. this is mainly for local testing,
    but might be useful for other purposes
    """

    session = boto3.Session()
    s3 = session.client('s3')
    s3_object = s3.get_object(Bucket=bucket, Key=key)
    body = s3_object['Body'].read()

    body = str(body)

    # could insert any standard cleaning/fixing stuff here
    # but might as well leave that for the processing function.....

    return body
