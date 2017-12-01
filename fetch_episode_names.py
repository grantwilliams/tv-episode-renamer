#!/usr/bin/python3
import json
import requests
from config import APIKEY


api_base = "https://api.thetvdb.com"
api_key = {"apikey": APIKEY}
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 "+
                  "(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
r = requests.post('{}/login'.format(api_base), data=json.dumps(api_key), headers=headers)
token = r.json()['token']
headers['Authorization'] = 'Bearer ' + token


def search_series(series):
    response = requests.get('{}/search/series?name={}'.format(api_base, series), headers=headers)
    return response.json()


def get_episodes(series_id, page=1):
    data = []
    response = requests.get('{}/series/{}/episodes?page={}'.format(api_base, series_id, page), headers=headers).json()
    data.extend(response['data'])
    num_pages = int(response['links']['last'])
    if num_pages > 1:
        for page in range(2, num_pages + 1):
            response = requests.get('{}/series/{}/episodes?page={}'
                                    .format(api_base, series_id, page), headers=headers).json()
            data.extend(response['data'])
    return data


def start_search(series):
    series_results = search_series(series)
    if len(series_results['data']) > 1:
        for index, result in enumerate(series_results['data']):
            print('{}. {}'.format(index, result['seriesName']))

        while True:
            try:
                choice = int(input('Which is the correct result?: '))
            except ValueError:
                print('Choice not valid, please choose a number from the list above: ')
                continue
            else:
                if choice < 0 or choice >= len(series_results['data']):
                    print('Choice not valid, please choose a number from the list above: ')
                    continue
                else:
                    break
    else:
        choice = 0  # if there is only 1 search result

    series_id = series_results['data'][choice]['id']

    episodes = get_episodes(series_id)

    return episodes
