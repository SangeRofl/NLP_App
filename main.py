# XDG_SESSION_TYPE=x11
# pyuic5 -x file.ui -o file.py
import sys, json

from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication, 
    QStackedWidget, 
    QFileDialog,
)

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
        self.main_view.ui.send_pushButton.clicked.connect(self.send)
        
    def switch_view(self, view):
        self.current_view = view
        self.widgets.setCurrentWidget(self.current_view)
        
    def send(self):
        text = self.main_view.ui.raw_text_textEdit.toPlainText()
        response = self.controller.send_message(text)
        self.main_view.fill(response)
    
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
    
    @QtCore.pyqtSlot()
    def action_clicked(self):
        action = self.sender()
        if action.text() == "Open...":
            self.fname = QFileDialog.getOpenFileName(self.main_view)[0]
            self.load_file(types=["json"])
        elif action.text() == "Open Doc...":
            self.fname = QFileDialog.getOpenFileName(self.main_view)[0]
            self.load_file(types=["doc", "docx"])
        elif action.text() == "Save...":
            self.save_file()    
    
    def load_file(self, types: list):
        if self.fname.split('.')[-1] not in types:
            print("Invalid file type!")
            return
        
        if "json" in types:
            with open(self.fname, 'r') as f:
                data = json.load(f)
                self.controller.fill_load_data(data)
        elif "doc" in types:
            with open(self.fname, 'r') as f:
                text = f.read()
            self.main_view.ui.raw_text_textEdit.setText(text)
    
    def save_file(self):
        result = self.controller.get_result()
        fname = QFileDialog.getSaveFileName(self.main_view)[0]

        try:
            with open(fname, 'w') as f:
                json.dump(result, f, indent=4)
        except Exception as e:
            print(e.__str__())
            print("couldn't save file!")

def application():
    app = App(sys.argv)
    app.setApplicationName("NLP App")
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    application()
