from abc import ABC, abstractmethod


class IFileStorage(ABC):
    """
    @brief Interface for File Storage operations.

    @details Provides an abstraction over different storage mechanisms
    (e.g., Local File System, AWS S3, Azure Blob Storage).
    """

    @abstractmethod
    def read(self, path: str) -> bytes:
        """
        @brief Reads a file from storage.

        @param path The path or key of the file.
        @return The file content as bytes.
        """
        ...

    @abstractmethod
    def write(self, path: str, data: bytes | str) -> None:
        """
        @brief Writes data to a file in storage.

        @param path The path or key of the file.
        @param data The data to write.
        """
        ...

    @abstractmethod
    def delete(self, path: str) -> None:
        """
        @brief Deletes a file from storage.

        @param path The path or key of the file to delete.
        """
        ...

    @abstractmethod
    def exists(self, path: str) -> bool:
        """
        @brief Checks if a file exists in storage.

        @param path The path or key of the file.
        @return True if the file exists, False otherwise.
        """
        ...
