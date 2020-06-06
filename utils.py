import datetime
import time
import requests
from bs4 import BeautifulSoup
import telegram

from settings import GROUP_ID, TEAM


# Парсим все матчи со страницы матчей
def parse_hltv_matches():
    matches = {}
    r = requests.get('https://www.hltv.org/matches')
    parser = BeautifulSoup(r.text, 'html.parser')
    all_data = parser.findAll('div', class_='upcoming-match standard-box')
    for n, i in enumerate(all_data):
        team_tag = i.findAll('div', class_='team')
        event_tag = i.find('td', class_='event')
        best_of_tag = i.find('div', class_=['map map-text', 'map-text'])
        time_tag = i.find('div', class_='time')
        match_tag = i.find('a', class_='a-reset')
        match_url = 'https://hltv.org' + match_tag['href']
        if team_tag:
            team1, team2 = team_tag[0].text, team_tag[1].text
        else:
            continue
        event = event_tag.text
        best_of = best_of_tag.text
        match_time = datetime.datetime.fromtimestamp(int(time_tag['data-unix'][:10]))
        matches[n] = [team1, team2, match_time, best_of, event, match_url]
    return matches


# Проверяем есть ли в общем списке матчей матчи нашей команды и если есть, то отправляем список всех матчей команды
def check_team(data: dict):
    if not data:
        return None
    return [
        value
        for _, value in data.items()
        if TEAM.lower() in [i.lower() for i in value if isinstance(i, str)]
    ]


# Парсим ссылку на русскоязычную трансляцию на твиче
def get_russian_twitch_link(match_link):
    if not match_link:
        return False
    r = requests.get(match_link)
    parser = BeautifulSoup(r.text, 'html.parser')
    twitch_tag = parser.findAll('div', class_="external-stream")
    for i in twitch_tag:
        if 'Russia' in i.contents[0]['data-link-tracking-destination']:
            twitch_link = i.contents[0]['href']
            return twitch_link
    return False


def monitor_matches(context):
    matches_to_show = []
    all_matches = parse_hltv_matches()
    team_matches = check_team(all_matches)
    if team_matches:
        for match in team_matches:
            delta = match[2] - datetime.datetime.now()
            if datetime.timedelta(hours=0) < delta < datetime.timedelta(hours=24):
                matches_to_show.append(match)
    if matches_to_show:
        result_string = (
                f'*Поддержи {TEAM.upper()} в ближайших матчах:* \n\n'
                + '\n\n'.join(f'{match[2].strftime("%H:%M")} \- {match[0]} vs {match[1]}\.  '
                              f'{match[3].upper()}\. Турнир: {match[4].replace("-", "")} \.'
                              + f' Трансляция: [Twitch]({get_russian_twitch_link(match[5])})'
                              * (get_russian_twitch_link(match[5]) != False)
                              for match in matches_to_show
                              )
        )
        context.bot.send_message(GROUP_ID, result_string, parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                 disable_web_page_preview=True)
