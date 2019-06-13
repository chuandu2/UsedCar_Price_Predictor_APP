"""
Created on 5/12/19

@author: SophieDu

"""
import argparse
import boto3
s3 = boto3.client("s3")

def uploadData(args):
    """
	Upload data to aws S3 bucket
	Args:
            --input_file_path: local file path for uploaded file
            --bucket_name: s3 bucket name
            --output_file_path: output file path in S3 for uploaded file
	Return:
		None
		Data uploaded to S3 bucket
	"""
    s3.upload_file(args.input_file_path,args.bucket_name,args.output_file_path)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload data to S3")

    # add argument
    parser.add_argument("--input_file_path", help="local file path for uploaded file")
    parser.add_argument("--bucket_name", help="s3 bucket name")
    parser.add_argument("--output_file_path", help="output file path in S3 for uploaded file")

    args = parser.parse_args()
    uploadData(args)
