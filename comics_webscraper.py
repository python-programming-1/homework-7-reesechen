# Python - HW7_Comics Web Scraping - Chia-Yu Chen

# Write a python program that will download the latest 10 comic images from https://www.gocomics.com/pearlsbeforeswine/

import os
import requests
from bs4 import BeautifulSoup

url = 'https://www.gocomics.com/pearlsbeforeswine/'

# get main website
res = requests.get(url)
res.raise_for_status()  # check the url is fine
soup = BeautifulSoup(res.text)  # pass the page into the BeautifulSoup module

comic_link = soup.select('a[data-link="comics"]')[0]
comic_url = 'https://www.gocomics.com' + comic_link.get('href')


i = 0
while i < 10:
    comic_res = requests.get(comic_url)
    comic_res.raise_for_status()
    comic_soup = BeautifulSoup(comic_res.text)

    # find the image url
    image = comic_soup.select('a[itemprop="image"]')
    image_url = image[0].img.attrs['src'] + '.png'

    # download the image url
    image_res = requests.get(image_url)
    image_res.raise_for_status()

    # save the image url
    image_file = open(os.path.basename(image_url), 'wb')
    for chunk in image_res.iter_content(100000):
        image_file.write(chunk)
    image_file.close()

    # find the previous url
    prev_link = comic_soup.select('div.gc-calendar-nav__previous')[0].contents[3]
    comic_url = 'https://www.gocomics.com' + prev_link.get('href')

    i += 1
