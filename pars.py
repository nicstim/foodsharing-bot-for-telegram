import re
import sqlite3

def add_street(name):
    con = sqlite3.connect("spb.db")
    cur = con.cursor()
    cur.execute("INSERT INTO street(name) VALUES(?)",(name,))
    cur.close()
    con.commit()
    con.close()


def add_sub(name):
    con = sqlite3.connect("spb.db")
    cur = con.cursor()
    cur.execute("INSERT INTO subway(name) VALUES(?)",(name,))
    cur.close()
    con.commit()
    con.close()

# print(1)
# with open(f'sub.txt', 'r', encoding='utf-8') as f:
#         for line in f:
#             pr = line.strip()
#             if len(pr) > 0:
# #                 add_sub(pr)
# print(2)
# with open(f'street.txt', 'r', encoding='utf-8') as f:
#         for line in f:
#             r = line.strip()
#             pr = str(r)
#             if len(pr) > 0:
#                 add_street(pr)



def get_substrings(string):
    """Функция разбивки на слова"""
    return re.split('\W+', string)


def get_distance(s1, s2):
    """Расстояние Дамерау-Левенштейна"""
    d, len_s1, len_s2 = {}, len(s1), len(s2)
    for i in range(-1, len_s1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, len_s2 + 1):
        d[(-1, j)] = j + 1
    for i in range(len_s1):
        for j in range(len_s2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,
                d[(i, j - 1)] + 1,
                d[(i - 1, j - 1)] + cost)
            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)
    return(d[len_s1 - 1, len_s2 - 1])


def check_substring(search_request, original_text, max_distance):
    """Проверка нечёткого вхождения одного набора слов в другой"""
    substring_list_1 = get_substrings(search_request)
    substring_list_2 = get_substrings(original_text)

    not_found_count = len(substring_list_1)

    for substring_1 in substring_list_1:
        for substring_2 in substring_list_2:
            if get_distance(substring_1, substring_2) <= max_distance:
                not_found_count -= 1

    if not not_found_count:
        return True


search_request = 'Рыбацкое'
original_text = '''Здравствуйте
Лекарства, срок норм у всех сфоткан.
Масло облепихи просроченное.
Хилак фортэ целый.
Забирать метро рыбацкое, шлиссельбургский пр 13.
Пишите в личку.
Спасибо за размещение 🌸
'''

result = check_substring(search_request, original_text, max_distance=2)

print(result)  # True если найдено, иначе None
