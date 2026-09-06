from pathlib import Path;
from sub_directories import SubDirectoriesHandler

observing_path_folder = Path("./test_downloads")
folder_items = list(observing_path_folder.iterdir())

sub_directories = ["%sort", "%unknown", "%images", "%documents", "%unsorted"]
sub_directory_handler = SubDirectoriesHandler(
    observing_path_folder,
    sub_directories
)
