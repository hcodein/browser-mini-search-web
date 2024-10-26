import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QMainWindow):
    def __init__(self):
        super(Browser, self).__init__()

        # Set the browser's main window properties
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://sites.google.com/view/minisearchweb/minisearchweb"))  # Set initial URL
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # Create a navigation bar
        navbar = QToolBar()
        navbar.setMovable(False)  # Disable toolbar movement
        self.addToolBar(navbar)

        # Back button
        back_btn = QAction("◀", self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        # Forward button
        forward_btn = QAction("▶", self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        # Reload button
        reload_btn = QAction("⟳", self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        # Home button
        home_btn = QAction("🏠", self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # URL bar styling to look more like a browser
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL or search...")  # Placeholder text
        self.url_bar.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border-radius: 10px;
                background: #f5f5f5;
                border: 1px solid #ccc;
            }
        """)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # Combo box for search engine selection
        self.search_engine_combo = QComboBox()
        self.search_engine_combo.addItems(["Google", "Yahoo", "DuckDuckGo"])
        navbar.addWidget(self.search_engine_combo)

        # Zoom in button
        zoom_in_btn = QAction("🔍+", self)
        zoom_in_btn.triggered.connect(self.zoom_in)
        navbar.addAction(zoom_in_btn)

        # Zoom out button
        zoom_out_btn = QAction("🔍-", self)
        zoom_out_btn.triggered.connect(self.zoom_out)
        navbar.addAction(zoom_out_btn)

        # Loading progress bar
        self.progress = QProgressBar()
        self.progress.setMaximumHeight(10)
        self.progress.setTextVisible(False)
        navbar.addWidget(self.progress)
        
        # Update the progress bar as the page loads
        self.browser.loadProgress.connect(self.update_progress)

        # Update the URL bar when the page changes
        self.browser.urlChanged.connect(self.update_url)

        # Set default zoom factor
        self.current_zoom = 1.0

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://sites.google.com/view/minisearchweb/minisearchweb"))

    def navigate_to_url(self):
        url = self.url_bar.text()
        search_engine = self.search_engine_combo.currentText()

        if not url.startswith("http"):
            if '.' in url:  # Checks if it's a URL
                url = "http://" + url
            else:  # Search the input
                if search_engine == "Google":
                    url = "https://www.google.com/search?q=" + url
                elif search_engine == "Yahoo":
                    url = "https://search.yahoo.com/search?p=" + url
                elif search_engine == "DuckDuckGo":
                    url = "https://duckduckgo.com/?q=" + url

        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def update_progress(self, value):
        self.progress.setValue(value)

    def zoom_in(self):
        self.current_zoom += 0.1
        self.browser.setZoomFactor(self.current_zoom)

    def zoom_out(self):
        self.current_zoom -= 0.1
        self.browser.setZoomFactor(self.current_zoom)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setApplicationName("PyQt5 Browser")
    window = Browser()
    app.exec_()
