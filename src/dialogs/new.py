# Betty > dialogs > new.py

#import logging

from PyQt5.QtWidgets import (QLabel,
                             QPushButton,
                             QGridLayout,
                             QHBoxLayout,
                             QVBoxLayout,
                             QDialog,
                             QListView)
from PyQt5.QtCore import (QSettings,
                          QPoint,
                          QSize,
                          Qt,
                          QAbstractListModel)
from PyQt5.QtGui import QIcon
from resources.constants import WORK_TYPE

__author__ = 'Jero'


class WorktypeListModel(QAbstractListModel):

    def __init__(self, worktypes, parent=None):
        super(WorktypeListModel, self).__init__(parent)
        self.__worktype = worktypes

    def data(self, index, role):
        if role == Qt.DisplayRole:
            row = index.row()
            value = self.__worktype[row]
            return value

        if role == Qt.DecorationRole:
            row = index.row()
            value = self.__worktype[row]

            if value == 'Filing':
                return QIcon(':/file_32.png')

            if value == 'Search (SIW)':
                return QIcon(':/magnify_32.png')

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def rowCount(self, parent):
        return len(self.__worktype)


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

        # DATA: define here
        data = WORK_TYPE

        # MODEL: use QStringListModel
        model = WorktypeListModel(data)

        # VIEW: use QListView
        self.templateListView = QListView()
        self.templateListView.setModel(model)

        self.createPushButton = QPushButton("&Create")
        self.cancelPushButton = QPushButton("C&ancel")

    def _layout(self):

        grid = QGridLayout()
        grid.addWidget(self.templateLabel, 0, 0)
        grid.addWidget(self.templateListView, 1, 0)

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        buttons.addWidget(self.createPushButton)
        buttons.addWidget(self.cancelPushButton)

        combine = QVBoxLayout()
        combine.addLayout(grid)
        combine.addLayout(buttons)

        self.setLayout(combine)

    def _properties(self):

        self.setWindowTitle("Add new Template")
        self.setWindowIcon(QIcon(':/new.png'))

    def _connections(self):

        self.templateListView.doubleClicked.connect(self.accept)
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

    def on_templateListView_doubleClicked(self):
        raw_data = self.templateListView.currentIndex()
        row = raw_data.row()
        print(WORK_TYPE[row])

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