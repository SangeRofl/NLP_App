from PyQt5.QtWidgets import (
    QMainWindow, 
    QTableWidgetItem,
    QMenuBar,
    QMenu
)
from PyQt5.QtGui import QFont

from view.templates.main_ui import Ui_MainWindow


class MainView(QMainWindow):
    bold_font = QFont()
    bold_font.setBold(True)
    
    def __init__(self):
        super(MainView, self).__init__()
        self.ui = Ui_MainWindow(self)
        self.init_UI()

    def init_UI(self):
        self.create_menu_bar()
        self.hide_interface()
                
    def hide_interface(self):
        pass
    
    def create_menu_bar(self):
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)

        self.file_menu = QMenu("&File", self)
        menuBar.addMenu(self.file_menu)

    def fill(self, result):
        self.ui.output_text_textEdit.setText(result)

    def clear_table(self):
        table = self.ui.tableWidget
        table.clearContents()
        table.setRowCount(0)
        
    def add_row(self):
        table = self.ui.tableWidget
        
        selected_row = table.currentIndex().row()
        table.insertRow(selected_row + 1)
        
    def delete_row(self):
        table = self.ui.tableWidget
        row_index = table.currentRow()
        table.removeRow(row_index)