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
    italic_font = QFont()
    italic_font.setItalic(True)
    
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
        self.clear_table()
        table = self.ui.tableWidget
        
        for type_title, words in result.items():
            row = table.rowCount()
            table.setRowCount(row+1)
            col = 0
            
            if type_title:
                type_title_cell = QTableWidgetItem(str(type_title))
                type_title_cell.setFont(MainView.bold_font)
                table.setItem(row, col, type_title_cell)
                row += 1

            for word, props in words.items():
                if word:
                    table.setRowCount(row+1)
                    word_cell = QTableWidgetItem(str(word))
                    table.setItem(row, col, word_cell)
                    col += 1 
                
                    if props:
                        props_cell = QTableWidgetItem(", ".join(props))
                        props_cell.setFont(MainView.italic_font)
                        table.setItem(row, col, props_cell)
                    row += 1
                    col = 0

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