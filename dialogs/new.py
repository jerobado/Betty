
from PyQt5.QtWidgets import (QLabel, QListWidget, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout,
                             QDialog)

from resources.constants import WORK_TYPE

__author__ = 'Jero'


# Dialogs starts here...
class New(QDialog):

    def __init__(self, parent=None):
        super(New, self).__init__(parent)

        self._widgets()
        self._layout()
        self._properties()
        self._connections()

    def _widgets(self):

        self.templateLabel = QLabel("Template:")
        self.templateListWidget = QListWidget()
        self.templateListWidget.addItems(WORK_TYPE)
        self.templateListWidget.setCurrentRow(0)
        self.createPushButton = QPushButton("&Create")
        self.cancelPushButton = QPushButton("C&ancel")

    def _layout(self):

        grid = QGridLayout()
        grid.addWidget(self.templateLabel, 0, 0)
        grid.addWidget(self.templateListWidget, 1, 0)

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        buttons.addWidget(self.createPushButton)
        buttons.addWidget(self.cancelPushButton)

        combine = QVBoxLayout()
        combine.addLayout(grid)
        combine.addLayout(buttons)

        self.setLayout(combine)

    def _properties(self):

        # self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Add new Template")
        self.resize(250, 100)

    def _connections(self):

        self.templateListWidget.itemDoubleClicked.connect(self.accept)
        self.createPushButton.clicked.connect(self.accept)
        self.cancelPushButton.clicked.connect(self.reject)