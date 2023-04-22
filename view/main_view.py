from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
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
        self.hide_interface()
                
    def hide_interface(self):
        pass
    
    def fill(self, result):
        self.clear_table()
        table = self.ui.tableWidget
        result = dict(sorted(result.items()))
        print("fill data: ", result)
        
        for lexem, wordforms in result.items():
            row = table.rowCount()
            table.setRowCount(row+1)
            col = 0
            
            if lexem:
                lexem_cell = QTableWidgetItem(str(lexem))
                lexem_cell.setFont(MainView.bold_font)
                table.setItem(row, col, lexem_cell)
                row += 1

            for wordform, seenumber_and_note in wordforms.items():
                if wordform:
                    table.setRowCount(row+1)
                    wordform_cell = QTableWidgetItem(str(wordform))
                    table.setItem(row, col, wordform_cell)
                    col += 1 
                
                    if seenumber := seenumber_and_note[0]:
                        seenumber_cell = QTableWidgetItem(str(seenumber))
                        table.setItem(row, col, seenumber_cell)
                    col += 1
                
                    if note := seenumber_and_note[1]:
                        seenumber_cell = QTableWidgetItem(str(note))
                        table.setItem(row, col, seenumber_cell)
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