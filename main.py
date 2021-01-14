from bs4 import BeautifulSoup
from requests import get
import os
import sys
import time
from models.Flat import Flat
from Serialization import Serialization



# TODO: Dodać warunki przy filtrowaniu

# Mieszkania w katowicach w apartamentowcach pod wynajem w serwisie olx.pl
URL = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/katowice/?search%5Bfilter_enum_builttype%5D%5B0%5D=apartamentowiec'
priceMax = 1700
htmlPath = "outputs/data.html"
csvPath = "outputs/flats_list.csv"
clear = lambda: os.system('cls')


def parse_price(price):
    return float(price.replace(' ', '').replace('zł', '').replace(',', '.'))

def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()

def say_hello():
    print("\n")
    print("###############################")
    print("# OLX Webscraping Application #")
    print("###############################")


page = get(URL)
bs = BeautifulSoup(page.content, 'html.parser')
flatsList = []

if os.path.exists(htmlPath):
    os.remove(htmlPath)

if os.path.exists(csvPath):
    os.remove(csvPath)

say_hello()

print("\n")
print("[#    FETCHING DATA     #]")

print("\n")

index = 0
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

    # print(location, ' ', title, ' ', price)
    linkString = str(link['href'])
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

    if float(flat.price) <= priceMax:
        flatsList.append(flat)
    index += 1



# Tworzenie pliku csv z danymi
Serialization.serialize_to_csv(flatsList)
print("GENERATED .csv FILE")


# Tworzenie pliku html z danymi
Serialization.serialize_to_html(flatsList)
print("GENERATED .html FILE")




