import pytest
import rename_episodes


#  episode_name, non_episode_numbers, expected result
get_episode_args = [
    ["Vikings.S01e09.720p.BluRay.x265.mkv", [], ['01', '09']],
    ["Vikings.Season 01 Episode 02.720p.BluRay.x265.mkv", [], ['01', '02']],
    ["That 70s Show - 7x09 720p DVD.mkv", ['70'], ['07', '09']],
    ["That 70s Show - 702 1080p Rip xxheyj.mkv", ['70'], ['07', '02']],
    ["8x22 - That '70s Finale.avi", ['70'], ['08', '22']],
    ["822 - That '70s Finale.avi", ['70'], ['08', '22']],
    ["The 4400 - 04x10 Blah Blah.mkv", ['4400'], ['04', '10']],
    ["21 Jump Steet - Episode 211 blah blah.mkv", ['21'], ['02', '11']],
    ["Sample.Show S03E01E02 Sample.Episode.mkv", [], ['03', '01', '02']],
    ["Sample.Show S03E01E02E03 Sample.Episode.mkv", [], ['03', '01', '02', '03']],
    ["Sample.Show 4x11 4x12 720p 1080p Sample.Episode.mkv", [], ['04', '11', '04', '12']],
    ["Sample.Show S02E06-07 720p 1080p Sample.Episode.mkv", [], ['02', '06', '07']],
    ["Sample.Show S02 ep03 720p 1080p Sample.Episode.mkv", [], ['02', '03']]
]

@pytest.fixture(params=get_episode_args)
def get_episode_params(request):
    return request.param

def test_get_epipsode(get_episode_params):
    assert(rename_episodes.get_episode(get_episode_params[0],
                                       get_episode_params[1]) == get_episode_params[2])
