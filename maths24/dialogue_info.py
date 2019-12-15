import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout

from maths24.strings import Strings


class InfoDialog(QDialog):

    def __init__(self, strings: Strings, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('About')
        dlgLayout = QVBoxLayout()

        label = QLabel()
        label.setText('Using basic arethmetic operations, join all the number tiles together to make 24.<br>'
                      '<br>'
                      'Made by Courtney Pitcher<br>'
                      'More info on <a href="https://github.com/IgniparousTempest/maths24-qt">github.com</a>.')
        label.setTextFormat(Qt.RichText)
        label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        label.setOpenExternalLinks(True)
        dlgLayout.addWidget(label)

        btns = QDialogButtonBox()
        btns.setStandardButtons(QDialogButtonBox.Ok)
        btns.button(QDialogButtonBox.Ok).clicked.connect(self.close)
        dlgLayout.addWidget(btns)

        self.setLayout(dlgLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = InfoDialog(Strings('en'))
    dlg.show()
    sys.exit(app.exec_())
