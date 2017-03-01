import pytest
import rename_episodes

#  directory, current_file_name, current_show, episodes_info, show_name_nums, expected result
preview_file_changes_args = [
    ['/media/vikings/season 01', "Vikings.S01e09.720p.BluRay.x265.mkv", "Vikings",
     [{'airedSeason': 1, 'airedEpisodeNumber': 9, 'episodeName': 'All Change'}], [],
     {'old': '/media/vikings/season 01/Vikings.S01e09.720p.BluRay.x265.mkv',
      'new': '/media/vikings/season 01/Vikings S01E09 - All Change.mkv'}],
    ['/media/That 70s Show/season 01', "8x22 - That '70s Finale.avi", "That 70s Show",
     [{'airedSeason': 8, 'airedEpisodeNumber': 22, 'episodeName': "That '70s Finale"}], ['70'],
     {'old': "/media/That 70s Show/season 01/8x22 - That '70s Finale.avi",
      'new': "/media/That 70s Show/season 01/That 70s Show S08E22 - That '70s Finale.avi"}]
]

@pytest.fixture(params=preview_file_changes_args)
def params_preview_file_changes(request):
    print(request.param[3])
    return [request.param[0], request.param[1], request.param[2], request.param[3],
            request.param[4], request.param[5]]

def test_preview_file_changes(params_preview_file_changes):
    assert(rename_episodes.preview_file_changes(params_preview_file_changes[0],
                                                params_preview_file_changes[1],
                                                params_preview_file_changes[2],
                                                params_preview_file_changes[3],
                                                params_preview_file_changes[4])
           == params_preview_file_changes[5])
