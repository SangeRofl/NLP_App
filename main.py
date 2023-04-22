# XDG_SESSION_TYPE=x11
# pyuic5 -x file.ui -o file.py
import sys

from PyQt5.QtWidgets import QApplication, QStackedWidget

from view.main_view import MainView
from controller.controller import Controller


class App(QApplication):
    '''Main application class.'''
    
    current_view = None

    def __init__(self, *args):
        super().__init__(list(args))
        self.controller = Controller(self)
        
        self.widgets = QStackedWidget()
        self.main_view = MainView()
        
        self.init_view()
        self.init_app()

    def init_app(self):
        # add widgets
        self.widgets.addWidget(self.main_view)
        # set size
        self.widgets.setFixedWidth(800)
        self.widgets.setFixedHeight(600)
        # show
        self.switch_view(self.main_view)
        self.widgets.show()
        
    def init_view(self):
        self.main_view.ui.process_pushButton.clicked.connect(self.process) 
        self.main_view.ui.add_pushButton.clicked.connect(self.add) 
        self.main_view.ui.delete_pushButton.clicked.connect(self.delete)
        self.main_view.ui.filter_pushButton.clicked.connect(self.filter)
        self.main_view.ui.reset_pushButton.clicked.connect(self.reset) 
        
    def switch_view(self, view):
        self.current_view = view
        self.widgets.setCurrentWidget(self.current_view)
        
    def process(self):
        text = self.main_view.ui.raw_text_textEdit.toPlainText()
        self.controller.process_text(text)
        
    def add(self):
        self.main_view.add_row()
    
    def delete(self):
        self.main_view.delete_row()
        
    def filter(self):
        filter_text = self.main_view.ui.filter_textEdit.toPlainText()
        self.controller.process_filter(filter_text)
    
    def reset(self):
        self.controller.process_reset()

def application():
    app = App(sys.argv)
    app.setApplicationName("NLP App")
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    application()
