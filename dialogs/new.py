# Betty > dialogs > new.py

#import logging

from PyQt5.QtWidgets import (QLabel, QListWidget, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout,
                             QDialog)
from PyQt5.QtCore import QSettings, QPoint, QSize, Qt
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
        self._readSettings()    # read current state of this dialog

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
        #self.resize(250, 100)

    def _connections(self):

        self.templateListWidget.itemDoubleClicked.connect(self.accept)
        self.createPushButton.clicked.connect(self.accept)
        self.cancelPushButton.clicked.connect(self.reject)

    def _readSettings(self):

        settings = QSettings("NEW", "new_dialog")
        position = settings.value("position", QPoint(200, 200))
        size = settings.value("size", QSize(250, 100))
        self.move(position)
        self.resize(size)

    def _writeSettings(self):

        settings = QSettings("NEW", "new_dialog")
        settings.setValue("position", self.pos())
        settings.setValue("size", self.size())

    def accept(self):

        self._writeSettings()
        self.done(1)
        #logging.info("[BET]: Template selection accepted")

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            self._writeSettings()
            self.close()

    def reject(self):

        self._writeSettings()
        self.close()

    def closeEvent(self, event):

        self._writeSettings()