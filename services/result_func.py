from services.fb_parser import parser, create_dict
from services.adonde_parser import adonde_parser
from time import sleep


def dict_handing(apart_dict: dict):
    page_dict = {}
    n = 1
    page = []
    for key, value in apart_dict.items():
        if 'price' in value:
            page.append(f'Цена: {value["price"]}, Адрес: {value["address"]}\nКомментарий продавца: {value["comment"]}\nСсылка: {value["link"]}')
        else:
            continue
        if key % 4 == 0:
            page_dict[n] = page
            n += 1
            page = []
    page_dict[n] = page
    return page_dict

def main_func(keyword):
    if keyword.endswith('fb'):
        page = parser(keyword)
        aparts: dict = create_dict(page, keyword)
        sleep(1)
    elif keyword.endswith('adon'):
        aparts: dict = adonde_parser(keyword)
    pages: dict = dict_handing(aparts)
    return pages