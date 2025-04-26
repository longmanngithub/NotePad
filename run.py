from main import NotePad
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
app.setStyle('Fusion')
window = NotePad()
sys.exit(app.exec())
