import boto3

# List and process objects in an S3 bucket
def get_s3_objects(bucket_name, obj_prefix=None):
    s3_client = boto3.client("s3")
    # Use list_objects_v2 API to handle large number of objects
    paginator = s3_client.get_paginator("list_objects_v2") 
    operation_parameters = {"Bucket": bucket_name}

    # Add prefix to operation parameters if provided
    if obj_prefix:
        operation_parameters["Prefix"] = obj_prefix
    print(f"Operation Parameters: {operation_parameters}")

    # Iterate over the objects in the bucket
    for page in paginator.paginate(**operation_parameters):
        if "Contents" in page:
            # List object keys in the page
            for obj in page["Contents"]:
                object_keys = []
                for page in paginator.paginate(**operation_parameters):
                    if "Contents" in page:
                        for obj in page["Contents"]:
                            object_keys.append(obj['Key'])
                    else:
                        print(f"No objects with prefix '{obj_prefix}' found in the bucket '{bucket_name}'.")
                return object_keys
        else :
            print(f"No objects with prefix '{obj_prefix}' found in the bucket '{bucket_name}'.")

if __name__ == "__main__":
    bucket_name = "bytewiztestbucket"
    obj_prefix = "folder1/"
    result = get_s3_objects(bucket_name, obj_prefix)
    print(result)