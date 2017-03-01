#!/usr/bin/env python3
import os
import re
import fetch_episode_names


def get_episode(episode_name, non_episode_numbers):
    episode_name = episode_name.replace('.', 'x')

    #  Removes numbers from the shows title, to not interfere with the regex search
    for num in non_episode_numbers:
        episode_name = re.sub(r'{}'.format(num), '', episode_name, 1)

    #  Assumes the first number is the season/episode number, won't work if a differnt number
    #  comes first ie. 1080p, 720p etc
    nums_in_episode_name = re.findall(r'\d+', episode_name)
    if len(nums_in_episode_name[0]) == 3:
        season_digit_length = 1
        episode_digit_length = 2
    else:
        season_digit_length = 2
        episode_digit_length = 2
    match = re.search(
        r'''
        (?ix)                   # Ignore case (i), and use verbose regex (x)
        (?:s|season)?
        (\d{{1,{0}}})           # Season number (Captured)
        \s*                     # 0-or-more whitespaces
        (?:                     # Non-grouping pattern
          \.|e|x|episode|^      # e or x or episode or start of a line
          )?                    # End non-grouping pattern
        \s*                     # 0-or-more whitespaces
        (\d{{1,{1}}})           # Episode number (Captured)
        '''.format(season_digit_length, episode_digit_length), episode_name, re.I)
    if match:
        zero_padded_season_episode = ['0' + x if len(x) < 2 else x for x in match.groups()]
        return zero_padded_season_episode

def preview_file_changes(directory, current_file_name, current_show, episodes_info, show_name_nums):
    illegal_characters = '/\\?*:|"<>'
    season_episode = get_episode(os.path.splitext(current_file_name)[0], show_name_nums)
    episode_name = ""
    for episode in episodes_info:
        if episode['airedSeason'] == int(season_episode[0]) and \
        episode['airedEpisodeNumber'] == int(season_episode[1]):
            episode_name = re.sub(r'[{}]'.format(illegal_characters), '', episode['episodeName'])
    file_ext = os.path.splitext(current_file_name)[1]

    new_file_name = '{} S{}E{} - {}{}'.format(current_show, season_episode[0], season_episode[1],
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
    current_dir = input("In which directory would you like to rename files? (Drag directory \
into Terminal window): ").strip()[1:-1]  # removes leading and trailing single or double quotes
    current_show = input("\nName of the show? (Will be used for naming the files, so please write \
it how you would like it to appear in the file name): ")
    show_name_nums = re.findall(r'\d+', current_show)

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
        confirm = input("Please take a look at the proposed file name changes, once confirmed, \
they can not be changed back. Confirm all changes: y/n? ").lower()
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
