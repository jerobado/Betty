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
                             QGroupBox,
                             QCheckBox,
                             QLayoutItem,
                             QSpacerItem,
                             QSizePolicy)

from resources._constants import (TYPE_TM,
                                 ITU,
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
        self._readSettings()            # read current state of this dialog
        self.on_SetCriteria_changed()   # this works but not pleasing

    def _widgets(self):

        self.trackerLineEdit = QLineEdit()
        self.clientLabel = QLabel("Client:")
        self.clientComboBox = QComboBox()
        # TODO: you also need a freaking list to hold your growing clients here XD
        self.clientComboBox.insertItem(0, "GE")
        self.clientComboBox.insertItem(1, "Unilever")
        self.clientComboBox.setCurrentText("Unilever")
        self.TMNCLabel = QLabel("TMNC:")
        self.ToTMLabel = QLabel("Type of Trademark:")
        self.ituComboBox = QCheckBox("Intent to Use")
        self.special_instructionsLabel = QLabel("Special Instructions:")
        self.previewLabel = QLabel("Preview:")
        self.TMNCLineEdit = QLineEdit()
        self.ToTMComboBox = QComboBox()
        self.ToTMComboBox.insertItems(0, TYPE_TM)
        self.ToTMComboBox.setCurrentText('Word in standard characters')
        self.special_instructionsLineEdit = QLineEdit()
        self.special_instructionsLineEdit.setPlaceholderText("Read correspondence for further instructions")
        self.previewTextEdit = QTextEdit()
        self.copyallButton = QPushButton("&Copy All")
        self.addButton = QPushButton("&Add")
        self.clearButton = QPushButton("Cl&ear")

    def _layout(self):

        tracker_layout = QHBoxLayout()
        tracker_layout.addWidget(self.trackerLineEdit)
        tracker_layout.addStretch()
        tracker_layout.addWidget(self.clientLabel)
        tracker_layout.addWidget(self.clientComboBox)

        # Tandem widgets
        tandem_HBoxLyout = QHBoxLayout()
        tandem_HBoxLyout.addWidget(self.TMNCLabel)
        tandem_HBoxLyout.addWidget(self.TMNCLineEdit)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding)

        grid = QGridLayout()
        #grid.addLayout(tandem_HBoxLyout, 0, 0, 1, 2)
        grid.addWidget(self.TMNCLabel, 0, 0)
        grid.addWidget(self.TMNCLineEdit, 0, 1)
        #grid.setColumnStretch(2, 1)
        grid.addItem(spacer, 0, 2)
        grid.addWidget(self.ituComboBox, 0, 3)
        #grid.addWidget(self.ituComboBox, 0, 4)
        grid.addWidget(self.ToTMLabel, 1, 0)
        grid.addWidget(self.ToTMComboBox, 1, 1)
        grid.addWidget(self.special_instructionsLabel, 2, 0)
        grid.addWidget(self.special_instructionsLineEdit, 2, 1, 1, 3)

        # Input widgets inside the QGroupBox
        input_group = QGroupBox("Set Criteria")
        input_group.setLayout(grid)

        # Arrange the buttons horizontally
        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self.copyallButton)
        buttons.addWidget(self.addButton)
        buttons.addWidget(self.clearButton)

        # Set everything vertically
        vertical = QVBoxLayout()
        vertical.addLayout(tracker_layout)
        vertical.addWidget(input_group)
        vertical.addWidget(self.previewLabel)
        vertical.addWidget(self.previewTextEdit)
        vertical.addLayout(buttons)

        # Now let your parent arrange everything for you
        self.setLayout(vertical)

    def _properties(self):

        self.trackerLineEdit.setPlaceholderText("Marker")
        self.trackerLineEdit.setFrame(False)
        font_style = QTextDocument()
        font_style.setDefaultStyleSheet(STYLE)
        self.previewTextEdit.setDocument(font_style)
        self.setWindowIcon(QIcon(':/file_32.png'))
        self.setWindowTitle("Filing Template Form")

    def _connections(self):

        self.clientComboBox.currentIndexChanged.connect(self.on_clientComboBox_activated)
        self.clientComboBox.currentIndexChanged.connect(self.on_SetCriteria_changed)
        self.TMNCLineEdit.textChanged.connect(self.on_SetCriteria_changed)
        self.ToTMComboBox.currentIndexChanged.connect(self.on_SetCriteria_changed)
        self.ituComboBox.stateChanged.connect(self.on_SetCriteria_changed)
        self.special_instructionsLineEdit.textChanged.connect(self.on_SetCriteria_changed)
        self.copyallButton.clicked.connect(self.on_copyallButton_clicked)
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

    def on_SetCriteria_changed(self):

        # Get user's input
        tmnc_trademark = self.TMNCLineEdit.text()
        type_trademark = self.ToTMComboBox.currentText()
        filing_special = self.special_instructionsLineEdit.text()
        itu = ITU if self.ituComboBox.isChecked() else ""

        # Check TMNC if not in uppercase
        if not tmnc_trademark.isupper():
            tmnc_trademark = str.upper(self.TMNCLineEdit.text())

        # Consolidate user's input
        html = FILING_TEMPLATE.substitute(default=self.DEFAULT_SI,
                                          special=FILING_SPECIAL.format(filing_special),
                                          itu=itu,
                                          filing=FILING.format(type_trademark, tmnc_trademark))

        # Show result
        self.previewTextEdit.setHtml(html)

    def on_clearButton_clicked(self):

        self.TMNCLineEdit.clear()
        self.special_instructionsLineEdit.clear()
        if self.ituComboBox.isChecked(): self.ituComboBox.setChecked(False)

    def on_copyallButton_clicked(self):

        self.previewTextEdit.selectAll()
        self.previewTextEdit.copy()

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