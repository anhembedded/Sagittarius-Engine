from sagittarius_engine.infrastructure.ports.i_file_storage import IFileStorage

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.storage.blob import BlobServiceClient

    AZURE_INSTALLED = True
except ImportError:
    AZURE_INSTALLED = False


class AzureBlobStorage(IFileStorage):
    """
    @brief File Storage implementation for Azure Blob Storage.

    @par Requirement:
    Requires the `azure-storage-blob` package to be installed.
    """

    def __init__(self, connection_string: str, container_name: str) -> None:
        """
        @brief Constructor.
        @param connection_string The Azure Storage connection string.
        @param container_name The name of the Blob container.
        """
        if not AZURE_INSTALLED:
            raise ImportError(
                "azure-storage-blob is not installed. Please install it using `pip install azure-storage-blob`."
            )

        self.blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        self.container_client = self.blob_service_client.get_container_client(
            container_name
        )

    def read(self, path: str) -> bytes:
        """@brief Reads a blob from Azure Blob Storage."""
        blob_client = self.container_client.get_blob_client(path)
        return blob_client.download_blob().readall()

    def write(self, path: str, data: bytes | str) -> None:
        """@brief Writes data to Azure Blob Storage."""
        blob_client = self.container_client.get_blob_client(path)
        body = data.encode("utf-8") if isinstance(data, str) else data
        blob_client.upload_blob(body, overwrite=True)

    def delete(self, path: str) -> None:
        """@brief Deletes a blob from Azure Blob Storage."""
        blob_client = self.container_client.get_blob_client(path)
        blob_client.delete_blob()

    def exists(self, path: str) -> bool:
        """@brief Checks if a blob exists in Azure Blob Storage."""
        blob_client = self.container_client.get_blob_client(path)
        try:
            blob_client.get_blob_properties()
            return True
        except ResourceNotFoundError:
            return False
