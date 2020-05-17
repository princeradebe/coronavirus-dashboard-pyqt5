import sys
import time
import urllib.request
import json
from corry import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from country import country_list

class MyForm(QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.get_all()
        countries = country_list.get_country()
        completer = QCompleter(countries)
        self.ui.country.setCompleter(completer)
        self.ui.country.editingFinished.connect(self.search)
    
    def get_all(self):
        url = "https://corona.lmao.ninja/v2/all"

        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'

        request = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(request)
        data = json.loads(resp.read().decode("utf-8"))
        time_stamp = data['updated']
        time_stamp_ft = time.strftime('%d-%B-%Y %H:%M:%S', time.localtime(time_stamp/1000))

        # Update GUI
        self.ui.activeCount.setText(str(data['active']))
        self.ui.recoveredCount.setText(str(data['recovered']))
        self.ui.confirmedCount.setText(str(data['cases']))
        self.ui.deathsCount.setText(str(data['deaths']))
        self.ui.criticalCount.setText(str(data['critical']))
        self.ui.lastUpdated.setText("Last updated: " + time_stamp_ft)        

    def search(self):
        url = "https://corona.lmao.ninja/v2/countries/" + self.ui.country.text()

        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'

        request = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(request)
        data = json.loads(resp.read().decode("utf-8"))
        flag_url = data['countryInfo']['flag']
        request = urllib.request.Request(flag_url, headers=headers)
        flag = urllib.request.urlopen(request).read()
        pixmap = QPixmap()
        pixmap.loadFromData(flag)
        time_stamp = data['updated']
        time_stamp_ft = time.strftime('%d-%B-%Y %H:%M:%S', time.localtime(time_stamp/1000))

        # Update GUI
        self.ui.countryFlag.setPixmap(pixmap)
        self.ui.activeCount.setText(str(data['active']))
        self.ui.recoveredCount.setText(str(data['recovered']))
        self.ui.confirmedCount.setText(str(data['cases']))
        self.ui.deathsCount.setText(str(data['deaths']))
        self.ui.criticalCount.setText(str(data['critical']))
        self.ui.lastUpdated.setText("Last updated: " + time_stamp_ft)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())