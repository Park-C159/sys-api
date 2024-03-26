import math

def toDate(x):
    year = 1
    num = x
    day_in_year = 365
    while num > day_in_year:
        num -= day_in_year
        year += 1
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            day_in_year = 366
    if day_in_year == 365:
        months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    else:
        months = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month = 1
    day = num
    for m, days in enumerate(months):
        if day > days:
            day -= days
            month += 1
        else:
            break

    return ("公元" + str(year) + "年" + str(month) + "月" + str(day) + "日")


x = 365 * 3 + 30+29
x = 1462
print(x)
date = toDate(x)
print(date)
