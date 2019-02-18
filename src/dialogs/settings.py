""" Trying to separate every dialog in a file

    Settings Dialog
"""

__author__ = 'Jero'

from PyQt5.QtWidgets import (QPushButton, QDialog, QCheckBox, QVBoxLayout, QHBoxLayout,
                            QGridLayout)


class Settings(QDialog):

    def __init__(self, parent=None):
        super(Settings, self).__init__(parent)

        self._widgets()
        self._layout()
        self._properties()
        self._connections()

    def _widgets(self):

        self.appendCheckBox = QCheckBox("Append new template to previous template")
        self.acceptPushButton = QPushButton("&Apply")
        self.cancelPushButton = QPushButton("&Cancel")

    def _layout(self):

        editor_grid = QGridLayout()
        editor_grid.addWidget(self.appendCheckBox, 0, 0)

        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self.acceptPushButton)
        buttons.addWidget(self.cancelPushButton)

        vertically = QVBoxLayout()
        vertically.addLayout(editor_grid)
        vertically.addLayout(buttons)

        self.setLayout(vertically)

    def _properties(self):

        self.setWindowTitle("Settings")
        self.resize(400, 50)

    def _connections(self):

        self.appendCheckBox.stateChanged.connect(self.on_appendCheckBox_stateChanged)
        self.acceptPushButton.clicked.connect(self.accept)
        self.cancelPushButton.clicked.connect(self.reject)

    def on_appendCheckBox_stateChanged(self):

        if self.appendCheckBox.isChecked():
            # set APPEND to True
            print("APPEND is checked!")
            self.appendCheckBox.setChecked(True)
        else:
            # set APPEND to False
            print("APPEND is False")
