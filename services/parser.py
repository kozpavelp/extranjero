import requests
from bs4 import BeautifulSoup


def soldol():

    SOL_DOL = 'https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BF%D0%B5%D1%80%D1%83%D0%B0%D0%BD%D1%81%D0%BA%D0%B8%D0%B9+%D1%81%D0%BE%D0%BB%D1%8C&oq=&aqs=chrome.1.69i57j69i59j35i39i650j0i67i650j0i512j0i20i263i512j0i67i650j0i512l2j0i20i263i512.4659j1j7&sourceid=chrome&ie=UTF-8&bshm=ncc/1'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}

    page = requests.get(SOL_DOL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})

    return convert[0].text