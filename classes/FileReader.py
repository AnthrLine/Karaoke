import os

class FileReader:

    # CONSTRUCTOR ######################################################################################################
    def __init__(self, path: str = '.') -> None:

        self._files = []
        self._directories = []

        self._filesI: int = 0
        self._directoriesI: int = 0

        list = os.scandir(path)

        for entry in list: # Ignores symlinks
            if entry.is_file():
                self._files.append(entry.name)
            elif entry.is_dir():
                self._directories.append(entry.name)

        list.close()


    def files(self):
        return self._files

    def directories(self):
        return self._directories

    def isDirectoriesEnd(self) -> bool:
        return len(self._directories) >= self._directoriesI

    def isFilesEnd(self) -> bool:
        return len(self._files) >= self._filesI

    def nextFile(self) -> str:
        res: str = self._files[self._filesI]
        self._filesI += 1
        return res

    def nextDirectory(self) -> str:
        res: str = self._directories[self._directoriesI]
        self._directoriesI += 1
        return res