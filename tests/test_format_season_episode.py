import pytest
import rename_episodes

format_season_episode_args = [
    [['01', '02'], 'S01E02'],
    [['01', '02', '03'], 'S01E02E03'],
    [['01', '02', '03', '04'], 'S01E02E03E04'],
    [['01', '02', '01', '03'], 'S01E02E03'],
    [['01', '01', '01', '02'], 'S01E01E02']
]

@pytest.fixture(params=format_season_episode_args)
def params_format_season_episode(request):
    return request.param

def test_format_season_episode(params_format_season_episode):
    assert(rename_episodes.format_season_episode(params_format_season_episode[0])
           == params_format_season_episode[1])
