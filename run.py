import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

# Ensure Qt platform plugin can be found in various environments
if "QT_QPA_PLATFORM_PLUGIN_PATH" not in os.environ:
    try:
        import PyQt5
        pyqt_dir = os.path.dirname(PyQt5.__file__)
        candidate_plugins = [
            os.path.join(pyqt_dir, "Qt5", "plugins"),
            os.path.join(pyqt_dir, "Qt", "plugins"),
            os.path.join(pyqt_dir, "plugins"),
        ]
        for c in candidate_plugins:
            platforms_dir = os.path.join(c, "platforms")
            if os.path.isdir(platforms_dir):
                os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = platforms_dir
                break
    except Exception:
        pass

import res_rc
from main import NotePad

app = QApplication(sys.argv)
app.setApplicationName("NotePad")
app.setApplicationDisplayName("NotePad")
app.setWindowIcon(QIcon(":/img/resources/_app_icon.ico"))
app.setStyle("Fusion")
window = NotePad()
sys.exit(app.exec_() if hasattr(app, "exec_") else app.exec())


