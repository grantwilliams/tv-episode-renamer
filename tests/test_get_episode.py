import pytest
import rename_episodes


#  episode_name, non_episode_numbers, expected result
get_episode_file_name = [
    ["Vikings.S01e09.720p.BluRay.x265.mkv", [], ['01', '09']],
    ["Vikings.Season 01 Episode 02.720p.BluRay.x265.mkv", [], ['01', '02']],
    ["That 70s Show - 7x09 DVD.mkv", ['70'], ['07', '09']],
    ["That 70s Show - 702 Rip xxheyj.mkv", ['70'], ['07', '02']],
    ["8x22 - That '70s Finale.avi", ['70'], ['08', '22']],
    ["822 - That '70s Finale.avi", ['70'], ['08', '22']],
    ["The 4400 - 04x10 Blah Blah.mkv", ['4400'], ['04', '10']],
    ["21 Jump Steet - Episode 211 blah blah.mkv", ['21'], ['02', '11']],
    # ["Sample.Show S03E01E02E03 Sample.Episode.mkv", [], ['03', '01', '02', '03']],
    # ["Sample.Show 4x11 4x12 4x13 Sample.Episode.mkv", [], ['04', '11', '12', '13']]
]

@pytest.fixture(params=get_episode_file_name)
def get_episode_params(request):
    print([request.param[0], request.param[1], request.param[2]])
    return [request.param[0], request.param[1], request.param[2]]

def test_get_epipsode(get_episode_params):
    assert(rename_episodes.get_episode(get_episode_params[0],
                                       get_episode_params[1]) == get_episode_params[2])
