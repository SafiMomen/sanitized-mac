from pathlib import Path;

class SubDirectoriesHandler:
    def __init__(self, parent_folder: Path, directories: list[str]) -> None:
        self._parent_folder = parent_folder
        self._directories = directories
        for directory in self._directories:
            self.process_sub_directory(directory_name=directory)

    def get_sub_directory(self, directory_name: str) -> Path:
        return self._parent_folder / directory_name;

    def get_sub_directories(self) -> list[Path]:
        sub_directories: list[Path] = []
        for directory in self._directories:
            directory_path = self.get_sub_directory(directory)
            sub_directories.append(directory_path)
        return sub_directories        

    def process_sub_directory(self, directory_name: str) -> None:
        directory_path = self.get_sub_directory(directory_name)
        if (directory_path.exists()):
            return
        # doesn't exist, make it, it is save to retrieve later. 
        directory_path.mkdir(parents=True, exist_ok=True);