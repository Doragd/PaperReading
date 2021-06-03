"""Markdown Calendar Generator"""
import calendar
from datetime import datetime
import sys


def create_calendar(year, month, with_isoweek=False, start_from_Sun=False, lang="en"):
    firstweekday = 6 if start_from_Sun else 0

    cal = calendar.Calendar(firstweekday=firstweekday)

    mdstr = ""
    dic = get_dict(lang)

    colnames = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    if start_from_Sun:
        colnames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    if with_isoweek:
        colnames.insert(0, "Week")
    colnames = [dic[col] for col in colnames]

    mdstr += '|' + '|'.join(colnames) + '|' + '\n'
    mdstr += '|' + '|'.join([':-:' for _ in range(len(colnames))]) + '|' + '\n'

    for days in cal.monthdatescalendar(year, month):
        if with_isoweek:
            isoweek = days[0].isocalendar()[1]
            mdstr += '|' + str(isoweek) + '|' + \
                '|'.join([str(d.day) for d in days]) + '|' + '\n'
        else:
            mdstr += '|' + '|'.join([str(d.day) for d in days]) + '|' + '\n'

    return mdstr


def print_calendar(year, month, with_isoweek=False, start_from_Sun=False, lang="en"):
    print('{}/{}\n'.format(year, month))
    print(create_calendar(year, month, with_isoweek, start_from_Sun, lang))


def get_dict(lang='en'):
    dic = {}
    colnames = ['Week', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    colnames_ja = ['週', '月', '火', '水', '木', '金', '土', '日']
    if lang == 'en':
        for col in colnames:
            dic[col] = col
    elif lang == 'ja':
        for col, colja in zip(colnames, colnames_ja):
            dic[col] = colja
    else:
        for col in colnames:
            dic[col] = col
    return dic


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) == 1:
        today = datetime.now()
        print_calendar(today.year, today.month)
    elif len(argv) == 2:
        year = int(argv[1])
        for month in range(1, 13):
            print_calendar(year, month, with_isoweek=True)
    elif len(argv) == 3:
        year, month = [int(a) for a in argv[1:3]]
        print_calendar(year, month)
    else:
        print('Usage: python mdcal.py [year] [month]')