import sys

from PyQt5.QtWidgets import QApplication
from dockify import DockifyUI

app = QApplication(sys.argv)

window = DockifyUI()
window.show()

sys.exit(app.exec_())