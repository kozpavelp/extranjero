from bs4 import BeautifulSoup as bs
from selenium.webdriver import Chrome, ChromeOptions
from selenium_stealth import stealth
from time import sleep

from lexicon.lexicon import URLS


# adodndevivir parser
def adonde_parser(city):
    casa_dict = {}
    options = ChromeOptions()
    options.add_argument('--headless')
    bro = Chrome(options=options)
    stealth(driver=bro,
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            languages=["en-US", "en"],
            vendor="Google Inc.::Google Chrome::77.0.3865.90",
            renderer="Intel Iris OpenGL Engine",
            run_on_insecure_origins=True,
            webgl_vendor="Intel Inc.",
            fix_hairline=True,
            platform="Win32"
            )
    url = URLS[city]
    bro.get(url)
    sleep(2)
    soup = bs(bro.page_source, 'lxml')
    deps = soup.findAll('div', class_="sc-i1odl-2")
    for num, d in enumerate(deps):
        casa_dict[num + 1] = {}
        casa_dict[num + 1]['price'] = d.find('div', class_='sc-12dh9kl-4').text.strip()
        casa_dict[num + 1]['link'] = 'https://www.adondevivir.com' + d.find('a', class_='sc-i1odl-11').get('href')
        casa_dict[num + 1]['address'] = d.find('div', class_='jneaYd').text.strip()
        casa_dict[num + 1]['comment'] = d.find('div', class_='eodGhu').text.strip()

    print(casa_dict)
    return casa_dict




