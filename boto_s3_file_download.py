import boto3
from datetime import datetime

def download_s3_file(bucket_name, object_key, local_file):
    s3_client = boto3.client('s3')

    # Generate a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    downloaded_file = f"{local_file}_{timestamp}"

    try:
        s3_client.download_file(bucket_name, object_key, downloaded_file)
        print(f"File downloaded successfully: {downloaded_file}")
    except Exception as e:
        print(f"Error downloading file: {e}")

if __name__ == "__main__":
    bucket_name = "bytewiztestbucket"
    object_key = "folder1/customers.json"
    local_file = "downloaded_file"
    download_s3_file(bucket_name, object_key, local_file)