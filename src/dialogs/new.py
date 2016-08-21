# Betty > dialogs > new.py

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
                          Qt,)
from PyQt5.QtGui import QIcon
from resources.constants import WORKTYPE
from resources.models import WorktypeListModel


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

        # DATA & MODEL:
        model = WorktypeListModel(WORKTYPE)

        # VIEW: use QListView
        self.templateListView = QListView()
        self.templateListView.setModel(model)
        #x = model.index()
        #print(x)
        #self.templateListView.setCurrentIndex()

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

        # TODO: this block of line here is not being use!
        print('rock \'n roll')
        raw_data = self.templateListView.currentIndex()
        row = raw_data.row()
        print(WORKTYPE[row], row)

    def accept(self):

        self._writeSettings()
        self.done(1)

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            self._writeSettings()
            self.close()
            print('closing')

        if event.key() == Qt.Key_Enter:
            print('rock \'n roll!')

        if event.key() == Qt.Key_Return:
            print('rock \'n roll to the world! \\m/')

    def reject(self):

        self._writeSettings()
        self.close()

    def closeEvent(self, event):

        self._writeSettings()