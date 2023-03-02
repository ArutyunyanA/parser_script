import scrapy
from scrapy.crawler import CrawlerProcess
import config


class OglasiSpider(scrapy.Spider):
    name = 'oglasi'

    start_urls = ['https://www.example.com']

# converting report to csv format file

    custom_settings = {
        'FEEDS': {
            'rent.csv': {
                'format': 'csv'
            }
        }
    }
# inside this link we will get all information what we needed.

    def parse(self, response):
        author_page_links = response.xpath('//div//h2/a/@href')
        yield from response.follow_all(author_page_links, self.parse_author)

# iteration function of pagination link to get all results on web page

        pagination_links = response.css('li.paging_next a::attr(href)')
        yield from response.follow_all(pagination_links, self.parse)

# collecting the data

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='')

        yield {
            'contact': extract_with_css('div.kontakt-opis p::text').strip(),
            'ref_num': extract_with_css('div.dsc strong::text').strip(),
            'new_label': extract_with_css('span.new_label::text').strip(),
            'description': extract_with_css('div.kratek::text').strip(),
            'phone': extract_with_css('div.kontakt-opis a::text').strip(),
            'price': extract_with_css('div.cena span::text').strip(),
            'conditions': extract_with_css('div.web-opis p::text').strip(),
        }

# function for settings email and sending csv_file by mail service

def send_mail():
    import smtplib
    from email.message import EmailMessage

    message = EmailMessage()
    message['From'] = config.USER_NAME
    message['To'] = 'example@gmail.com'
    message['Subject'] = 'Letter'
    message.set_content('Hello, this is auto-message')
    with open("rent.csv", "r") as f:
        data = f.read()
    message.add_attachment(data, filename='rent.csv')

    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login(config.USER_NAME, config.PASSWORD)
    server.send_message(message)
    server.quit()


process = CrawlerProcess()
process.crawl(OglasiSpider)
process.start()
send_mail()





