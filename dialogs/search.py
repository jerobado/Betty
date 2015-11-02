# BET > dialogs > search.py

__author__ = 'Jero'

from PyQt5.QtWidgets import (QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QDateEdit, QTextEdit, QSpinBox,
                             QGridLayout, QDialog, QHBoxLayout, QVBoxLayout, QGroupBox, QCalendarWidget)
from PyQt5.QtGui import QTextDocument, QTextCharFormat
from PyQt5.QtCore import QDate

from resources.constants import (SPECIAL_INS,
                                 WITH_ARTWORK,
                                 WITH_IMAGE,
                                 UN_TAT,
                                 GE_TAT,
                                 TEMPLATE,
                                 STYLE)


# Main dialog for searching template
class Search(QDialog):

    def __init__(self, parent=None):
        super(Search, self).__init__(parent)
        # resident variables
        self.date_format = 'd MMM yyyy'
        self.selected_TAT = ''
        self.artwork = ''
        self.image = ''
        self.special_ins = ''
        self.client_TAT = ''

        # resident functions
        self._widgets()
        self._layout()
        self._properties()
        self._connections()

    def _widgets(self):
        """ Create new PyQt widgets here """

        self.clientLabel = QLabel("Client:")
        self.clientComboBox = QComboBox()
        self.clientComboBox.insertItem(0, "GE")
        self.clientComboBox.insertItem(1, "Unilever")
        self.clientComboBox.setCurrentIndex(1)
        self.due_dateLabel = QLabel("Due Date:")
        self.importanceLabel = QLabel("Importance:")
        self.special_instructionLabel = QLabel("Special Instruction:")
        self.due_dateDateEdit = QDateEdit(QDate.currentDate())  # initialize by current date
        self.defaultCalender = QCalendarWidget()
        self.currentDateFormat = QTextCharFormat()
        self.currentDateFormat.setFontWeight(75)
        self.daysSpinBox = QSpinBox()
        self.importanceComboBox = QComboBox()  # provide a list when using this widget for it's content
        self.importanceComboBox.insertItem(0, "Low/Medium")
        self.importanceComboBox.insertItem(1, "Critical")
        self.importanceComboBox.setCurrentIndex(0)
        self.with_artworkCheckBox = QCheckBox("with artwork")
        self.with_imageCheckBox = QCheckBox("with image")
        self.special_instructionLineEdit = QLineEdit()
        self.previewLabel = QLabel("Preview:")
        self.templateTextEdit = QTextEdit()
        self.previewButton = QPushButton("Pr&eview")
        self.generateButton = QPushButton("&Generate")
        self.clearButton = QPushButton("&Clear")

    def _layout(self):
        """ Set and arrange PyQt widgets here """

        # clientLabel + clientComboBox
        label_combobox_HBoxLayout = QHBoxLayout()
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
        grid.addLayout(label_dateEdit_tandem, 0, 0)  # affected
        grid.addWidget(self.with_artworkCheckBox, 0, 2)
        grid.addLayout(label_comboBox_tandem, 1, 0)  # affected
        grid.addWidget(self.with_imageCheckBox, 1, 2)
        grid.addWidget(self.special_instructionLabel, 2, 0)
        grid.addWidget(self.special_instructionLineEdit, 3, 0, 1, 3)

        input_fieldsGroupBox = QGroupBox("Input Fields")
        input_fieldsGroupBox.setLayout(grid)

        # arrange vertically
        center = QVBoxLayout()
        center.addLayout(label_combobox_HBoxLayout)
        center.addWidget(input_fieldsGroupBox)
        center.addWidget(self.previewLabel)
        center.addWidget(self.templateTextEdit)

        # layout buttons
        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self.previewButton)
        buttons.addWidget(self.generateButton)
        buttons.addWidget(self.clearButton)

        # add layout to the group
        center.addLayout(buttons)

        # set main layout for Search
        self.setLayout(center)

    def _properties(self):
        """ Set properties of PyQt widgets here """

        self.due_dateDateEdit.setDisplayFormat(self.date_format)   # ex. 14 Mar 2015
        self.due_dateDateEdit.setCalendarPopup(True)
        self.due_dateDateEdit.setCalendarWidget(self.defaultCalender)
        self.defaultCalender.setGridVisible(True)
        self.defaultCalender.setDateTextFormat(QDate.currentDate(), self.currentDateFormat)
        self.special_instructionLineEdit.setPlaceholderText("Read correspondence for further instructions")
        # TODO: search somewhere in GQR wherein you can apply something informative on this tooltip
        self.with_artworkCheckBox.setToolTip("Hello artwork tooltip?")
        self.with_imageCheckBox.setToolTip("i can do that too!")
        # you need this to style templateTextEdit
        style_document = QTextDocument()
        style_document.setDefaultStyleSheet(STYLE)
        # apply style
        self.templateTextEdit.setDocument(style_document)

        # set default TAT values:
        #self.selected_TAT = MEDIUM_TAT
        self.client_TAT = UN_TAT

        # TEST: see line 37
        self.selected_TAT = UN_TAT['Low/Medium']   # set default

        self.setWindowTitle("Search (SIW) Template | Testing")
        self.resize(410, 550)  # width, height

    def _connections(self):
        """ Connect every PyQt widgets here """

        self.clientComboBox.activated.connect(self.on_clientComboBox_activated)
        self.importanceComboBox.activated.connect(self.on_importanceComboBox_activated)
        self.with_artworkCheckBox.stateChanged.connect(self.on_with_artworkCheckBox_stateChanged)
        self.with_imageCheckBox.stateChanged.connect(self.on_with_imageCheckBox_stateChanged)
        self.previewButton.clicked.connect(self.on_previewButton_clicked)
        # the generate button will only retrieve and throw data based on the input widgets
        self.generateButton.clicked.connect(self.accept)
        self.clearButton.clicked.connect(self.on_clearButton_clicked)

    # EVENT HANDLING starts here...
    def on_clientComboBox_activated(self):
        """ Event handler for self.clientComboBox """

        # TODO: i'm not satisfied with this code below but somehow it works, make this appealing in the near future ^^,
        print("[BET]: You selected", self.clientComboBox.currentText())
        if self.clientComboBox.currentText() == 'GE':
            self.client_TAT = GE_TAT
            self.selected_TAT = GE_TAT[self.importanceComboBox.currentText()]
        elif self.clientComboBox.currentText() == 'Unilever':
            self.client_TAT = UN_TAT
            self.selected_TAT = UN_TAT[self.importanceComboBox.currentText()]
        else:
            print("#edw")

    def on_importanceComboBox_activated(self):
        """ Event handler for self.importanceComboBox """

        # get selected importance
        importance = self.importanceComboBox.currentText()

        # check what the user chose
        if importance == 'Low/Medium':
            self.selected_TAT = self.client_TAT[importance]
        elif importance == 'Critical':
            self.selected_TAT = self.client_TAT[importance]
        else:
            print('BET: unsual - no importance selected?')

    def on_with_artworkCheckBox_stateChanged(self):
        """ Event handler for with_artworkCheckBox """

        if self.with_artworkCheckBox.isChecked():
            self.artwork = WITH_ARTWORK
        else:
            self.artwork = ''

    def on_with_imageCheckBox_stateChanged(self):
        """ Event handler for with_imageCheckBox """

        if self.with_imageCheckBox.isChecked():
            self.image = WITH_IMAGE
        else:
            self.image = ''

    def on_previewButton_clicked(self):
        """ Preview the user's input inside the previewTextEdit """

        # get date selected
        due_date = self.due_dateDateEdit.date()
        # check if special_instructionLineEdit has content
        if self.special_instructionLineEdit.text():
            self.special_ins = SPECIAL_INS.format(self.special_instructionLineEdit.text())
        else:
            self.special_ins = ''
        # consolidate anything :)
        self.html = TEMPLATE.substitute(special=self.special_ins,
                                        artwork=self.artwork,
                                        TAT=self.selected_TAT.format(due_date.toString(self.date_format)),
                                        image=self.image)
        # show output
        self.templateTextEdit.setHtml(self.html.strip())

    def on_clearButton_clicked(self):
        """ Event handler for clearing text inside self.special_instructionLineEdit and self.templateTextEdit """

        self.special_instructionLineEdit.clear()    # clean any text inside this widget
        self.templateTextEdit.clear()               # same here
