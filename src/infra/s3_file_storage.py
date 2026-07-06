from src.interfaces import IFileStorage

try:
    import boto3
    from botocore.exceptions import ClientError

    BOTO3_INSTALLED = True
except ImportError:
    BOTO3_INSTALLED = False


class S3FileStorage(IFileStorage):
    """
    @brief File Storage implementation for AWS S3.

    @par Requirement:
    Requires the `boto3` package to be installed.
    """

    def __init__(self, bucket_name: str) -> None:
        """
        @brief Constructor.
        @param bucket_name The name of the S3 bucket.
        """
        if not BOTO3_INSTALLED:
            raise ImportError(
                "boto3 is not installed. Please install it using `pip install boto3`."
            )
        self.bucket_name = bucket_name
        self.s3_client = boto3.client("s3")

    def read(self, path: str) -> bytes:
        """@brief Reads a file from S3."""
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=path)
        return response["Body"].read()

    def write(self, path: str, data: bytes | str) -> None:
        """@brief Writes data to S3."""
        body = data.encode("utf-8") if isinstance(data, str) else data
        self.s3_client.put_object(Bucket=self.bucket_name, Key=path, Body=body)

    def delete(self, path: str) -> None:
        """@brief Deletes a file from S3."""
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=path)

    def exists(self, path: str) -> bool:
        """@brief Checks if a file exists in S3."""
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=path)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            raise
