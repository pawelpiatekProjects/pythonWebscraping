from bs4 import BeautifulSoup
from requests import get
import csv
from models.Flat import Flat

# TODO: Dodać warunki przy filtrowaniu

# Mieszkania w katowicach w apartamentowcach pod wynajem w serwisie olx.pl
URL = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/katowice/?search%5Bfilter_enum_builttype%5D%5B0%5D=apartamentowiec'


def parse_price(price):
    return float(price.replace(' ', '').replace('zł', '').replace(',', '.'))


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

data = []

# Przekszatałcanie do zaoisywania do pliku .csv
for x in flatsList:
    data.append([str(x.title), str(x.location), str(x.website), str(x.buildingType), str(x.rooms), str(x.price), str(x.area), str(x.link)])


# Serializowanie do pliku csv
header = ['title', 'location', 'website (platform)', 'buildingType', 'rooms', 'price (zł)', 'area (m2)', 'link']

# Zapisywanie do csv z ';' jako separator
with open('outputs/flats_list.csv', 'w') as f:
    write = csv.writer(f, delimiter=";")
    write.writerow(header)
    write.writerows(data)

# HTML

testStr = ''
for x in flatsList:
    # testStr = testStr + x
    testStr = testStr + '<div style="background-color: #eeeeee; padding: 30px; margin-bottom: 20px">'
    testStr = testStr + '<h3>' + x.title + '</h3>'
    testStr = testStr + '<ul>'
    testStr = testStr + '<li>' + '<p><b>Location: </b>' + x.location + '</p></li>'
    testStr = testStr + '<li>' + '<p><b>Website: </b>' + x.website + '</p></li>'
    testStr = testStr + '<li>' + '<p><b>Building type: </b>' + x.buildingType + '</p></li>'
    testStr = testStr + '<li>' + '<p><b>Number of rooms: </b>' + x.rooms + '</p></li>'
    testStr = testStr + '<li>' + '<p><b>Price (zł): </b>' + x.price + '</p></li>'
    testStr = testStr + '<li>' + '<p><b>Area (m2): </b>' + x.area + '</p></li>'
    testStr = testStr + '<li>' + f'<b>Link: </b><a href={x.link}>' + x.title + '<a/></li>'
    testStr = testStr + '</ul>'
    testStr = testStr + '</div>'

text = f'''
    <html>
        <body>
            <div style="padding: 30px">
                {testStr}
            </div>
        </body>
    </html>
'''

with open('outputs/data.html', 'w') as f:
    f.write(text)
    f.close()




