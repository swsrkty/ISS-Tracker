from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer
import plotly.express as px
import pandas as pd
import requests

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.browser = QtWebEngineWidgets.QWebEngineView(self)

        vlayout = QVBoxLayout(self)
        vlayout.addWidget(self.browser)

        timer = QTimer(self)
        timer.timeout.connect(self.show_map)
        timer.start(5000)

        self.show_map()
        self.resize(1000,800)

    def show_map(self):
        req = requests.get('http://api.open-notify.org/iss-now.json')
        obj = req.json()
        lat = obj['iss_position']['latitude']
        lon = obj['iss_position']['longitude']
        config = {'staticPlot': True}
        df = pd.DataFrame({ 'lat': [lat], 'lon': [lon] })
        fig = px.scatter_geo(df, lat = 'lat', lon = 'lon')
        self.browser.setHtml(fig.to_html(include_plotlyjs = 'cdn', config = config))

if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    app.exec()
