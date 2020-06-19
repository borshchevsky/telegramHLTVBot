import datetime
import logging
import requests
import time
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
import telegram

from models import Base, Match, engine
from settings import GROUP_ID, TEAM, DB_URI

logging.basicConfig(filename='bot.log', level=logging.INFO)


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


def matches_to_show():
    matches_to_show = []
    all_matches = parse_hltv_matches()
    team_matches = check_team(all_matches)
    if team_matches:
        for match in team_matches:
            delta = match[2] - datetime.datetime.now()
            if datetime.timedelta(hours=0) < delta < datetime.timedelta(hours=24):
                matches_to_show.append(match)
    return matches_to_show


def monitor_matches(context):
    session = sessionmaker(engine)()
    now = datetime.datetime.now()
    matches = [match for match in session.query(Match).all() if datetime.timedelta(0) < match.match_time - now < datetime.timedelta(hours=24)]
    if matches:
        result_string = (
                f'*Поддержи {TEAM.upper()} в ближайших матчах:* \n\n'
                + '\n\n'.join(
                f'{match.match_time.strftime("%H:%M")} \- {match.team1} vs {match.team2}\. '
                f'{match.best_of.upper()}\. Турнир: {match.event.replace("-", "").replace(".", " ")} \.'
                + f' Трансляция: [Twitch]({match.twitch})'
                * (match.twitch != False)
                for match in matches
            )
        )
        context.bot.send_message(GROUP_ID, result_string, parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                 disable_web_page_preview=True)
    session.close()


USERS = {}


def run_command(update, context):
    def show_help(_):
        c = '\n'.join(i for i in commands)
        context.bot.send_message(GROUP_ID, f'*Команды бота:*\n{c}', parse_mode='Markdown')

    user_id = update.message.from_user.id
    if user_id in USERS:
        delta = time.monotonic() - USERS[user_id]
        if delta < 15:
            return
        else:
            USERS[user_id] = time.monotonic()
    else:
        USERS[user_id] = time.monotonic()
    commands = {
        '!today': show_today_matches,
        '!insta': show_instagram,
        '!vk': show_vk,
        '!twitch': show_twitch,
        '!help': show_help,
    }

    text = update.message.text
    if text in commands:
        commands[text](context)


def show_today_matches(context):
    matches = matches_to_show()
    if matches:
        result_string = '*Сегодняшние матчи:* \n\n' + \
                        '\n\n'.join(
                            f'{match[2].strftime("%H:%M")} \- {match[0]} vs {match[1]}\. '
                            f'{match[3].upper()}\. Турнир: {match[4].replace("-", "")} \.'
                            + f' Трансляция: [Twitch]({get_russian_twitch_link(match[5])})'
                            * (get_russian_twitch_link(match[5]) != False)
                            for match in matches
                        )
        context.bot.send_message(GROUP_ID, result_string, parse_mode=telegram.ParseMode.MARKDOWN_V2,
                                 disable_web_page_preview=True)
    else:
        context.bot.send_message(GROUP_ID, 'Сегодня матчей нет.')


def show_instagram(context):
    context.bot.send_message(GROUP_ID, 'Инстаграм Димы: https://www.instagram.com/dimaoneshot',
                             disable_web_page_preview=True)


def show_vk(context):
    context.bot.send_message(GROUP_ID, 'Группа ВК: https://vk.com/dimaoneshot', disable_web_page_preview=True)


def show_twitch(context):
    context.bot.send_message(GROUP_ID, 'Канал Twitch: https://twitch.tv/dimaoneshot', disable_web_page_preview=True)


def check_and_add_to_db():
    while True:
        matches = matches_to_show()
        if matches:
            session = sessionmaker(engine)()
            for match in matches:
                url = match[5]
                exists = session.query(Match.match_url).filter_by(match_url=url).scalar()
                if exists:
                    break
                else:
                    m = Match(
                        team1=match[0],
                        team2=match[1],
                        match_time=match[2],
                        best_of=match[3],
                        event=match[4],
                        match_url=match[5],
                        twitch=get_russian_twitch_link(match[5])
                    )
                    session.add(m)
            session.commit()
            session.close()
        time.sleep(1800)  # Проверяем матчи раз в 30 минут и добавляем в базу, если появились новые


if __name__ == '__main__':
    check_and_add_to_db()