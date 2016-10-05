# Betty > dialogs > search.py

from PyQt5.QtGui import (QTextDocument,
                         QTextCharFormat,
                         QIcon)

from PyQt5.QtCore import (QDate,
                          QStringListModel,
                          Qt,
                          QSettings,
                          QSize,
                          QPoint)

from PyQt5.QtWidgets import (QLabel,
                             QLineEdit,
                             QPushButton,
                             QComboBox,
                             QCheckBox,
                             QDateEdit,
                             QTextEdit,
                             QSpinBox,
                             QGridLayout,
                             QDialog,
                             QHBoxLayout,
                             QVBoxLayout,
                             QGroupBox,
                             QCalendarWidget,
                             QCompleter)

from resources._constants import (SEARCH_SPECIAL,
                                 SEARCH_TEMPLATE,
                                 ARTWORK_TOOLTIP,
                                 IMAGE_TOOLTIP,
                                 WITH_ARTWORK,
                                 WITH_IMAGE,
                                 GOOGLE_DEFAULT,
                                 GOOGLE_TAT,
                                 ABBOTT_TAT,
                                 UN_TAT,
                                 GE_TAT,
                                 STYLE)


# Main dialog for searching template
class Search(QDialog):

    def __init__(self, parent=None):
        super(Search, self).__init__(parent)

        # resident variables
        self.date_format = 'd MMM yyyy'
        self.due_date = QDate.currentDate()
        self.today = QDate.currentDate()
        self.selected_TAT = ''
        self.artwork = ''
        self.image = ''
        self.special_ins = ''
        self.client_TAT = ''
        self.DEFAULT_SI = ''

        # TEST: trying to implement QCompleter here
        self.suggested_markers_model = QStringListModel()
        self.suggested_markers_model.setStringList(["bapples", "banana", "apple", "orange", "amazing"])
        self.tracker_completer = QCompleter()
        self.tracker_completer.setModel(self.suggested_markers_model)
        self.tracker_completer.setCaseSensitivity(Qt.CaseInsensitive)

        # resident functions
        self._widgets()
        self._layout()
        self._properties()
        self._connections()
        self._readSettings()            # read current state of this dialog
        self.on_setCriteria_changed()   # Method that will handle the changes in the Set Criteria fields

    def _widgets(self):
        """ Create new PyQt widgets here """

        self.trackerLineEdit = QLineEdit()
        self.clientLabel = QLabel("Client:")
        self.clientComboBox = QComboBox()
        # TODO: you need a freaking list to hold your growing clients :)
        self.clientComboBox.insertItem(0, "Abbott")
        self.clientComboBox.insertItem(1, "GE")
        self.clientComboBox.insertItem(2, "Google")
        self.clientComboBox.insertItem(3, "Unilever")
        self.clientComboBox.setCurrentText("Unilever")
        self.due_dateLabel = QLabel("Due Date:")
        self.importanceLabel = QLabel("Select Importance:")
        self.specialLabel = QLabel("Special Instruction:")
        self.due_dateDateEdit = QDateEdit(QDate.currentDate())  # initialize by current date
        self.defaultCalendar = QCalendarWidget()
        self.currentDateFormat = QTextCharFormat()
        self.currentDateFormat.setFontWeight(75)
        self.daysSpinBox = QSpinBox()
        self.importanceComboBox = QComboBox()  # provide a list when using this widget for it's content
        self.importanceComboBox.insertItem(0, "Low/Medium")
        self.importanceComboBox.insertItem(1, "Critical")
        self.importanceComboBox.setCurrentIndex(0)
        self.with_artworkCheckBox = QCheckBox("With Artwork")
        self.with_imageCheckBox = QCheckBox("With Image")
        self.specialLineEdit = QLineEdit()
        self.previewLabel = QLabel("Preview:")
        self.previewTextEdit = QTextEdit()
        self.previewButton = QPushButton("Pr&eview")
        self.addButton = QPushButton("&Add")
        self.clearButton = QPushButton("&Clear")

    def _layout(self):
        """ Set and arrange PyQt widgets here """

        # clientLabel + clientComboBox
        label_combobox_HBoxLayout = QHBoxLayout()
        label_combobox_HBoxLayout.addWidget(self.trackerLineEdit)
        label_combobox_HBoxLayout.addStretch()
        label_combobox_HBoxLayout.addWidget(self.clientLabel)
        label_combobox_HBoxLayout.addWidget(self.clientComboBox)

        label_dateEdit_tandem = QHBoxLayout()
        label_dateEdit_tandem.addWidget(self.due_dateLabel)
        label_dateEdit_tandem.addWidget(self.due_dateDateEdit)
        label_dateEdit_tandem.addWidget(self.daysSpinBox)

        label_comboBox_tandem = QHBoxLayout()
        label_comboBox_tandem.addWidget(self.importanceLabel)
        label_comboBox_tandem.addWidget(self.importanceComboBox)

        grid = QGridLayout()  # widget ka pala
        grid.addLayout(label_dateEdit_tandem, 0, 0)     # Label, DateEdit, SpinBox
        grid.addWidget(self.with_artworkCheckBox, 0, 2)
        grid.addLayout(label_comboBox_tandem, 1, 0)     # Label, ComboBox
        grid.addWidget(self.with_imageCheckBox, 1, 2)
        grid.addWidget(self.specialLabel, 2, 0)
        grid.addWidget(self.specialLineEdit, 3, 0, 1, 3)

        input_fieldsGroupBox = QGroupBox("Set Criteria")
        input_fieldsGroupBox.setLayout(grid)

        # Arrange vertically
        center = QVBoxLayout()
        center.addLayout(label_combobox_HBoxLayout)
        center.addWidget(input_fieldsGroupBox)
        center.addWidget(self.previewLabel)
        center.addWidget(self.previewTextEdit)

        # Layout buttons
        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self.previewButton)
        buttons.addWidget(self.addButton)
        buttons.addWidget(self.clearButton)

        # add layout to the group
        center.addLayout(buttons)

        # set main layout for Search
        self.setLayout(center)

    def _properties(self):
        """ Set properties of PyQt widgets here """

        self.trackerLineEdit.setPlaceholderText("Marker")
        self.trackerLineEdit.setFrame(False)
        self.trackerLineEdit.setCompleter(self.tracker_completer)
        self.due_dateDateEdit.setDisplayFormat(self.date_format)   # ex. 14 Mar 2015
        self.due_dateDateEdit.setCalendarPopup(True)
        self.due_dateDateEdit.setCalendarWidget(self.defaultCalendar)
        self.defaultCalendar.setGridVisible(True)
        self.defaultCalendar.setDateTextFormat(QDate.currentDate(), self.currentDateFormat)
        self.specialLineEdit.setPlaceholderText("Read correspondence for further instructions")
        self.with_artworkCheckBox.setToolTip(ARTWORK_TOOLTIP)
        self.with_imageCheckBox.setToolTip(IMAGE_TOOLTIP)
        # You need this to style self.previewTextEdit
        style_document = QTextDocument()
        style_document.setDefaultStyleSheet(STYLE)
        # Apply style
        self.previewTextEdit.setDocument(style_document)
        #self.setAttribute(Qt.WA_DeleteOnClose)
        #self.setWindowModality(Qt.NonModal)

        # set default TAT values
        self.client_TAT = UN_TAT

        # TEST: see line 37
        self.selected_TAT = UN_TAT['Low/Medium']   # set default

        # For the main window
        self.setWindowTitle("Search (SIW) Template Form")
        self.setWindowIcon(QIcon(':/magnify_32.png'))

    def _readSettings(self):

        settings = QSettings("SEARCHING", "search_dialog")
        position = settings.value("position", QPoint(200, 200))
        size = settings.value("size", QSize(410, 550))
        self.move(position)
        self.resize(size)

    def _writeSettings(self):

        settings = QSettings("SEARCHING", "search_dialog")
        settings.setValue("position", self.pos())
        settings.setValue("size", self.size())

    def _connections(self):
        """ Connect every PyQt widgets here """

        # experiment starts here
        self.due_dateDateEdit.dateChanged.connect(self.on_due_dateDateEdit_dateChanged)
        self.due_dateDateEdit.dateChanged.connect(self.on_setCriteria_changed)

        self.daysSpinBox.valueChanged.connect(self.on_daysSpinBox_valueChanged)
        self.daysSpinBox.valueChanged.connect(self.on_setCriteria_changed)

        self.clientComboBox.currentIndexChanged.connect(self.on_clientComboBox_activated)
        self.clientComboBox.currentIndexChanged.connect(self.on_setCriteria_changed)

        self.importanceComboBox.currentIndexChanged.connect(self.on_importanceComboBox_activated)
        self.importanceComboBox.currentIndexChanged.connect(self.on_setCriteria_changed)

        self.with_artworkCheckBox.stateChanged.connect(self.on_setCriteria_changed)
        self.with_imageCheckBox.stateChanged.connect(self.on_setCriteria_changed)

        self.specialLineEdit.textChanged.connect(self.on_setCriteria_changed)
        # experiment ends here

        self.previewButton.clicked.connect(self.on_previewButton_clicked)
        # The generate button will only retrieve and throw data based on the input widgets
        self.addButton.clicked.connect(self.accept)
        self.clearButton.clicked.connect(self.on_clearButton_clicked)

    # TEST: event handling for self.dueDateEdit.dateChanged
    def on_due_dateDateEdit_dateChanged(self):
        """ Event handler for self.due_dateDateEdit

            return QDate
        """

        # Get any selected date when the user uses the calendar
        self.due_date = self.due_dateDateEdit.date()
        return self.due_date

    def dialog_info(self):
        """ Dialog information identifier """

        return 'Searching'

    # EVENT HANDLING starts here...
    def on_clientComboBox_activated(self):
        """ Event handler for self.clientComboBox """

        # TODO: Ok, you see a pattern here. You know what to do with this un-pythonic block of conditions!
        if self.clientComboBox.currentText() == 'GE':
            self.DEFAULT_SI = ""
            self.client_TAT = GE_TAT
            self.selected_TAT = GE_TAT[self.importanceComboBox.currentText()]
        elif self.clientComboBox.currentText() == 'Google':
            self.DEFAULT_SI = GOOGLE_DEFAULT
            self.client_TAT = GOOGLE_TAT
            self.selected_TAT = GOOGLE_TAT[self.importanceComboBox.currentText()]
        elif self.clientComboBox.currentText() == 'Unilever':
            self.DEFAULT_SI = ""
            self.client_TAT = UN_TAT
            self.selected_TAT = UN_TAT[self.importanceComboBox.currentText()]
        elif self.clientComboBox.currentText() == 'Abbott':
            self.DEFAULT_SI = ""
            self.client_TAT = ABBOTT_TAT
            self.selected_TAT = ABBOTT_TAT[self.importanceComboBox.currentText()]
        else:
            pass

    def on_importanceComboBox_activated(self):
        """ Event handler for self.importanceComboBox """

        # Get selected importance
        importance = self.importanceComboBox.currentText()

        # Check what the user choose
        if importance == 'Low/Medium':
            self.selected_TAT = self.client_TAT[importance]
        elif importance == 'Critical':
            self.selected_TAT = self.client_TAT[importance]
        else:
            print('BET: unsual - no importance selected?')

    def on_daysSpinBox_valueChanged(self):

        self.due_date = self.today.addDays(self.daysSpinBox.value())

    def on_setCriteria_changed(self):

        with_artwork = WITH_ARTWORK if self.with_artworkCheckBox.isChecked() else ""
        with_image = WITH_IMAGE if self.with_imageCheckBox.isChecked() else ""
        special = SEARCH_SPECIAL.format(self.specialLineEdit.text()) if self.specialLineEdit.text() else ""

        # Consolidate anything :)
        self.html = SEARCH_TEMPLATE.substitute(default=self.DEFAULT_SI,
                                               special=special,
                                               artwork=with_artwork,
                                               TAT=self.selected_TAT.format(self.due_date.toString(self.date_format)),
                                               image=with_image)

        # Show output
        self.previewTextEdit.setHtml(self.html.strip())

    def on_previewButton_clicked(self):
        """ Preview the user's input inside the self.previewTextEdit """
        # TODO: method to be replace as 'Copy All'

        # Check if specialLineEdit has content
        if self.specialLineEdit.text():
            self.special_ins = SEARCH_SPECIAL.format(self.specialLineEdit.text())
        else:
            self.special_ins = ''

        # Consolidate anything :)
        self.html = SEARCH_TEMPLATE.substitute(default=self.DEFAULT_SI,
                                               special=self.special_ins,
                                               artwork=self.artwork,
                                               TAT=self.selected_TAT.format(self.due_date.toString(self.date_format)),
                                               image=self.image)

        # Show output
        self.previewTextEdit.setHtml(self.html.strip())

        # Enable self.addButton
        self.addButton.setEnabled(True)

    def on_clearButton_clicked(self):
        """ Event handler for clearing text inside self.specialLineEdit and self.previewTextEdit """

        self.specialLineEdit.clear()
        self.previewTextEdit.clear()

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
