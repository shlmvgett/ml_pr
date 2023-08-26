import requests
from fake_useragent import UserAgent
from lxml import html
import csv
import time


def parse_page(page):
    content_items = page.xpath("//div[@class='topicbox']")
    for i in range(len(content_items) - 1):
        if len(content_items[i]) >= 3:
            date = content_items[i].xpath("//p/a")[i].text_content()
            content = content_items[i].xpath("//div[@class='text']")[i].text_content()
            num = content_items[i].xpath("//div[@class='votingbox']/div[1]")[i].text_content()
            link = "https://www.anekdot.ru" + content_items[i].xpath("//div[@class='votingbox']/div[3]/a[1]")[i].get('href')
            votes = content_items[i].xpath("//div[@class='votingbox']/div[2]")[i].get('data-r')

            with open('data.csv', 'a', newline='') as file:
                # num,link,date,likes,dislikes,text
                writer = csv.writer(file)
                writer.writerow([num, link, date, votes.split(";")[2], votes.split(";")[3], content])


def get_page():
    init_page_number = 820
    link_template = 'https://www.anekdot.ru/best/anekdot/'
    for page_number in range(init_page_number, 1, -1):
        print(f"Parse page: ", {page_number})
        page_link = link_template + str(page_number).zfill(4)
        response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})
        response.encoding = 'utf-8'
        page = html.fromstring(response.content)
        parse_page(page)
        time.sleep(0.3)


if __name__ == '__main__':
    get_page()
