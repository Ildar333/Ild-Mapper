import json
class Parser() :
    def __init__(self):
        pass
    #г. Нальчик ул. Лазо д. 6
    def get_json(self,jsonObject):
        data = jsonObject
        dict = data['response']['GeoObjectCollection']['featureMember']
        geo_position = dict[0]['GeoObject']['Point']['pos']
        return str(geo_position).split(' ')
        
            

