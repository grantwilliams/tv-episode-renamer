#!/usr/bin/env python
import os
import sys
import logging
import click
import move_episodes

home_path = 'HOMEPATH' if sys.platform == 'win32' else 'HOME'
log_directory = os.path.join(os.environ[home_path], '.tv-episode-renamer')
if not os.path.exists(log_directory):
    os.makedirs('{}/move_changes'.format(log_directory))

move_logger = logging.getLogger('File Move')
move_logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s: [%(levelname)s] %(message)s')
fh = logging.FileHandler('{}/file_move.log'.format(log_directory))
fh.setLevel(logging.WARNING)
fh.setFormatter(formatter)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
move_logger.addHandler(fh)
move_logger.addHandler(ch)

@click.command()
@click.option('-s', '--include-subtitles', is_flag=True, help='Also move the subtitle files found')
@click.option('--reverse-changes-file', type=click.Path(), help='Choose a file to reverse changes')
def _move_episodes(include_subtitles, reverse_changes_file):
    file_mover = move_episodes.FileMove(root_dir=os.path.abspath(os.getcwd()),
                                        logger=move_logger,
                                        log_directory=log_directory,
                                        include_subtitles=include_subtitles)
    if reverse_changes_file:
        file_mover.reverse_changes(reverse_changes_file)
        print('All changes from "{}" reversed'.format(reverse_changes_file))
        sys.exit()
    for file in file_mover.get_root_dir_contents():
        file_path = os.path.join(file_mover.get_root_dir(), file)
        if os.path.isdir(file_path):
            os.chdir(file_path)
            new_dir = os.getcwd()
            file_mover.preview_file_move(new_dir)
            file_mover.delete_dir(file_path)

    # Change back to parent dir, to avoid Permission Error when deleting sub dirs
    os.chdir(file_mover.get_root_dir())

    confirm = input("Please take a look at the proposed file moves, once confirmed, they can "
                    "not be moved back. Confirm all changes: y/n? ").lower()
    while True:
        if confirm in ['y', 'yes']:
            file_mover.confirm_file_moves()
            file_mover.save_file_changes()
            break
        elif confirm in ['n', 'no']:
            print('\nNo files were moved\n')
            break
        else:
            confirm = input('Sorry, could not understand, please choose y or n: ')

_move_episodes()
