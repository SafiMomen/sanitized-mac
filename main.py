from pathlib import Path;
from sub_directories import *;
from weak_file_detection import *;
from weak_watchdog import *;
import shutil;

observing_path_folder = Path("./test_downloads")
folder_items = list(observing_path_folder.iterdir())

# %unsorted: doesn't attempt sort on files, used for user convenience.
# %sort: putting files in this folder causes item to auto sort
# %unknwon: the file type couldn't be determined. 
sub_directories = ["%sort", "%unknown", "%unsorted"]
#TODO: add custom file type implementation
for file_type, suffixes in SUPPORTED_SUFFIXES.items():
    sub_directories.append(("%" + file_type));

sub_directory_handler = SubDirectoriesHandler(
    observing_path_folder,
    sub_directories
);

def file_ready_for_processing(item_file: Path) -> None:
    print("[debug]::attempting file allocation.");
    file_type = get_file_type(item_file);
    destination = sub_directory_handler.get_sub_directory(("%" + file_type))
    shutil.move(item_file, destination);
    
directory_watchdog = DirectoryWatchdog(
    "%sort", 
    sub_directory_handler,
    file_processed=file_ready_for_processing
);
directory_watchdog.start_polling();
