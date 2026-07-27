import pytest

pytest.importorskip("boto3")
import importlib
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

import sagittarius_engine.infrastructure.storage.s3_file_storage as s3_module
from sagittarius_engine.infrastructure.storage.s3_file_storage import S3FileStorage


class TestS3FileStorage:
    def test_s3_file_storage__read__success(self):
        with patch("boto3.client") as mock_boto3_client:
            mock_client = mock_boto3_client.return_value
            mock_client.get_object.return_value = {
                "Body": MagicMock(read=MagicMock(return_value=b"test data"))
            }

            storage = S3FileStorage(bucket_name="my-bucket")
            data = storage.read("path/to/file.txt")

            assert data == b"test data"
            mock_client.get_object.assert_called_once_with(
                Bucket="my-bucket", Key="path/to/file.txt"
            )

    def test_s3_file_storage__write_bytes__success(self):
        with patch("boto3.client") as mock_boto3_client:
            mock_client = mock_boto3_client.return_value
            storage = S3FileStorage(bucket_name="my-bucket")

            storage.write("path/to/file.txt", b"test data")

            mock_client.put_object.assert_called_once_with(
                Bucket="my-bucket", Key="path/to/file.txt", Body=b"test data"
            )

    def test_s3_file_storage__write_str__success(self):
        with patch("boto3.client") as mock_boto3_client:
            mock_client = mock_boto3_client.return_value
            storage = S3FileStorage(bucket_name="my-bucket")

            storage.write("path/to/file.txt", "test data")

            mock_client.put_object.assert_called_once_with(
                Bucket="my-bucket", Key="path/to/file.txt", Body=b"test data"
            )

    def test_s3_file_storage__delete__success(self):
        with patch("boto3.client") as mock_boto3_client:
            mock_client = mock_boto3_client.return_value
            storage = S3FileStorage(bucket_name="my-bucket")

            storage.delete("path/to/file.txt")

            mock_client.delete_object.assert_called_once_with(
                Bucket="my-bucket", Key="path/to/file.txt"
            )

    def test_s3_file_storage__exists__true(self):
        with patch("boto3.client") as mock_boto3_client:
            mock_client = mock_boto3_client.return_value
            mock_client.head_object.return_value = {}

            storage = S3FileStorage(bucket_name="my-bucket")
            exists = storage.exists("path/to/file.txt")

            assert exists is True
            mock_client.head_object.assert_called_once_with(
                Bucket="my-bucket", Key="path/to/file.txt"
            )

    def test_s3_file_storage__exists__false(self):
        with patch("boto3.client") as mock_boto3_client:
            mock_client = mock_boto3_client.return_value
            mock_client.head_object.side_effect = ClientError(
                {"Error": {"Code": "404"}}, "head_object"
            )

            storage = S3FileStorage(bucket_name="my-bucket")
            exists = storage.exists("path/to/file.txt")

            assert exists is False
            mock_client.head_object.assert_called_once_with(
                Bucket="my-bucket", Key="path/to/file.txt"
            )

    def test_s3_file_storage__exists__raises_other_error(self):
        with patch("boto3.client") as mock_boto3_client:
            mock_client = mock_boto3_client.return_value
            mock_client.head_object.side_effect = ClientError(
                {"Error": {"Code": "500"}}, "head_object"
            )

            storage = S3FileStorage(bucket_name="my-bucket")

            with pytest.raises(ClientError):
                storage.exists("path/to/file.txt")

            mock_client.head_object.assert_called_once_with(
                Bucket="my-bucket", Key="path/to/file.txt"
            )

    def test_s3_file_storage__init__missing_boto3(self):
        try:
            with patch.dict("sys.modules", {"boto3": None}):
                importlib.reload(s3_module)
                with pytest.raises(ImportError, match="boto3 is not installed"):
                    s3_module.S3FileStorage(bucket_name="my-bucket")
        finally:
            importlib.reload(s3_module)
