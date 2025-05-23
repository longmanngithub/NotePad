import os.path
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QFileInfo, QTime, QDate
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog,QPrintPreviewDialog
from PyQt5.QtWidgets import *
from NotePad import Ui_NotePad
from functions import *


class NotePad(QMainWindow, Ui_NotePad):
    def __init__(self):
        super().__init__()
        self.window = QMainWindow()
        self.setupUi(self)
        self.show()
        
        self.showMaximized()
        
        # Globals
        self.filename = None
        self.path = ''
        
        # Inits
        self.update_title()
        
        # Connections
        self.actionNew.triggered.connect(self.new_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionSave_as.triggered.connect(self.save_file_as)
        self.actionBold.triggered.connect(self.bold)
        self.actionItalic.triggered.connect(self.italic)
        self.actionUnderline.triggered.connect(self.underline)
        self.actionAlign_Left.triggered.connect(self.align_left)
        self.actionAlign_Center.triggered.connect(self.align_center)
        self.actionAlign_Right.triggered.connect(self.align_right)
        self.actionAlign_Justify.triggered.connect(self.align_justify)
        self.actionUndo.triggered.connect(self.undo)
        self.actionRedo.triggered.connect(self.redo)
        self.fontcombo.activated.connect(self.font_family)
        self.font_size.valueChanged.connect(self.set_font_size)
        self.actionFont.triggered.connect(self.font_options)
        self.actionFont_Color.triggered.connect(self.text_color)
        self.actionBackground_Color.triggered.connect(self.bg_color)
        self.actionPrint.triggered.connect(self.print_file)
        self.actionPrint_Preview.triggered.connect(self.print_preview)
        self.actionExport_to_PDF.triggered.connect(self.export_to_pdf)
        self.actionInsert_Time.triggered.connect(self.insert_time)
        self.actionInsert_Date.triggered.connect(self.insert_date)
        
        self.actionAbout.triggered.connect(about_app)
        
        
# Functions

    # Set Window Title
    def update_title(self):
        if self.filename:
            self.setWindowTitle(f"{self.filename} - NotePad")
        else:
            self.setWindowTitle("Untitled - NotePad")
        
    # New File
    def new_file(self):
        try:
            if len(self.textEdit.toPlainText().strip()) !=0:
                prompt = QMessageBox.question(self, 'New File', 
                                 "This will clear current content. Continue?", 
                                 QMessageBox.Yes | QMessageBox.No
                                 )
                if prompt == QMessageBox.Yes:
                    new(self)
            else:
                new(self)
        except Exception as e:
            print(f"New file creation error: {e}")
            
    # Open File
    def open_file(self):
        try:
            path, _ = QFileDialog.getOpenFileName(self, 'Open a File', ':\\')
            if path:
                self.path = path 
                with open(path, 'r') as file:
                    content = file.read()
                    self.textEdit.setText(content)
                    self.filename = os.path.basename(self.path)
                    self.update_title() 
        except Exception as e:
            print(f"File opening error: {e}")
            
    # Save File
    def save_file(self):
        try:
            if self.path == '':     # If no file is opened, the call save as function
                self.save_file_as()
            
            content = self.textEdit.toPlainText().strip()
        
            with open(self.path, 'w') as file:
                file.write(content)
                self.statusbar.showMessage(f'{self.filename} has been saved successfully')
                self.update_title()
        except Exception as e:
            print(f'Error saving file: {e}')
            
    # Save As
    def save_file_as(self):
        try:
            path, _ = QFileDialog.getSaveFileName(self, 'Save file as', ':\\', 
                                                  "Text Files (*.txt);; All Files (*.*)"
                                                  )
            if path:
                content = self.textEdit.toPlainText().strip()
                self.path = path
                self.filename = os.path.basename(self.path)
                with open(self.path, 'w') as file:
                    file.write(content)
                    self.statusbar.showMessage(f'{self.filename} has been saved successfully')
                    self.update_title()
        except Exception as e:
            print(f'Error saveing file as: {e}')
            
    # Bold
    def bold(self):
        if self.textEdit.fontWeight() == QFont.Bold:
            self.textEdit.setFontWeight(QFont.Normal)
        else:
            self.textEdit.setFontWeight(QFont.Bold)
            
    # Italic
    def italic(self):
        if self.textEdit.fontItalic() == QFont.StyleItalic:
            self.textEdit.setFontItalic(False)
        else:
            self.textEdit.setFontItalic(True)
            
    # Underline
    def underline(self):
        state = self.textEdit.fontUnderline()
        self.textEdit.setFontUnderline(not state)
        
    # Align Left
    def align_left(self):
        self.textEdit.setAlignment(Qt.AlignLeft)
        
    # Align Center
    def align_center(self):
        self.textEdit.setAlignment(Qt.AlignCenter)
        
    # Align Right
    def align_right(self):
        self.textEdit.setAlignment(Qt.AlignRight)
        
    # Align Justify
    def align_justify(self):
        self.textEdit.setAlignment(Qt.AlignJustify)
        
    # Undo
    def undo(self):
        self.textEdit.undo()
        
    # Redo
    def redo(self):
        self.textEdit.redo()
        
    # Change Font Color
    def text_color(self):
        color = QColorDialog.getColor()
        self.textEdit.setTextColor(color)
        
    # Change Background Color
    def bg_color(self):
        color = QColorDialog.getColor()
        self.textEdit.setTextBackgroundColor(color)
        
    # Change Font
    def font_family(self):
        font = self.fontcombo.currentText()
        self.textEdit.setCurrentFont(QFont(font))
    
    # Change Font Size
    def set_font_size(self):
        size = self.font_size.value()
        self.textEdit.setFontPointSize(size)
        
    # Font Options
    def font_options(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)    
        
    # Print
    def print_file(self):
        printer = QPrinter(QPrinter.HighResolution)
        prompt = QPrintDialog(printer, self)
        if prompt.exec_() == QPrintDialog.Accepted:
            self.textEdit.print_(printer)
            
    # Print Preview
    def preview(self, printer):
        self.textEdit.print_(printer)
    def print_preview(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintPreviewDialog(printer, self)
        dialog.paintRequested.connect(self.preview)
        dialog.exec_()
    
    # Export to PDF
    def export_to_pdf(self):
        file, _ = QFileDialog.getSaveFileName(self, "Export to PDF", ':\\', 
                                              'PDF Files;; All Files'
                                              )
        if file:
            if QFileInfo(file).suffix() == "":
                file += '.pdf'
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(file)
            self.textEdit.document().print_(printer)
            
    # Insert Current Time
    def insert_time(self):
        time = QTime.currentTime()
        self.textEdit.insertPlainText(time.toString(Qt.DefaultLocaleLongDate))
        
    # Insert Current Date
    def insert_date(self):
        date = QDate.currentDate()
        self.textEdit.insertPlainText(date.toString(Qt.DefaultLocaleLongDate))
        
    # Prompt user to save on exit
    def closeEvent(self, event):
        try:
            # No file opened and NotePad empty
            if not self.filename and self.textEdit.toPlainText() == "":
                sys.exit()              
            # Save a new file
            elif not self.filename and self.textEdit.toPlainText() != "":
                ask = QMessageBox.question(
                    self, 'Save File Before Closing',
                    'This new document has not been saved. Do you want to save it before closing?',
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
                )
                if ask == QMessageBox.Yes:
                    self.save_file()
                    sys.exit()
                elif ask == QMessageBox.Cancel:
                    QtGui.QCloseEvent.ignore(event)
                else:
                    sys.exit()
            # Save a modified file
            elif file_changed(self.path, self.textEdit.toPlainText().strip()):
                ask = QMessageBox.question(
                    self, 'Save File Before Closing',
                    f'{self.filename} has been modified. Do you want to save changes before closing?',
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
                )
                if ask == QMessageBox.Yes:
                    self.save_file()
                    sys.exit()
                elif ask == QMessageBox.Cancel:
                    QtGui.QCloseEvent.ignore(event)
                else:
                    sys.exit()
            else:
                sys.exit()
        except Exception as e:
            print(f"Close event error: {e}")
            
    # 
                    
                    
                    
                    