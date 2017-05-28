# Betty > dialogs > new.py

from PyQt5.QtWidgets import (QLabel,
                             QPushButton,
                             QGridLayout,
                             QHBoxLayout,
                             QVBoxLayout,
                             QDialog,
                             QListView)
from PyQt5.QtCore import (QSettings,
                          Qt,)
from PyQt5.QtGui import QIcon
from resources._constants import WORKTYPE
from resources.models import WorktypeListModel


class New(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)
        self._widgets()
        self._layout()
        self._properties()
        self._connections()
        self._readSettings()    # read current state of this dialog

    def _widgets(self):

        self.templateLabel = QLabel("Template:")

        # DATA & MODEL:
        model = WorktypeListModel(WORKTYPE)

        # VIEW: use QListView
        self.templateListView = QListView()
        self.templateListView.setModel(model)
        self.templateListView.setCurrentIndex(model.index(0, 0))    # Set 'Filing' as selected

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
        self.restoreGeometry(settings.value("new_dialog_geometry", self.saveGeometry()))

    def _writeSettings(self):

        settings = QSettings("NEW", "new_dialog")
        settings.setValue("new_dialog_geometry", self.saveGeometry())

    def accept(self):

        self._writeSettings()
        self.done(1)

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            self._writeSettings()
            self.close()

        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self._writeSettings()
            self.done(1)

    def reject(self):

        self._writeSettings()
        self.close()

    def closeEvent(self, event):

        self._writeSettings()