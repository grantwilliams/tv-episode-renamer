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
from datetime import datetime
import json
import shutil
from subtitle_exts import SUBTITLE_EXTS


class FileMove(object):
    def __init__(self, root_dir, logger, log_directory, include_subtitles=False):
        self.__root_dir = root_dir
        self.__include_subtitles = include_subtitles
        self.__root_dir_contents = os.listdir(self.__root_dir)
        self.__dirs_to_delete = []
        self.__proposed_changes = []
        self.__logger = logger
        self.__log_directory = log_directory

    def get_root_dir(self):
        return self.__root_dir

    def get_root_dir_contents(self):
        return self.__root_dir_contents

    def dirs_to_delete(self):
        return self.__dirs_to_delete

    def proposed_changes(self):
        return self.__proposed_changes

    def delete_dir(self, directory):
        self.__dirs_to_delete.append(directory)

    def preview_file_move(self, new_directory):
        dir_list = os.listdir(new_directory)
        largest_file = ""  # The largest file will be the video file that needs to be moved
        largest_file_size = 0
        subtitle_file = None
        for file in dir_list:
            file_size = os.path.getsize(file)
            if file_size > largest_file_size:
                largest_file = file
                largest_file_size = file_size
            if os.path.splitext(file)[1] in SUBTITLE_EXTS:
                subtitle_file = file
        old_file_path = os.path.join(new_directory, largest_file)
        new_file_path = os.path.join(self.get_root_dir(), largest_file)

        self.__logger.info('Moving:\n{}\nto:\n{}\n'.format(old_file_path, new_file_path))

        change_dict = {'old_file': old_file_path, 'new_file': new_file_path}

        if subtitle_file and self.__include_subtitles:
            old_subtitle_path = os.path.join(new_directory, subtitle_file)
            new_subtitle_path = os.path.join(self.get_root_dir(), subtitle_file)
            self.__logger.info('Moving:\n{}\nto:\n{}\n'.format(old_subtitle_path, new_subtitle_path))
            change_dict.update({'old_sub': old_subtitle_path, 'new_sub': new_subtitle_path})
        self.__proposed_changes.append(change_dict)

    def confirm_file_moves(self):
        for change in self.__proposed_changes:
            os.rename(change['old_file'], change['new_file'])
            if change.get('new_sub', False):
                os.rename(change['old_sub'], change['new_sub'])

        for directory in self.__dirs_to_delete:
            shutil.rmtree(directory, ignore_errors=True)
            self.__logger.warning('{} deleted'.format(directory))

        self.__logger.info("\nAll files successfully moved!\n")

    def save_file_changes(self):
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('{}/move_changes/{} changes.json'.format(self.__log_directory, time_now), 'w', encoding='utf-8') as write_file:
            json.dump(obj=self.__proposed_changes, fp=write_file, indent=4)

    def reverse_changes(self, changes_file):
        with open(changes_file, 'r') as read_file:
            changes = json.load(read_file)
            for change in changes:
                if not os.path.isdir(os.path.dirname(change.get('old_file', 'old_sub'))):
                    os.mkdir(os.path.dirname(change.get('old_file', 'old_sub')))
                os.rename(change['new_file'], change['old_file'])
                if change.get('new_sub', False):
                    os.rename(change['new_sub'], change['old_sub'])
