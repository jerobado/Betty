# Create GUI here

import sys

from string import Template

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QDate, Qt

import bipc_resources

APP = QApplication(sys.argv)

SPECIAL_INS = "<div><p><b>{}</b></p></div>"
WITH_ARTWORK = "<div><p>Artwork attached to illustrate how the mark will appear on pack.</p></div>"
WITH_IMAGE = "<div><p>The trade mark to be searched is as shown in the attached image file.</p></div>"
# all client's except GE
MEDIUM_TAT = """
    <div><p><b>DEADLINE: {}.</b> Please provide your search report ON or BEFORE the specified deadline. \
    If the due date falls on a weekend, holiday or non-working day, please send us your search \
    analysis before then.</p></div>"""
CRITICAL_TAT = """
    <div><p><b>DEADLINE: URGENT, {}.</b> Please provide your search report ON or BEFORE the specified deadline. \
    If the due date falls on a weekend, holiday or non-working day, please send us your search \
    analysis before then.</p></div>"""
# GE TAT
GE_MEDIUM_TAT = """
    <div><p><b>DEADLINE: {}.</b> Please provide your search report ON or BEFORE the specified deadline. \
    If the due date falls on a weekend, holiday or non-working day, please send us your search \
    analysis on the next business day.</p></div>"""
GE_CRITICAL_TAT = """
    <div><p><b>DEADLINE: EXPEDITED {}.</b> Please provide your search report ON or BEFORE the specified deadline. \
    If the due date falls on a weekend, holiday or non-working day, please send us your search \
    analysis on the next business day.</p></div>"""


TEMPLATE = Template("$special $artwork $TAT $image")

STYLE = """
    div {
        font-family: "Arial";
        font-size: 10pt;
    }
    """
WORKTYPE = ['Filing', 'Search (SIW)']


# initial design for our application
class BIPCTemplateGUI(QDialog):

    def __init__(self, parent=None):
        super(BIPCTemplateGUI, self).__init__(parent)
        # resident variables
        self.date_format = 'd MMM yyyy'
        self.selected_TAT = ''
        self.artwork = ''
        self.image = ''
        self.special_ins = ''

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

        center = QVBoxLayout()
        center.addLayout(label_combobox_HBoxLayout)
        center.addWidget(input_fieldsGroupBox)

        # add widgets for output
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

        # set main layout for BIPCTemplateGUI
        self.setLayout(center)

    def _properties(self):
        """ Set properties of PyQt widgets here """

        self.due_dateDateEdit.setDisplayFormat(self.date_format)   # ex. 14 Mar 2015
        self.due_dateDateEdit.setCalendarPopup(True)
        self.special_instructionLineEdit.setPlaceholderText("Input test string here...")
        self.with_artworkCheckBox.setToolTip("Hello artwork tooltip?")
        self.with_imageCheckBox.setToolTip("i can do that too!")
        # you need this to style templateTextEdit
        style_document = QTextDocument()
        style_document.setDefaultStyleSheet(STYLE)
        # apply style
        self.templateTextEdit.setDocument(style_document)

        # Default values:
        self.selected_TAT = MEDIUM_TAT

        self.setWindowTitle("Search (SIW) Template | Testing")
        self.resize(500, 350)  # width, height

    def _connections(self):
        """ Connect every PyQt widgets here """

        self.clientComboBox.activated.connect(self.on_clientComboBox_activated)
        self.importanceComboBox.activated.connect(self.on_importanceComboBox_activated)
        self.with_artworkCheckBox.stateChanged.connect(self.on_with_artworkCheckBox_stateChanged)
        self.with_imageCheckBox.stateChanged.connect(self.on_with_imageCheckBox_stateChanged)
        self.previewButton.clicked.connect(self.on_previewButton_clicked)
        self.templateTextEdit.textChanged.connect(self.on_templateTextEdit_textChanged)
        # the generate button will only retrieve and throw data based on the input widgets
        self.generateButton.clicked.connect(self.accept)
        self.clearButton.clicked.connect(self.on_clearButton_clicked)

    # EVENT HANDLING starts here...
    def on_clientComboBox_activated(self):
        """ Event handler for self.clientComboBox """




    def on_importanceComboBox_activated(self):
        """ Event handler for self.importanceComboBox """

        if self.importanceComboBox.currentText() == 'Low/Medium':
            self.selected_TAT = MEDIUM_TAT
            print('medium')
        elif self.importanceComboBox.currentText() == 'Critical':
            self.selected_TAT = CRITICAL_TAT
        else:
            print('Amazing!')

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

    def on_templateTextEdit_textChanged(self):

        print("Someone wrote something on the preview box")

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

        self.special_instructionLineEdit.clear()   # clean any text inside this widget
        self.templateTextEdit.clear()   # same here

    # TODO: make use of this idle function in the near future :)
    def exchange_data(self):
        """ Event handler for testLineEdit """

        # if the user directly inserted something on the previewTextEdit, copy all text
        #self.templateTextEdit.selectAll()
        pass


