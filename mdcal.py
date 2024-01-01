import os
import re
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

def update_calendar(year, month, day, with_isoweek=False, start_from_Sun=False, lang="en"):
    # Check if README.md exists, if not, create one
    if not os.path.exists('README.md'):
        with open('README.md', 'w') as f:
            print("The file README.md does not exist. Creating a new one...")
            f.write('## 🎯 Calendar\n\n## Records\n\n')

    # Read the content of README.md
    with open('README.md', 'r') as file:
        content = file.read()

    # Extract the part between "## 🎯 Calendar" to the start of the next section "## Records".
    calendar_section_match = re.search("## 🎯 Calendar(.*)(?=## 🍃 Records)", content, re.DOTALL)
    
    # If "## 🎯 Calendar" section doesn't exist or there is no calendar data
    if calendar_section_match is None:
        return "The 'Calendar' section does not exist in README.md or there is no calendar data."

    calendar_section = calendar_section_match.group(1)

    # Check if the current month/year already exists in the calendar
    current_month_exists = "* {}/{}\n".format(year, month) in calendar_section
    calendar_section_lines = ["## 🎯 Calendar\n"]

    if not current_month_exists:
        # Create the calendar for the current month/year and append it
        cal = create_calendar(year, month, with_isoweek, start_from_Sun, lang)
        calendar_section_lines.append('* {}/{}\n'.format(year, month))
        calendar_section_lines += cal.split("\n")
        calendar_section_lines.append('\n') 
    else:
        # Append the existing calendar for the current month/year
        calendar_section_lines += calendar_section.split("\n")[2:]
    
    star_flag = True
    month_start_flag = False
    for i in range(4, len(calendar_section_lines)):
        if re.match("^\\|([ ]*.*[ ]*\|)+$", calendar_section_lines[i]):
            day_cells = calendar_section_lines[i].split("|")
            for j in range(1, len(day_cells) - 1):
                digit = re.findall(r'\d+', day_cells[j].strip())
                if len(digit) == 0:
                    continue
                if digit[0] == "1":
                    month_start_flag = True   
                if digit[0] == str(day) and "🌟" not in day_cells[j] and star_flag and month_start_flag:
                    day_cells[j] = day_cells[j].strip() + "🌟"
                    star_flag = False
            calendar_section_lines[i] = "|".join(day_cells)

    # Replace 'Calendar' section in README.md with the updated section
    new_content = re.sub(r"## 🎯 Calendar(.*)(?=## 🍃 Records)", "\n".join(calendar_section_lines), content, flags=re.DOTALL)
    
    with open('README.md', 'w') as file:
        file.write(new_content)

    return "Successfully updated Calendar of README.md"

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) == 3:
        year, month = [int(a) for a in argv[1:3]]
        print(update_calendar(year, month, datetime.now().day))
    elif len(argv) == 4:
        year, month, day = [int(a) for a in argv[1:4]]
        print(update_calendar(year, month, day))
    else:
        print('Usage: python mdcal.py [year] [month] [day]')