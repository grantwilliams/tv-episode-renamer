import pytest
import rename_episodes

#  directory, current_file_name, current_show, episodes_info, show_name_nums, expected result
preview_file_changes_args = [
    ['/media/vikings/season 01', 'Vikings.S01e09.720p.BluRay.x265.mkv', 'Vikings',
     [{'airedSeason': 1, 'airedEpisodeNumber': 9, 'episodeName': 'All Change'}], [],
     {'old': '/media/vikings/season 01/Vikings.S01e09.720p.BluRay.x265.mkv',
      'new': '/media/vikings/season 01/Vikings S01E09 - All Change.mkv'}],
    ["/media/That '70s Show/season 01", "8x22 - That '70s Finale.avi", "That '70s Show",
     [{'airedSeason': 8, 'airedEpisodeNumber': 22, 'episodeName': "That '70s Finale"}], ['70'],
     {'old': "/media/That '70s Show/season 01/8x22 - That '70s Finale.avi",
      'new': "/media/That '70s Show/season 01/That '70s Show S08E22 - That '70s Finale.avi"}],
    ['/media/The Office (US)/Season 07', 'The.Office.s07e11e12.avi', 'The Office',
     [{'airedSeason': 7, 'airedEpisodeNumber': 11, 'episodeName': 'Classy Christmas (1)'},
      {'airedSeason': 7, 'airedEpisodeNumber': 12, 'episodeName': 'Classy Christmas (2)'}], [],
     {'old': '/media/The Office (US)/Season 07/The.Office.s07e11e12.avi',
      'new': '/media/The Office (US)/Season 07/The Office S07E11E12 - Classy Christmas (1), Classy Christmas (2).avi'}]
]

@pytest.fixture(params=preview_file_changes_args)
def params_preview_file_changes(request):
    return request.param

def test_preview_file_changes(params_preview_file_changes):
    assert(rename_episodes.preview_file_changes(params_preview_file_changes[0],
                                                params_preview_file_changes[1],
                                                params_preview_file_changes[2],
                                                params_preview_file_changes[3],
                                                params_preview_file_changes[4])
           == params_preview_file_changes[5])
