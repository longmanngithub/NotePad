from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox

def new(ui):
    ui.textEdit.clear()
    ui.filename = None
    ui.statusbar.showMessage("A new file has been created.")
    ui.setWindowTitle("Untitled - NotePad")
    
def file_changed(filename, NotePad_text):
    with open(filename, 'r') as file:
        existing = file.read()
    return True if existing != NotePad_text else False

def about_app():
    msg = QMessageBox()
    msg.setWindowTitle("About NotePad")
    icon = QtGui.QIcon()
    icon.addPixmap(
        QtGui.QPixmap('./resources/_app_icon.ico'),
        QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
    msg.setWindowIcon(icon)
    msg.setText(
        "<p><b>NotePad</b> v1.0</p>"
        
        "This NotePad is supercharged with Python.<br>"
    )
    msg.exec_()
    