#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
import argparse
import shutil
from subtitle_exts import SUBTITLE_EXTS

def preview_file_moves(current_dir, new_directory, take_subtitles):
    new_dir_list = os.listdir(new_directory)
    largest_file = ""  # The largest file will be the video file that needs to be moved
    largest_file_size = 0
    subtitle_file = None
    for file in new_dir_list:
        if os.path.getsize(file) > largest_file_size:
            largest_file = file
            largest_file_size = os.path.getsize(file)
        if os.path.splitext(file)[1] in SUBTITLE_EXTS:
            subtitle_file = file
    old_path = os.path.join(new_directory, largest_file)
    new_path = os.path.join(current_dir, largest_file)
    print('{} --> '.format(old_path), '{}\n'.format(new_path))
    change_dict = {'old': old_path,
                   'new': new_path}

    if subtitle_file and take_subtitles:
        old_subtitle_path = os.path.join(new_directory, subtitle_file)
        new_subtitle_path = os.path.join(current_dir, subtitle_file)
        print('{} --> '.format(old_subtitle_path), '{}\n'.format(new_subtitle_path))
        change_dict.update({'sub_old': old_subtitle_path,
                            'sub_new': new_subtitle_path})
    return change_dict

def confirm_file_moves(file_names, dirs_to_delete):
    for file_name in file_names:
        os.rename(file_name['old'], file_name['new'])
        if file_name.get('sub_new', False):
            os.rename(file_name['sub_old'], file_name['sub_new'])

    for directory in dirs_to_delete:
        print('{} deleted'.format(directory))
        shutil.rmtree(directory, ignore_errors=True)

    print("\nAll files successfully moved!\n")

def main(**kwargs):
    current_dir = os.path.abspath(os.getcwd())
    print('Current Working Directory: {}'.format(current_dir))

    folders = os.listdir(current_dir)

    dirs_to_delete = []
    proposed_moves = []
    for folder in folders:
        folder_path = os.path.join(current_dir, folder)
        if os.path.isdir(folder_path):
            dirs_to_delete.append(folder_path)
            os.chdir(folder_path)
            new_dir = os.getcwd()
            proposed_moves.append(preview_file_moves(current_dir, new_dir, kwargs['take_subtitles']))

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
    p = argparse.ArgumentParser()
    p.add_argument('-s', '--take-subtitles', help='BOOLEAN')
    args = p.parse_args()
    main(**vars(args))
