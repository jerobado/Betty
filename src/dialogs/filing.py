# Betty > dialogs > filing.py

from PyQt5.QtGui import (QTextDocument,
                         QIcon)

from PyQt5.QtCore import (QSettings,
                          QPoint,
                          QSize,
                          Qt)

from PyQt5.QtWidgets import (QLabel,
                             QLineEdit,
                             QDialog,
                             QVBoxLayout,
                             QHBoxLayout,
                             QGridLayout,
                             QComboBox,
                             QTextEdit,
                             QPushButton,
                             QGroupBox)

from resources.constants import (TYPE_TM,
                                 FILING,
                                 FILING_SPECIAL,
                                 FILING_TEMPLATE,
                                 STYLE,
                                 GE_DEFAULT)


class Filing(QDialog):
    """ Main dialog for the Filing template form """

    def __init__(self, parent=None):
        super(Filing, self).__init__(parent)

        # resident variables
        self.DEFAULT_SI = ''

        # resident functions
        self._widgets()
        self._layout()
        self._properties()
        self._connections()
        self._readSettings()    # read current state of this dialog

    def _widgets(self):

        self.trackerLineEdit = QLineEdit()
        self.clientLabel = QLabel("Client:")
        self.clientComboBox = QComboBox()
        # TODO: you also need a freaking list to hold your growing clients here XD
        self.clientComboBox.insertItem(0, "GE")
        self.clientComboBox.insertItem(1, "Unilever")
        self.clientComboBox.setCurrentText("Unilever")
        self.TMNCLabel = QLabel("TMNC:")
        self.ToTMLabel = QLabel("Type of Trade Mark:")
        self.special_instructionsLabel = QLabel("Special Instructions:")
        self.previewLabel = QLabel("Preview:")
        self.TMNCLineEdit = QLineEdit()
        self.ToTMComboBox = QComboBox()
        self.ToTMComboBox.insertItems(0, TYPE_TM)
        self.ToTMComboBox.setCurrentText('Word in standard characters')
        self.special_instructionsLineEdit = QLineEdit()
        self.special_instructionsLineEdit.setPlaceholderText("Read correspondence for further instructions")
        self.previewTextEdit = QTextEdit()
        self.previewButton = QPushButton("Pr&eview")
        self.addButton = QPushButton("&Add")
        self.addButton.setEnabled(False)
        self.clearButton = QPushButton("&Clear")

    def _layout(self):

        tracker_layout = QHBoxLayout()
        tracker_layout.addWidget(self.trackerLineEdit)
        tracker_layout.addStretch()
        tracker_layout.addWidget(self.clientLabel)
        tracker_layout.addWidget(self.clientComboBox)

        grid = QGridLayout()
        grid.addWidget(self.TMNCLabel, 0, 0)
        grid.addWidget(self.TMNCLineEdit, 0, 1)
        grid.addWidget(self.ToTMLabel, 1, 0)
        grid.addWidget(self.ToTMComboBox, 1, 1)
        grid.addWidget(self.special_instructionsLabel, 2, 0)
        grid.addWidget(self.special_instructionsLineEdit, 2, 1)

        # input widgets inside the QGroupBox
        input_group = QGroupBox("Set Criteria")
        input_group.setLayout(grid)

        # arrange the buttons horizontally
        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self.previewButton)
        buttons.addWidget(self.addButton)
        buttons.addWidget(self.clearButton)

        # set everything vertically
        vertical = QVBoxLayout()
        vertical.addLayout(tracker_layout)
        vertical.addWidget(input_group)
        vertical.addWidget(self.previewLabel)
        vertical.addWidget(self.previewTextEdit)
        vertical.addLayout(buttons)

        # now let your parent arrange everything for you
        self.setLayout(vertical)

    def _properties(self):

        self.trackerLineEdit.setPlaceholderText("Marker")
        self.trackerLineEdit.setFrame(False)
        font_style = QTextDocument()
        font_style.setDefaultStyleSheet(STYLE)
        self.previewTextEdit.setDocument(font_style)
        #self.resize(410, 550)  # width, height
        self.setWindowIcon(QIcon(':/file_32.png'))
        self.setWindowTitle("Filing Template Form")


    def _connections(self):

        self.clientComboBox.activated.connect(self.on_clientComboBox_activated)
        self.previewButton.clicked.connect(self.on_previewButton_clicked)
        self.addButton.clicked.connect(self.accept)
        self.clearButton.clicked.connect(self.on_clearButton_clicked)

    def _readSettings(self):

        settings = QSettings("FILING", "filing_dialog")
        position = settings.value("position", QPoint(200, 200))
        size = settings.value("size", QSize(410, 550))
        self.move(position)
        self.resize(size)

    def _writeSettings(self):

        settings = QSettings("FILING", "filing_dialog")
        settings.setValue("position", self.pos())
        settings.setValue("size", self.size())

    def dialog_info(self):
        """ Dialog information identifier """

        return 'Filing'

    # EVENT HANDLER starts here
    def on_clientComboBox_activated(self):
        """" Event handler for the client dropdown list """

        if self.clientComboBox.currentText() == 'GE':
            self.DEFAULT_SI = GE_DEFAULT
        elif self.clientComboBox.currentText() == 'Unilever':
            self.DEFAULT_SI = ""
        else:
            print("#edw")

    def on_clearButton_clicked(self):

        self.TMNCLineEdit.clear()
        self.special_instructionsLineEdit.clear()
        self.previewTextEdit.clear()

    def on_previewButton_clicked(self):

        # Get user's input
        tmnc_trademark = self.TMNCLineEdit.text()
        type_trademark = self.ToTMComboBox.currentText()
        filing_special = self.special_instructionsLineEdit.text()

        # Check TMNC if not in uppercase
        if not tmnc_trademark.isupper():
            tmnc_trademark = str.upper(self.TMNCLineEdit.text())

        # Consolidate user's input
        html = FILING_TEMPLATE.substitute(default=self.DEFAULT_SI,
                                          special=FILING_SPECIAL.format(filing_special),
                                          filing=FILING.format(type_trademark, tmnc_trademark))

        # Show result
        self.previewTextEdit.setHtml(html)

        # Enable self.addButton
        self.addButton.setEnabled(True)

    # OVERRIDING: starts here
    def accept(self):

        self._writeSettings()
        self.done(1)

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            self._writeSettings()
            self.close()

    def closeEvent(self, event):

        self._writeSettings()