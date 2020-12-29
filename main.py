from bs4 import BeautifulSoup
from requests import get
import json
import pickle
import csv

# Mieszkania w katowicach w apartamentowcach pod wynajem w serwisie olx.pl
URL = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/katowice/?search%5Bfilter_enum_builttype%5D%5B0%5D=apartamentowiec'


def parse_price(price):
    return float(price.replace(' ', '').replace('zł', '').replace(',', '.'))

class Flat:
    def __init__(self, title, location, website, buildingType, rooms, price, area, description, link):
        self.title = title
        self.location = location
        self.website = website
        self.buildingType = buildingType
        self.rooms = rooms
        self.price = price
        self.area = area
        self.description = description
        self.link = link

    def print_values(self):
        print(self.title + '; ' + self.location + '; ' + self.website + '; ' + self.buildingType + '; ' + self.rooms + '; ' + self.price + '; ' + self.area + '; ' + self.description + '; ' + self.link)

    def get_link(self):
        return f'{self.link}'


page = get(URL)
bs = BeautifulSoup(page.content, 'html.parser')
flatsList = []

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


    else:
        flatPage = get(linkString)
        bsFlat = BeautifulSoup(flatPage.content, 'html.parser')
        offerContent = bsFlat.find('div', class_='css-2wxlkt')

        # Flat details
        for detail in offerContent.find_all('div', class_='css-11ic80g'):
            itemName = detail.find('div', class_='css-152vbi8').get_text().strip()
            itemContent = detail.find('div', class_='css-1s5nyln').get_text().strip()
            if itemName == 'Rodzaj zabudowy:':
                buildingType = itemContent

            if itemName == 'Powierzchnia:':
                area = itemContent.split(' ')[0]

            if itemName == 'Liczba pokoi:':
                rooms = itemContent

        # Flat description
        description = bsFlat.find('section', class_='css-2kt7ta')
        descriptionContent = description.find('div')
        descriptionText = ''
        for descriptionRow in descriptionContent.find_all('p'):
            descriptionText = descriptionText + descriptionRow.get_text().strip()

        flat = Flat(title, location, 'OTODOM', buildingType, rooms, str(price), area, descriptionText, linkString)

    flatsList.append(flat)

# jsonString = json.dumps(flatsList)
# print(jsonString)



data = []

# for x in flatsList:
#     data.append({
#         'title': x.title,
#         'location': x.location,
#         'website': x.website,
#         'buildingType': x.buildingType,
#         'rooms': x.rooms,
#         'price': x.price,
#         'area': x.area,
#         'description': x.description,
#         'link': x.link
#     })

for x in flatsList:
    # data.append([str(x.title), str(x.location), str(x.website), str(x.buildingType), str(x.rooms), str(x.price), str(x.area), str(x.description), str(x.link)])
    data.append([str(x.title), str(x.location), str(x.website), str(x.buildingType), str(x.rooms), str(x.price), str(x.area), str(x.link)])
    # data.append(['aaa', 'bbb', 'ccc', 'ddd', 'eee', 'fff', 'ggg', 'hhh', 'iii'])

# for x in data:
#     print(x)
#
#     print('-----------')

# Serialize csv
header = ['title', 'location', 'website (platform)', 'buildingType', 'rooms', 'price (zł)', 'area (m2)', 'link']

with open('flats_list.csv', 'w') as f:
    write = csv.writer(f, delimiter=";")
    write.writerow(header)
    write.writerows(data)

# Serialize pickle
# filename = 'test'
# outfile = open(filename, 'wb')
# pickle.dump(data, outfile)
# outfile.close()

# for x in flatsList:
#     # x.print_values()
#     print(x)
#     print('--------------------------')


