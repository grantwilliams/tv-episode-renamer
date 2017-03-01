#!/usr/bin/env python3

"""
This module is used to move video files from sub directories up into the parent directory.  Often
episodes will come in their own directory with a readme file and some preview images, this will
move the largest file (hopefully the video) and move it up one level and delete the unnecessary
folder and it's contents.
A preview of the changes will be printed to the terminal first, so you can make sure they are
correct before confirming, as it makes non reversable moves and deletes.
Assumes a file tree something like:

SeriesName(dir)
|
├──Season 01(dir)
|       ├──Episode 01(dir)
|       |       ├──Episode 01.avi
|       |       └──readme
|       └──Episode 02.mkv
|       └──Episode 03.mkv
|
└──Season 02(dir)
        ├──Episode 01(dir)
        |       ├──Episode 01.avi
        |       └──readme
        └──Episode 02.mkv

Note: it will only go one level deep, so it will need to be run in each 'season' directory
"""

import os
import shutil

def preview_file_moves(current_dir, new_directory):
    new_dir_list = os.listdir(new_directory)
    largest_file = ""  # The largest file will be the video file that needs to be moved
    largest_file_size = 0
    for file in new_dir_list:
        if os.path.getsize(file) > largest_file_size:
            largest_file = file
            largest_file_size = os.path.getsize(file)
    print('{}/{} -->  '.format(new_directory, largest_file),
          '{}/{}\n'.format(current_dir, largest_file))
    return {
        'old': '{}/{}'.format(new_directory, largest_file),
        'new': '{}/{}'.format(current_dir, largest_file)
    }

def confirm_file_moves(file_names, dirs_to_delete):
    for file_name in file_names:
        os.rename(file_name['old'], file_name['new'])

    for directory in dirs_to_delete:
        print('{} deleted'.format(directory))
        shutil.rmtree(directory, ignore_errors=True)

    print("\nAll files successfully moved!\n")

def main():
    current_dir = input("Which directory do you want to flatten? (Drag directory \
into Terminal window): ").strip()[1:-1]  # Removes leading and trailing single or double quotes

    folders = os.listdir(current_dir)
    dirs_to_delete = []

    proposed_moves = []
    for folder in folders:
        if os.path.isdir('{}/{}'.format(current_dir, folder)):
            dirs_to_delete.append('{}/{}'.format(current_dir, folder))
            os.chdir('{}/{}'.format(current_dir, folder))
            new_dir = os.getcwd()
            proposed_moves.append(preview_file_moves(current_dir, new_dir))

    # Change back to parent dir, to avoid Permission Error when deleting sub dirs
    os.chdir(current_dir)

    confirm = input("Please take a look at the proposed file moves, once confirmed, they can \
    not be moved back. Confirm all changes: y/n? ").lower()
    while True:
        if confirm in ['y', 'yes']:
            confirm_file_moves(proposed_moves, dirs_to_delete)
            break
        elif confirm in ['n', 'no']:
            print('\nNo files were moved\n')
            break
        else:
            confirm = input('Sorry, could not understand, please choose y or n: ')

if __name__ == '__main__':
    main()
