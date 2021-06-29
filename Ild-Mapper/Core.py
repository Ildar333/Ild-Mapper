import sys
from PyQt5.QtCore import QUrl
import requests
from requests.models import parse_header_links
import mapper_ui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from requests import api
import folium
import io
import JSONPARSER
import dbmodule.DBCONNECTION
import datetime

class Interface(QtWidgets.QMainWindow,mapper_ui.Ui_MainWindow):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.btnAction.clicked.connect(self.parse)
        self.btnSave.clicked.connect(self.save)
        self.btnMap.clicked.connect(self.init_map)
        self.parser_json = JSONPARSER.Parser
        self.json_resp = None
        self.service = None
        self.logTime = str(datetime.datetime.now())
        self.input_query = None
        self.response = None
        self.description = None

    def parse(self):
        self.txtLongitude.clear(); self.txtLatitude.clear()
        self.parse_inputQuery(self.txtQuery.text())
        resp = self.parse_request()
        get_point = self.parser_json.get_json(self, resp.json())
        self.txtLongitude.append(get_point[0]); self.txtLatitude.append(get_point[1])
        
    def parse_inputQuery(self, query):
        self.query = query
    
    def parse_request(self):
        request = requests.get('https://geocode-maps.yandex.ru/1.x/?format=json&apikey={api}&geocode={addr}'.format(api='a96a2feb-3396-4d0d-a39b-3fb9b46e40b3', addr=self.query))
        self.json_resp = str(request.json())
        self.service = 'Yandex'
        self.input_query = self.query
        return request

    def save(self):
        self.response = str(self.txtLongitude.toPlainText() +' '+ self.txtLatitude.toPlainText())
        self.description = self.textEdit.toPlainText()
        values = (f"{self.service}",f"{self.logTime}",f"{self.query}", f"{self.response}", f"{self.description}", f"{self.json_resp}")
        dbmodule.DBCONNECTION.external_request('insert',values)
        dbmodule.DBCONNECTION.external_request('show_all', None)

    def init_map (self):
        coordinates = [self.txtLatitude.toPlainText(), self.txtLongitude.toPlainText()]
        layout = QVBoxLayout()
        self.setLayout(layout)

        map = folium.Map(tiles="cartodbpositron",location=coordinates, zoom_start=18)
        folium.Marker(location=coordinates, popup=self.description).add_to(map)
        data = io.BytesIO()
        map.save('stuff.html')
        
        web_view = QWebEngineView()
        web_view.load(QUrl("E:/python_Projects/Mapper/stuff.html"))
        web_view.show()
        layout.addWidget(web_view)

def main ():
    app = QtWidgets.QApplication(sys.argv)
    window = Interface()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()