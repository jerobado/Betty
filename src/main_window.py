# Betty > src > main_window.py
# Main user interface of Betty

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from PyQt5.QtGui import (QIcon,
                         QKeySequence)
from PyQt5.QtCore import (Qt,
                          QDateTime,
                          QSettings)
from PyQt5.QtWidgets import (QMainWindow,
                             QLabel,
                             QTextEdit,
                             QAction,
                             QDockWidget,
                             QMessageBox,
                             QListView)
from resources._constants import (ABOUT,
                                  TITLE,
                                  TEMP_TEMPLATE_STORAGE_DATA,
                                  TEMP_TEMPLATE_STORAGE_LIST,
                                  TEMP_TEMPLATE_DATECREATED,
                                  TEMP_TEMPLATE_DIALOG_INFO,
                                  TEMP_TEMPLATE_SEARCH_TAT,
                                  TEMP_TEMPLATE_SEARCH_IMPORTANCE)
from resources.models import TrackerListModel
from resources import bipc_resources   # Don't remove this!

# Application settings variables
APPEND = True   # Default, any new template created will overwrite the previous one


class Betty(QMainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)
        # Resident variables
        self.todays_marker = ''
        self.model = TrackerListModel(TEMP_TEMPLATE_STORAGE_DATA)
        # Private methods
        self._widgets()
        self._properties()
        self._createActions()
        self._createMenus()
        self._createToolBars()
        self._createStatusBar()
        self._createDockWindows()
        self._connections()
        self._readSettings()

    def _widgets(self):

        # Status bar
        self.statusLabel = QLabel()
        self.mainTextEdit = QTextEdit()
        # Central Widget
        self.setCentralWidget(self.mainTextEdit)

    def _properties(self):

        # For the main window
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle(TITLE)
        self.setWindowIcon(QIcon(':/TOOLS.png'))

    def _readSettings(self):
        """ Method for retrieving Betty's position and state """

        settings = QSettings("GIPSC Core Team", "Betty")
        self.restoreGeometry(settings.value("betty_geometry"))
        self.restoreState(settings.value("betty_state", self.saveState()))

    def _writeSettings(self):
        """ Method for saving Betty's position and state """

        settings = QSettings("GIPSC Core Team", "Betty")
        settings.setValue("betty_geometry", self.saveGeometry())
        settings.setValue("betty_state", self.saveState())  # blame this line if something crashes

    def _connections(self):
        """ Connect widget signals and slots """

        self.trackerListView.clicked.connect(self.on_trackerListView_clicked)
        self.mainTextEdit.copyAvailable.connect(self.copyAction.setEnabled)
        self.mainTextEdit.copyAvailable.connect(self.cutAction.setEnabled)

    def _createActions(self):

        # Remember: when using QIcon, don't forget to update resources.qrc
        # Remember: when creating a QAction, it should have a parent

        # File menu: actions inside this menu
        self.newAction = QAction(QIcon(":/new.png"), "&New", self,
                                 shortcut=QKeySequence.New,
                                 statusTip="Create a new template",
                                 toolTip="New",
                                 triggered=self.on_newTemplate_action)
        self.exitAction = QAction(QIcon(":/quit.png"), "E&xit", self,
                                  shortcut="Ctrl+Q",
                                  statusTip="Exit the application",
                                  triggered=self.close)

        # Edit menu
        self.cutAction = QAction(QIcon(":/cut.png"), "Cu&t", self,
                                 shortcut=QKeySequence.Cut,
                                 enabled=False,
                                 statusTip="Cut to clipboard",
                                 toolTip="Cut",
                                 triggered=self.mainTextEdit.cut)
        self.copyAction = QAction(QIcon(":/copy.png"), "&Copy", self,
                                  shortcut=QKeySequence.Copy,
                                  enabled=False,
                                  statusTip="Copy to clipboard",
                                  toolTip="Copy",
                                  triggered=self.mainTextEdit.copy)
        self.pasteAction = QAction(QIcon(":/paste.png"), "&Paste", self,
                                   shortcut=QKeySequence.Paste,
                                   statusTip="Paste from clipboard",
                                   toolTip="Paste",
                                   triggered=self.mainTextEdit.paste)
        self.select_allAction = QAction(QIcon(":/select_all.png"), "Select &All", self,
                                        shortcut=QKeySequence.SelectAll,
                                        statusTip="Select all",
                                        triggered=self.mainTextEdit.selectAll)

        # Settings menu
        self.appendAction = QAction("&Append Template", self,
                                    checkable=True,
                                    statusTip="Append created template to editor",
                                    triggered=self.on_appendAction_clicked)

        # Help menu
        self.aboutAction = QAction("&About", self,
                                   statusTip="Show information about Betty",
                                   triggered=self.on_aboutAction_clicked)

    def _createMenus(self):
        """ FILE, EDIT (Cut, Copy, Paste), Format (Bold, UPPERCASE, etc., Help """

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
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.select_allAction)

        # View: Tracker
        self.viewMenu = self.menuBar().addMenu("&View")

        # Settings: Append Template
        self.settingsMenu = self.menuBar().addMenu("&Settings")
        self.settingsMenu.addAction(self.appendAction)

        # Help: About
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAction)

    def _createToolBars(self):

        # File: toolbars
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.setObjectName("fileToolBar")
        self.fileToolBar.setMovable(False)
        self.fileToolBar.addAction(self.newAction)

        # Edit: toolbars
        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.setObjectName("editToolBar")
        self.editToolBar.setMovable(False)
        self.editToolBar.addAction(self.cutAction)
        self.editToolBar.addAction(self.copyAction)
        self.editToolBar.addAction(self.pasteAction)
        self.editToolBar.addSeparator()
        self.editToolBar.addAction(self.select_allAction)

    def _createStatusBar(self):

        self.status = self.statusBar()
        self.status.addPermanentWidget(self.statusLabel)
        self.status.showMessage("Ready", 6000)

    def _createDockWindows(self):
        """ Event handler for View > Tracker """

        # Dock Widget
        self.trackerDockWidget = QDockWidget("Tracker", self)
        self.trackerDockWidget.setObjectName("trackerDockWidget")
        self.trackerDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea)

        # Add widget to be inserted inside self.trackerDockWidget
        self.trackerListView = QListView()
        self.trackerListView.resize(0, 80)
        self.trackerDockWidget.setWidget(self.trackerListView)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.trackerDockWidget)

        # Add an action, you cannot customize tracker action by using QDockWidget.toggleViewAction()
        self.viewMenu.addAction(self.trackerDockWidget.toggleViewAction())

    # SLOTS: Define BET slots here
    def on_newTemplate_action(self):
        """ Event handler for File > New """

        from src.dialogs.new import New                         # Get the New dialog for template selection
        newDialog = New(self)                                   # Initialize

        if newDialog.exec_():
            index = newDialog.templateListView.currentIndex()
            if index.row() == 0:                                # Filing
                from src.dialogs.filing import Filing           # Get the Filing template dialog
                superstar69 = Filing(self)                      # Sneaker manufactured by Adidas
                self.window_modal(superstar69)                  # Somehow modal dialogs works
            elif index.row() == 1:                              # Search (SIW)
                from src.dialogs.search import Search           # Get the Searching template dialog
                topstar77 = Search(self)                        # Sneaker manufactured by Pony Int'l
                self.window_modal(topstar77)                    # Fire In Your New Shoes - Kaskade f/ Dragonette
            else:
                # Waiting for another template to be created
                print('allstars17')

    # EVENT HANDLER: define it here
    def on_trackerListView_clicked(self):
        raw_data = self.trackerListView.currentIndex()
        row = raw_data.row()
        raw_template = TEMP_TEMPLATE_STORAGE_LIST[row]
        self.check_if_append(raw_template)
        self.setWindowTitle(' - '.join([TEMP_TEMPLATE_STORAGE_DATA[row], TITLE]))

    # UTILITIES: functional task use by the main window
    def check_if_append(self, template):
        """ Method for checking if 'Append Template' is activated by the user in the Menu bar """

        if APPEND:
            # Transmit the html template into the editor overriding any text
            self.mainTextEdit.setHtml(template)
        else:
            # Append the html template to the last line into the editor
            self.mainTextEdit.append(template)

    def add_to_storage(self, template):
        """ Method for storing generated templates """

        TEMP_TEMPLATE_STORAGE_LIST.append(template)

    def add_to_listview(self, users_marker):
        """ Method that will populate the Tracker list """

        # Add the user defined marker in the Tracker
        if users_marker:
            self.todays_marker = users_marker
            TEMP_TEMPLATE_STORAGE_DATA.append(users_marker)

        # Default marker is the current system Date & Time
        else:
            datetime_marker = QDateTime()
            self.todays_marker = datetime_marker.currentDateTime().toString('dd-MMM-yyyy hh:mm:ss')
            TEMP_TEMPLATE_STORAGE_DATA.append(self.todays_marker)      # Store the generated marker in temp list

        self.model.insertRows(len(TEMP_TEMPLATE_STORAGE_DATA), 1)      # Re-insert the list in the model
        self.trackerListView.setModel(self.model)                      # Update the model

    def add_to_windowtitle(self):
        """ Method that will set the window title based on the default (date & time) or user's marker """

        self.setWindowTitle(' - '.join([self.todays_marker, TITLE]))

    def window_modal(self, dialog):
        """ Method that accepts a dialog object for viewing """

        # Invoke the selected dialog
        if dialog.exec_():
            # Execute this statements if the user hits the 'Add' button
            if dialog.dialog_info() == 'Searching':
                tat = dialog.today.daysTo(dialog.due_date)
                importance = dialog.importanceComboBox.currentText()
                TEMP_TEMPLATE_SEARCH_TAT.append(tat)
                TEMP_TEMPLATE_SEARCH_IMPORTANCE.append(importance)
            else:
                # We append 'None' as a dummy value on these containers to keep the length in sync with the Tracker list
                TEMP_TEMPLATE_SEARCH_TAT.append(None)
                TEMP_TEMPLATE_SEARCH_IMPORTANCE.append(None)

            TEMP_TEMPLATE_DATECREATED.append(QDateTime.currentDateTime().toString('dd-MMM-yyyy hh:mm:ss'))
            TEMP_TEMPLATE_DIALOG_INFO.append(dialog.dialog_info())      # Storage for dialog information used
            generated_template = dialog.previewTextEdit.toHtml()        # Retrieve any text this widget in HTML format
            self.add_to_listview(dialog.trackerLineEdit.text())         # Populate the Tracker
            self.add_to_storage(generated_template)                     # Populate the temporary storage
            self.check_if_append(generated_template)                    # Appending?
            self.add_to_windowtitle()                                   # Set the window title
            self.status.showMessage('New {0} template added'.format(dialog.dialog_info()), 6000)

    # MENU ACTIONS: define slots here for menu
    def on_aboutAction_clicked(self):
        """ Event handler for Help > About"""

        QMessageBox.about(self, "About Betty", ABOUT)

    def on_appendAction_clicked(self):

        # Default value for 'Append Template' is False
        global APPEND
        APPEND = False if self.appendAction.isChecked() else True

    # REUSE: only re-write QMainWindow's resident functions here
    def closeEvent(self, event):

        # Get Betty's last state before totally closing
        self._writeSettings()
