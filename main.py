from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from bs4 import BeautifulSoup
from requests import get
import os
import sys
import smtplib
from models.Flat import Flat
from Serialization import Serialization


# TODO: Dodać warunki przy filtrowaniu

# Mieszkania w katowicach w apartamentowcach pod wynajem w serwisie olx.pl
URL = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/katowice/?search%5Bfilter_enum_builttype%5D%5B0%5D=apartamentowiec'
priceMax = 1700
htmlPath = "outputs/data.html"
csvPath = "outputs/flats_list.csv"
clear = lambda: os.system('cls')


# Parsowanie ceny ze strony
def parse_price(price):
    return float(price.replace(' ', '').replace('zł', '').replace(',', '.'))


# Funkcja służąca do wyświetlenia informacji o programie
def say_hello():
    print("\n")
    print("###############################")
    print("# OLX Webscraping Application #")
    print("###############################")
    print("\n")
    print("[#    FETCHING DATA     #]")
    print("\n")


# Funkcja służąca do wysłania emaila
def send_email():
    if os.path.exists('outputs/flats_list.csv'):
        from_email = 'olx.webscraping.bot@gmail.com'
        to_email = 'pawel.piatek2@edu.uekat.pl'
        msg = MIMEMultipart()
        msg['Subject'] = 'OLX Flats'
        msg['From'] = from_email
        msg['To'] = to_email

        sender_email = 'olx.webscraping.bot@gmail.com'
        password = 'webscraping1#'

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open('outputs/flats_list.csv', "rb").read())
        encoders.encode_base64(part)

        part.add_header('Content-Disposition', 'attachment', filename="flats_list.csv")

        # Dodanie pliku .csv z mieszkaniami jako załącznik
        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        print("SENT EMAIL TO: ", to_email)


# Pobranie zawartości strony
page = get(URL)
bs = BeautifulSoup(page.content, 'html.parser')
flatsList = []

# Sprawdzanie czy pliki istnieją, jeśli istnieją to zostają usunięte
if os.path.exists(htmlPath):
    os.remove(htmlPath)

if os.path.exists(csvPath):
    os.remove(csvPath)

# Wyświetlenie informacji o programie
say_hello()

# Przeszukiwanie ofert na OLX
for offer in bs.find_all('div', class_='offer-wrapper'):

    footer = offer.find('td', class_='bottom-cell')
    # strip() - usuwa znaki konca linii
    location = footer.find('small', class_='breadcrumb').get_text().strip()
    title = offer.find('strong').get_text().strip()
    price = parse_price(offer.find('p', class_='price').get_text().strip())
    link = offer.find('a')

    buildingType = ''
    area = ''
    rooms = ''

    linkString = str(link['href'])

    # Dodawane są wyłączenie oferty z OLX (oferty z podtalu Otodom nie są dodawane)
    if 'olx' in linkString:

        flatPage = get(linkString)
        bsFlat = BeautifulSoup(flatPage.content, 'html.parser')
        offerContent = bsFlat.find('div', class_='descriptioncontent')

        # Flat details
        for detail in offerContent.find_all('li', class_='offer-details__item'):
            itemName = detail.find('span').get_text().strip()
            itemContent = detail.find('strong', class_='offer-details__value').get_text().strip()

            if itemName == 'Rodzaj zabudowy':
                buildingType = itemContent

            if 'm²' in itemContent:
                area = itemContent.split(' ')[0]

            if itemName == 'Liczba pokoi':
                rooms = itemContent

        # Description
        description = bsFlat.find('div', id='textContent').get_text().strip()
        flat = Flat(title, location, 'OLX', buildingType, rooms, str(price), area, description, linkString)

    # Dodawane są tylko te eferty, które spełniają kryteria odnośnie ceny
    if float(flat.price) <= priceMax:
        flatsList.append(flat)

# Tworzenie pliku csv z danymi
Serialization.serialize_to_csv(flatsList)
print("GENERATED .csv FILE")


# Tworzenie pliku html z danymi
Serialization.serialize_to_html(flatsList)
print("GENERATED .html FILE")

# Wysyłanie e-mail
send_email()




