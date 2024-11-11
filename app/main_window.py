import sys
import pandas as pd
import plotly.express as px
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os
from PyQt5.QtCore import Qt, QUrl


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("US Cities Map")
        self.h = 800 
        self.w = 600
        self.resize(self.h, self.w) 
        self.setStyleSheet("background-color: black;")
        # main container widget
        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0) 
        layout.setSpacing(0)  

        #  map data
        self.map_html_path = self.create_plotly_map()

        #display call
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl.fromLocalFile(self.map_html_path))

       
        layout.addWidget(self.web_view)

        container.setLayout(layout)
        self.setCentralWidget(container)

    def create_plotly_map(self):
        us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")

        fig = px.scatter_mapbox(
            us_cities, 
            lat="lat", 
            lon="lon", 
            hover_name="City", 
            hover_data=["State", "Population"],
            color_discrete_sequence=["fuchsia"], 
            zoom=3, 
            height=self.w 
            
        )
        fig.update_layout(
            mapbox_style="carto-darkmatter",
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
        )
        fig.show(config={'scrollZoom': True})  # opens web browswer view
        config = {
        "scrollZoom": True,  # Enable scroll-to-zoom
        "displayModeBar": False,  # Hide the mode bar (optional)
        }

        current_dir = os.path.dirname(os.path.abspath(__file__)) 
        html_path = os.path.join(current_dir, "_ui", "static", "us_cities_map.html")  
        fig.write_html(html_path)
        with open(html_path, "w",  encoding="utf-8") as f:
            f.write(fig.to_html(full_html=False, config=config))  # Pass the config here

        return html_path


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMainWindow {
            background-color: black;
        }
        QWebEngineView {
            background-color: black;
            border: none;
        }
    """)
    window = MainWindow()
    
    window.show()
    sys.exit(app.exec())
