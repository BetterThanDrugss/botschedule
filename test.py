# -*- coding: utf-8 -*-
import calendar
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import date
from datetime import timedelta


def get_html_from_source(url):
    html_doc = urlopen(url).read()
    soup = BeautifulSoup(html_doc, features="html.parser")
    return soup


def save_file(soup):
    s = str(soup)
    with open("test.txt", 'w') as file_handler:
        file_handler.write(s)


def english_bug(lesson):
    if len(lesson) == 5:
        return lesson
    elif len(lesson) > 5:
        if 'неделя' in lesson:
            lesson.pop(-1)
            lesson.pop(-1)
            return english_bug(lesson)
        else:
            while len(lesson) != 5:
                lesson[1] += ' ' + lesson[2]
                lesson.pop(2)
            return lesson
    else:
        try:
            int(lesson[3])
            print('try')
            print(lesson[3])
            lesson.append(lesson[3])
            lesson[3] = lesson[2]
            lesson[2] = ''
            return lesson
        except Exception as err:
            print('Except')
            lesson.append('-')
            return lesson


def get_day():
    my_date = date.today()
    return calendar.day_name[my_date.weekday()]


def get_next_day():
    my_date = date.today()
    tomorrow = my_date + timedelta(days=1)
    return calendar.day_name[tomorrow.weekday()]


def get_info_for_mes(lesson_num, lesson):
    try:
        lesson = english_bug(lesson)
        message = """\nПара {}: {}
        Преподаватель: {} {}
        Группа: {}
        Кабинет: {}
        """.format(lesson_num, lesson[0], lesson[1], lesson[2], lesson[3], lesson[4])
        return message
    except Exception as err:
        message = ''
        print('{} {}'.format(err, lesson_num))
        return message


def test(soup, day_or_next_day):
    if day_or_next_day == 0:
        day = get_day()
    else:
        day = get_next_day()

    DAYS = {'Monday': '1', 'Tuesday': '2', 'Wednesday': '3', 'Thursday': '4', 'Friday': '5', 'Saturday': '6'}
    if day in DAYS:
        day_num = DAYS.get(day)
        search_str = 'pair lw_' + str(day_num)
        lessons_code = soup.find_all(class_=re.compile(search_str))
        lessons_lst = []
        for i in lessons_code:
            lesson = str(i)
            if lesson.find('removed') == -1:
                lessons_lst.append(lesson)
            else:
                pass
        clear_lessons_lst = []
        for i in lessons_lst:
            clear_lessons_lst.append(clear_info(i))
        return clear_lessons_lst

    else:
        return 'Сегодня нет пар, гуляй Бамбина <3 '


def clear_info(lesson):
    lesson = str(lesson)
    soup = BeautifulSoup(lesson, features="html.parser")
    lesson = str(soup.getText()).split()
    return lesson


def main(num, link):
    soup = get_html_from_source(link)
    save_file(soup)

    if num == 0:
        result = test(soup, 0)
        return result

    else:
        result = test(soup, 1)
        return result


if __name__ == "__main__":
    main(1, 'https://kbp.by/rasp/timetable/view_beta_tbp/?cat=group&id=24')
