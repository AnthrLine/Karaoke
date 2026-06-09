import os

from classes.FileReader import FileReader
from typing import List, Tuple

from classes.lrcgetter import Lrcgetter
from classes.song import Song

def addLRC(song: Song):

    ULRC, SLRC = Lrcgetter.searchSong(song)

    if(SLRC != None):
        song.addSLRC(SLRC)
        print(f"[SUCCESS] Embedded synced lyrics into: {song.filename()} ({song.length()}s)")
    elif(ULRC != None):
        song.addULRC(ULRC)
        print(f"[SUCCESS] Embedded lyrics into: {song.filename()} ({song.length()}s)")

    else:
        print(f"[NO_LRC] No lyrics found for: {song.filename()} ({song.length()}s)")

def start() -> None:
    root_directory = "./debug"
    dir_stack: List[str] = [root_directory]

    print(f"Starting recursive scan from: {os.path.abspath(root_directory)}\n")

    while dir_stack:
        current_dir = dir_stack.pop()

        try:
            reader = FileReader(current_dir)
        except Exception as e:
            print(f"Skipping directory {current_dir} due to error: {e}")
            continue

        # Process all files found in the current directory level
        while not reader.isFilesEnd():
            file_path = reader.nextFile()
            _, ext = os.path.splitext(file_path)

            try:
                song = Song.from_file(file_path)

            except Exception as e:
                print(f"[ERROR] Failed to process song {file_path}: {e}")

            if not song.hasULRC() and not song.hasSLRC():
                addLRC(song)

        # Push discovered subdirectories onto our stack so they get processed recursively next
        while not reader.isDirectoriesEnd():
            sub_dir = reader.nextDirectory()
            dir_stack.append(sub_dir)

if __name__ == '__main__':
    start()