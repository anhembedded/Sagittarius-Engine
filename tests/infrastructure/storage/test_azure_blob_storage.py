import pytest

pytest.importorskip("azure")
import importlib
from unittest.mock import MagicMock, patch

from azure.core.exceptions import ResourceNotFoundError

import sagittarius_engine.infrastructure.storage.azure_blob_storage as azure_module
from sagittarius_engine.infrastructure.storage.azure_blob_storage import (
    AzureBlobStorage,
)


class TestAzureBlobStorage:
    def test_azure_blob_storage__read__success(self):
        with patch(
            "sagittarius_engine.infrastructure.storage.azure_blob_storage.BlobServiceClient"
        ) as mock_blob_service_client:
            mock_service_client = (
                mock_blob_service_client.from_connection_string.return_value
            )
            mock_container_client = (
                mock_service_client.get_container_client.return_value
            )
            mock_blob_client = mock_container_client.get_blob_client.return_value
            mock_blob_client.download_blob.return_value = MagicMock(
                readall=MagicMock(return_value=b"test data")
            )

            storage = AzureBlobStorage(
                connection_string="dummy_conn_str", container_name="my-container"
            )
            data = storage.read("path/to/file.txt")

            assert data == b"test data"
            mock_blob_service_client.from_connection_string.assert_called_once_with(
                "dummy_conn_str"
            )
            mock_service_client.get_container_client.assert_called_once_with(
                "my-container"
            )
            mock_container_client.get_blob_client.assert_called_once_with(
                "path/to/file.txt"
            )
            mock_blob_client.download_blob.assert_called_once()
            mock_blob_client.download_blob.return_value.readall.assert_called_once()

    def test_azure_blob_storage__write_bytes__success(self):
        with patch(
            "sagittarius_engine.infrastructure.storage.azure_blob_storage.BlobServiceClient"
        ) as mock_blob_service_client:
            mock_service_client = (
                mock_blob_service_client.from_connection_string.return_value
            )
            mock_container_client = (
                mock_service_client.get_container_client.return_value
            )
            mock_blob_client = mock_container_client.get_blob_client.return_value

            storage = AzureBlobStorage(
                connection_string="dummy_conn_str", container_name="my-container"
            )
            storage.write("path/to/file.txt", b"test data")

            mock_container_client.get_blob_client.assert_called_once_with(
                "path/to/file.txt"
            )
            mock_blob_client.upload_blob.assert_called_once_with(
                b"test data", overwrite=True
            )

    def test_azure_blob_storage__write_str__success(self):
        with patch(
            "sagittarius_engine.infrastructure.storage.azure_blob_storage.BlobServiceClient"
        ) as mock_blob_service_client:
            mock_service_client = (
                mock_blob_service_client.from_connection_string.return_value
            )
            mock_container_client = (
                mock_service_client.get_container_client.return_value
            )
            mock_blob_client = mock_container_client.get_blob_client.return_value

            storage = AzureBlobStorage(
                connection_string="dummy_conn_str", container_name="my-container"
            )
            storage.write("path/to/file.txt", "test data")

            mock_container_client.get_blob_client.assert_called_once_with(
                "path/to/file.txt"
            )
            mock_blob_client.upload_blob.assert_called_once_with(
                b"test data", overwrite=True
            )

    def test_azure_blob_storage__delete__success(self):
        with patch(
            "sagittarius_engine.infrastructure.storage.azure_blob_storage.BlobServiceClient"
        ) as mock_blob_service_client:
            mock_service_client = (
                mock_blob_service_client.from_connection_string.return_value
            )
            mock_container_client = (
                mock_service_client.get_container_client.return_value
            )
            mock_blob_client = mock_container_client.get_blob_client.return_value

            storage = AzureBlobStorage(
                connection_string="dummy_conn_str", container_name="my-container"
            )
            storage.delete("path/to/file.txt")

            mock_container_client.get_blob_client.assert_called_once_with(
                "path/to/file.txt"
            )
            mock_blob_client.delete_blob.assert_called_once()

    def test_azure_blob_storage__exists__true(self):
        with patch(
            "sagittarius_engine.infrastructure.storage.azure_blob_storage.BlobServiceClient"
        ) as mock_blob_service_client:
            mock_service_client = (
                mock_blob_service_client.from_connection_string.return_value
            )
            mock_container_client = (
                mock_service_client.get_container_client.return_value
            )
            mock_blob_client = mock_container_client.get_blob_client.return_value
            mock_blob_client.get_blob_properties.return_value = {}

            storage = AzureBlobStorage(
                connection_string="dummy_conn_str", container_name="my-container"
            )
            exists = storage.exists("path/to/file.txt")

            assert exists is True
            mock_container_client.get_blob_client.assert_called_once_with(
                "path/to/file.txt"
            )
            mock_blob_client.get_blob_properties.assert_called_once()

    def test_azure_blob_storage__exists__false(self):
        with patch(
            "sagittarius_engine.infrastructure.storage.azure_blob_storage.BlobServiceClient"
        ) as mock_blob_service_client:
            mock_service_client = (
                mock_blob_service_client.from_connection_string.return_value
            )
            mock_container_client = (
                mock_service_client.get_container_client.return_value
            )
            mock_blob_client = mock_container_client.get_blob_client.return_value
            mock_blob_client.get_blob_properties.side_effect = ResourceNotFoundError()

            storage = AzureBlobStorage(
                connection_string="dummy_conn_str", container_name="my-container"
            )
            exists = storage.exists("path/to/file.txt")

            assert exists is False
            mock_container_client.get_blob_client.assert_called_once_with(
                "path/to/file.txt"
            )
            mock_blob_client.get_blob_properties.assert_called_once()

    def test_azure_blob_storage__init__missing_azure_storage_blob(self):
        try:
            with patch.dict("sys.modules", {"azure.storage.blob": None}):
                importlib.reload(azure_module)
                with pytest.raises(
                    ImportError, match="azure-storage-blob is not installed"
                ):
                    azure_module.AzureBlobStorage(
                        connection_string="dummy", container_name="dummy"
                    )
        finally:
            importlib.reload(azure_module)
