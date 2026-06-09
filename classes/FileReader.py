import os

class FileReader:

    # CONSTRUCTOR ######################################################################################################
    def __init__(self, path: str = '.') -> None:

        self._files = []
        self._directories = []

        self._filesI: int = 0
        self._directoriesI: int = 0

        list = os.scandir(path)

        with os.scandir(path) as entries:
            for entry in entries:  # Ignores symlinks automatically
                if entry.is_file():
                    self._files.append(entry.path)
                elif entry.is_dir():
                    self._directories.append(entry.path)


    def files(self):
        return self._files

    def directories(self):
        return self._directories

    def isDirectoriesEnd(self) -> bool:
        return self._directoriesI >= len(self._directories)

    def isFilesEnd(self) -> bool:
        return self._filesI >= len(self._files)

    def nextFile(self) -> str:
        res: str = self._files[self._filesI]
        self._filesI += 1
        return res

    def nextDirectory(self) -> str:
        res: str = self._directories[self._directoriesI]
        self._directoriesI += 1
        return res