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
