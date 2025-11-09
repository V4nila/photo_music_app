from PyQt5.QtWidgets import QApplication
import sys
from app.gui import PhotoMusicApp  # Import your GUI class

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhotoMusicApp()
    window.show()
    sys.exit(app.exec_())
