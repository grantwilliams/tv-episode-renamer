#!/usr/bin/env python3
import os
import re
import fetch_episode_names
from regex_patterns import PATTERNS


def get_episode(episode_name, non_episode_numbers):
    """
    Extract season and episode number from episode name
    :param str episode_name: name of the original file
    :param list non_episode_numbers: list of numbers in the show's name
    :rtype: list
    """

    ep_name_reduced = episode_name
    #  Removes numbers from the shows title, to not interfere with the regex search
    for num in non_episode_numbers:
        ep_name_reduced = re.sub(r'{}'.format(num), '', ep_name_reduced, 1)

    for item in ['x264', 'x265', '720p', '1080p']:
        ep_name_reduced = re.sub(r'{}'.format(item), '', ep_name_reduced)

    #  Assumes the first number is the season/episode number
    nums_in_episode_name = re.findall(r'\d+', ep_name_reduced)
    try:
        season_digit_length = 1 if len(nums_in_episode_name[0]) == 3 else 2
    except IndexError:
        print("Could not find a season and episode number in file name '{}'".format(episode_name))
        exit()

    matches = [re.search(regex.format(season_digit_length), ep_name_reduced) for regex in PATTERNS]
    best_match = max([match.groups() for match in matches if match is not None])

    if best_match:
        best_match = [num for num in best_match if len(num) <= 2]  # removes 3 or more digit nums
        zero_padded_season_episode = ['0' + x if len(x) < 2 else x for x in best_match]
        return zero_padded_season_episode

def format_season_episode(season_episode_numbers):
    """
    Takes list of season and episode numbers to create a string for placing in the file name
    :param list season_episode_numbers: list of numbers, season and episode
    :rtype str: eg. S02E03, S02E03E04
    """

    if len(season_episode_numbers) == 2:
        return 'S{}E{}'.format(season_episode_numbers[0], season_episode_numbers[1])

    list_as_ints = [int(x) for x in season_episode_numbers[1:]]

    # Check #1 if list is comprised of all episode numbers or mixture of season and episode numbers
    all_are_episodes = False
    if list_as_ints == sorted(list_as_ints):
        all_are_episodes = True

    return_string = 'S{}'.format(season_episode_numbers[0])
    if len(season_episode_numbers) % 2 == 0:
        if all_are_episodes and len(list_as_ints) == len(set(list_as_ints)):  # Check #2
            for num in season_episode_numbers[1:]:
                return_string += 'E{}'.format(num)
        elif all([x for x in season_episode_numbers[0::2]]):
            for num in season_episode_numbers[1::2]:
                return_string += 'E{}'.format(num)
    else:
        for num in season_episode_numbers[1:]:
            return_string += 'E{}'.format(num)
    return return_string

def preview_file_changes(directory, current_file_name, current_show, episodes_info, show_name_nums):
    """
    Present the proposed changes to the file names for the user to confirm
    :param str directory: the parent directory, from where the script was called
    :param str current_file_name: original file name
    :param str current_show: TV show being changed, taken from user input
    :param dict episodes_info: info for every episode of the show, api response from thetvdb.com
    :param list show_name_nums: list of numbers in the show's name
    :rtype: dict
    """
    illegal_characters = '/\\?*:|"<>'
    season_episode = get_episode(os.path.splitext(current_file_name)[0], show_name_nums)

    episode_name = ""
    for episode in episodes_info:
        if episode['airedSeason'] == int(season_episode[0]) and \
        episode['airedEpisodeNumber'] == int(season_episode[1]):
            episode_name = re.sub(r'[{}]'.format(illegal_characters), '', episode['episodeName'])
    file_ext = os.path.splitext(current_file_name)[1]

    new_file_name = '{} {} - {}{}'.format(current_show, format_season_episode(season_episode),
                                          episode_name, file_ext)

    if new_file_name != current_file_name:
        print('Renaming: {} to:'.format(current_file_name))
        print(new_file_name)
        print()
        return {
            'old': '{}/{}'.format(directory, current_file_name),
            'new': '{}/{} S{}E{} - {}{}'.format(directory, current_show, season_episode[0],
                                                season_episode[1], episode_name, file_ext)
        }

def main():
    current_dir = input("In which directory would you like to rename files? "+
                        "(Drag directory into Terminal window): ").strip()
    current_show = input("\nName of the show? (Will be used for naming the files, so please write "+
                         "it how you would like it to appear in the file name): ")
    show_name_nums = re.findall(r'\d+', current_show)

    if current_dir[0] in ["'", '"'] and current_dir[-1] in ["'", '"']:
        current_dir = current_dir[1:-1]  # removes leading and trailing single or double quotes

    episodes_info = fetch_episode_names.start_search(current_show)
    folder_items = os.listdir(current_dir)

    proposed_changes = []
    for item in folder_items:
        renamed_file = None
        if item == 'Extras':
            pass # leave this folder alone
        elif os.path.isdir('{}/{}'.format(current_dir, item)):
            os.chdir('{}/{}'.format(current_dir, item))
            new_dir = os.getcwd()
            files = os.listdir(new_dir)
            for file in files:
                if file != 'Extras':
                    renamed_file = preview_file_changes(new_dir, file, current_show, episodes_info,
                                                        show_name_nums)
                    if renamed_file is not None:
                        proposed_changes.append(renamed_file)
        else:
            renamed_file = preview_file_changes(current_dir, item, current_show, episodes_info,
                                                show_name_nums)
            if renamed_file is not None:
                proposed_changes.append(renamed_file)

    print('Files to be renamed: {}'.format(len(proposed_changes)))
    if len(proposed_changes) > 0:
        confirm = input("Please take a look at the proposed file name changes, once confirmed, "+
                        "they can not be changed back. Confirm all changes: y/n? ").lower()
        while True:
            if confirm in ['y', 'yes']:
                for file in proposed_changes:
                    os.rename(file['old'], file['new'])
                print("\nAll files successfully renamed!\n")
                break
            elif confirm in ['n', 'no']:
                print('\nNo files were changed\n')
                break
            else:
                confirm = input('Sorry, could not understand, please choose y or n: ')
    else:
        print('No changes made')

if __name__ == '__main__':
    main()