# my second GUI design for this application (trying to mimic e-Docs)
class BETWindow(QMainWindow):
    sequenceNumber = 0
    windowList = []

    def __init__(self, parent=None):
        super(BETWindow, self).__init__(parent)

        self._widgets()
        #self._layout()
        self._properties()
        #self._connections()

        self._createActions()
        self._createMenus()
        self._createToolBars()
        self._createStatusBar()

    def _widgets(self):

        self.statusLabel = QLabel()
        self.testTextEdit = QTextEdit()
        #self.testTextEdit.setMinimumSize(200, 200)
        #self.testTextEdit.setAlignment(Qt.AlignCenter)
        #self.testTextEdit.setContextMenuPolicy(Qt.ActionsContextMenu)

        # Dock Widget
        #self.testDocking = QDockWidget("Sample", self)
        #self.testDocking.setObjectName("SampleDockWidget")
        #self.testDocking.setAllowedAreas(Qt.AllDockWidgetAreas)
        # add widget to be inserted inside self.testDocking
        #self.testListWidget = QListWidget()
        #self.testDocking.setWidget(self.testListWidget)
        #self.addDockWidget(Qt.RightDockWidgetArea, self.testDocking)

        # Central Widget
        self.setCentralWidget(self.testTextEdit)

    def _properties(self):
        """ Main Window properties """

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.resize(600, 350)   # width, height
        # set window center screen
        self.screenMainSize = QDesktopWidget().screenGeometry()
        print(self.screenMainSize)
        BETsize = self.geometry()
        # horizontal position = screenwidth - windowwidth /2
        hpos = (self.screenMainSize.width() - BETsize.width()) / 2
        vpos = (self.screenMainSize.height() - BETsize.height()) / 2
        self.move(hpos, vpos)
        print(BETsize)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint |
                            Qt.WindowCloseButtonHint)

    def _createActions(self):

        # Remember: when creating an QAction, it should have a parent
        # File menu: actions's inside this menu
        self.newAction = QAction(QIcon(":/new.png"), "&New", self, shortcut=QKeySequence.New,
                                 statusTip="Create a new Template", toolTip="New", triggered=self.newTemplate)
        self.exitAction = QAction("E&xit", self, shortcut="Ctrl+Q",
                                  statusTip="Exit the application", triggered=self.close)

        # TODO: add new "triggered" attributes and slots/methods, see sample above
        # Edit menu: actions inside this menu
        self.cutAction = QAction(QIcon(":/scissors.png"), "Cu&t", self, shortcut=QKeySequence.Cut,
                                statusTip="Cut to clipboard", toolTip="Cut")
        self.copyAction = QAction(QIcon(":/copy.png"), "&Copy", self, shortcut=QKeySequence.Copy,
                                  statusTip="Copy to clipboard", toolTip="Copy")
        self.pasteAction = QAction(QIcon(":/paste.png"), "&Paste", self, shortcut=QKeySequence.Paste,
                                   statusTip="Paste from clipboard", toolTip="Paste")

    def _createMenus(self):

        # FILE, Edit (Cut, Copy, Paste), Format (Bold, UPPERCASE, etc., Help

        # File: application's commands
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)

        # Edit: undo, redo, cut, copy or paste
        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.cutAction)
        self.editMenu.addAction(self.copyAction)
        self.editMenu.addAction(self.pasteAction)

    def _createToolBars(self):

        # File: toolbars
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newAction)

        # Edit: toolbars
        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.cutAction)
        self.editToolBar.addAction(self.copyAction)
        self.editToolBar.addAction(self.pasteAction)


    def _createStatusBar(self):

        self.status = self.statusBar()
        self.status.addPermanentWidget(self.statusLabel)
        self.status.showMessage("Ready", 6000)

    def newTemplate(self):

        newWindow = NewTemplateDialog(self)
        # BETWindow.windowList.append(newWindow)
        newWindow.move(self.x() + 40, self.y() + 40)

        if newWindow.exec_():
            if newWindow.templateListWidget.currentItem().text() == "Search (SIW)":
                print("CODING: show dialog for creating a search template")
                newTemplateDialog = BIPCTemplateGUI(self)
                if newTemplateDialog.exec_():
                    # if the user hit 'Generate', populate testTextEdit in BETWindow
                    superstar = newTemplateDialog.templateTextEdit.toHtml() # get any text inside the preview QTextEdit
                    self.testTextEdit.setHtml(superstar)   # transmit the data to the main window
                else:
                    print("Someone hit Esc")
            elif newWindow.templateListWidget.currentItem().text() == "Filing":
                print("CODING: show dialog for creating a filing template")
            else:
                print("Amazing")
        else:
            print("Cancel")


# Dialogs starts here...
class NewTemplateDialog(QDialog):

    def __init__(self, parent=None):
        super(NewTemplateDialog, self).__init__(parent)

        self._widgets()
        self._layout()
        self._properties()
        self._connections()

    def _widgets(self):

        self.templateLabel = QLabel("Template:")
        self.templateListWidget = QListWidget()
        self.templateListWidget.addItems(WORKTYPE)
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

        # TODO: please fix this, make the this dialog center
        # self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Add new Template")
        self.resize(250, 100)
        # set window center screen
        # screen = QDesktopWidget().screenGeometry()
        # print(screen)
        BETsize = self.geometry()
        # horizontal position = screenwidth - windowwidth /2
        hpos = (600 - BETsize.width()) / 2
        vpos = (350 - BETsize.height()) / 2
        self.move(hpos, vpos)

    def _connections(self):

        self.templateListWidget.itemDoubleClicked.connect(self.accept)
        self.createPushButton.clicked.connect(self.accept)
        self.cancelPushButton.clicked.connect(self.reject)

    def on_test_slot(self):

        # TEST: open a new template
        print("TEST: slot")
        if self.templateListWidget.currentItem().text() == "Search (SIW)":
            dialog = BIPCTemplateGUI()
            if dialog.exec_():
                print(self.templateListWidget.currentItem().text())
            else:
                print("Do the recap!")
        elif self.templateListWidget.currentItem().text() == "Filing":
            print(self.templateListWidget.currentItem().text())
        else:
            print("Matulog ka na!")