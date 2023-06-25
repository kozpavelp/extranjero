from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from time import sleep

from lexicon.lexicon import LEXICON, URLS


options = ChromeOptions()
options.add_argument('--headless')
browser = Chrome(options=options)


# creating dict using keyword of city #
def create_dict(page, keyword):
    num = 1
    keyword = keyword.split('_')[0]
    apart_dict = dict()
    for casa in page:
        apart_dict[num] = {}
        link = casa.get_attribute('href')
        casa = casa.text.split('\n')
        if len(casa) == 3 and keyword in casa[2]:
            apart_dict[num]['price'] = casa[0]
            apart_dict[num]['comment'] = casa[1]
            apart_dict[num]['address'] = casa[2]
            apart_dict[num]['link'] = link
            num += 1
    return apart_dict


# get whole html #
def parser(keyword):
    city_url = URLS[keyword]
    options = ChromeOptions()
    options.add_argument('--headless')
    bro = Chrome(options=options)
    bro.get(city_url)
    sleep(2)
    city = keyword.split('_')[0]
    while True:
        bro.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        sleep(2)
        page = bro.find_elements(By.PARTIAL_LINK_TEXT, 'S/')
        aparts = page[-1].text.split('\n')
        if len(aparts) != 3 or city not in aparts[2]:
            break

    return page
