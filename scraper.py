import requests
from bs4 import BeautifulSoup
import smtplib
import time

URL = 'https://www.ebay.com/itm/Canon-EOS-5D-Mark-IV-Digital-SLR-Camera-Body-Only/323086614873' #may replace with any eBay URL

headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'} #replace with personal user agent

def check_price():
    page = requests.get(URL, headers=headers)

    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    title = soup2.find(id="itemTitle").get_text()
    price = soup2.find(id="prcIsum", itemprop="price").get_text()

    converted_price = float(price[10:18].replace(',',''))
    converted_title = title[52:]

    print(converted_price)
    print(converted_title.strip())

    if converted_price < 1700: #replace with maximum price you want to be alerted for
        send_mail()

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('(EMAIL)', '(PASSWORD)')

    subject = "Price fell down!"
    body = 'Check the eBay link: ' + str(URL)

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'xxxx@gmail.com', #where email will be sent from
        'yyyy@gmail.com', #email that will receive
        msg
    )
    print("Email sent!")
    server.quit()


while True:
    check_price()
    time.sleep(60 * 60 * 24) #check everyday, can change accordingly