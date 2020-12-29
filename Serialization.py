import csv

class Serialization:
    @staticmethod
    def serialize_to_html(list):
        testStr = ''
        for x in list:
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

    @staticmethod
    def serialize_to_csv(list):
        data = []
        # Przekszatałcanie do zaoisywania do pliku .csv
        for x in list:
            data.append([str(x.title), str(x.location), str(x.website), str(x.buildingType), str(x.rooms), str(x.price),
                         str(x.area), str(x.link)])

        # Serializowanie do pliku csv
        header = ['title', 'location', 'website (platform)', 'buildingType', 'rooms', 'price (zł)', 'area (m2)', 'link']

        # Zapisywanie do csv z ';' jako separator
        with open('outputs/flats_list.csv', 'w') as f:
            write = csv.writer(f, delimiter=";")
            write.writerow(header)
            write.writerows(data)
