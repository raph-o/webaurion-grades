import csv
import os
import sys
import requests

from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook

webaurion_url = 'https://webaurion.esiee.fr'
webhook_url = ('webhook url')
session = requests.session()


def login(username, password):
    r = session.post(webaurion_url + '/login', data={'username': username, 'password': password})
    return r.status_code == 200


def logout():
    r = session.get(webaurion_url + "/logout")
    return r.status_code == 200


def get_grades():
    html = session.get(webaurion_url).text
    soup = BeautifulSoup(html, 'html.parser')
    courses = soup.find_all('li', class_='ui-carousel-item')

    results = []
    for course in courses:
        note_element = course.find('span', class_='texteIndicateur')
        note = note_element.text.strip() if note_element else None

        title_element = course.find('span', class_='champsText2')
        title = title_element.text.strip() if title_element else None

        date_element = course.find('span', class_='champsDate')
        date = date_element.text.strip() if date_element else None

        results.append({
            'note': note,
            'title': title,
            'date': date
        })
    return results


def send_webhook(content):
    webhook = DiscordWebhook(url=webhook_url, content=content)
    webhook.execute()


def putGrades(grades):
    file_name = 'grades.csv'
    with open(file_name, 'a+', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        reader = csv.reader(f)

        if not os.path.isfile(file_name):
            writer = csv.writer(f)
            writer.writerow(['Titre', 'Date', 'Note'])

        f.seek(0)
        msg = ''
        for grade in grades:
            found = False
            for row in reader:
                if row[0] == grade['title']:
                    found = True
                    break

            if not found:
                writer.writerow([grade['title'], grade['date'], grade['note']])
                msg += f'Il y a une nouvelle note !\nMatière : {grade["title"]}, Date : {grade["date"]}, Note : {grade["note"]}\n'

        send_webhook(msg if msg != '' else 'Pas de nouvelle note')


if __name__ == '__main__':
    if login('username', 'password'):
        grades = get_grades()
        if grades is None:
            print('Erreur durant la récupération des notes')
            send_webhook('Erreur durant la récupération des notes')
            sys.exit(1)

        print(grades)
        putGrades(grades)

        if not logout():
            print('Erreur durant la déconnexion')
            send_webhook('Erreur durant la déconnexion')
            sys.exit(1)
    else:
        print('Erreur durant la connexion')
        send_webhook('Erreur durant la connexion')
        sys.exit(1)
