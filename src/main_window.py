# Project-BET > src > main_window.py
# The main UI of Betty

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from PyQt5.QtGui import (QIcon,
                         QKeySequence)

from PyQt5.QtCore import (Qt,
                          QDateTime,
                          QSettings,
                          QPoint,
                          QSize)

from PyQt5.QtWidgets import (QMainWindow,
                             QLabel,
                             QTextEdit,
                             QAction,
                             QDockWidget,
                             QMessageBox,
                             QListView)

from resources import bipc_resources   # Don't remove this!

from resources.constants import (ABOUT,
                                 TITLE,
                                 TEMP_DIALOG_INFO)

from resources.models import TrackerListModel

# Application settings variables
APPEND = True   # Default, any new template created will overwrite the previous one


# Main window for our application
class Betty(QMainWindow):

    def __init__(self, parent=None):
        super(Betty, self).__init__(parent)

        # Resident variables
        self.todays_marker = ''
        self.TEMP_TEMPLATE_STORAGE_LIST = []    # template holder in HTML format
        self.TEMP_TEMPLATE_STORAGE_DATA = []    # tracker list holder
        self.model = TrackerListModel(self.TEMP_TEMPLATE_STORAGE_DATA)

        self._widgets()
        self._properties()
        self._readSettings()

        self._createActions()
        self._createMenus()
        self._createToolBars()
        self._createStatusBar()
        self._createDockWindows()

        self._connections()

    def _widgets(self):

        self.statusLabel = QLabel()
        self.testTextEdit = QTextEdit()

        # Central Widget
        self.setCentralWidget(self.testTextEdit)

    def _properties(self):
        """ Main Window properties """

        # For the main window
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle(TITLE)
        self.setWindowIcon(QIcon(':/TOOLS.png'))

    def _readSettings(self):
        settings = QSettings("GIPSC Core Team", "Betty")
        position = settings.value("position", QPoint(200, 600))
        size = settings.value("size", QSize(700, 350))  # width, height
        self.move(position)
        self.resize(size)

    def _writeSettings(self):
        settings = QSettings("GIPSC Core Team", "Betty")
        settings.setValue("position", self.pos())
        settings.setValue("size", self.size())

    def _connections(self):
        """ Connect widget signals and slots """

        self.trackerListView.clicked.connect(self.on_trackerListView_clicked)
        self.testTextEdit.copyAvailable.connect(self.copyAction.setEnabled)
        self.testTextEdit.copyAvailable.connect(self.cutAction.setEnabled)

    def _createActions(self):

        # TODO: implement a good shortcut system when navigating the application
        # Remember: when using QIcon, don't forget to update resources.qrc
        # Remember: when creating a QAction, it should have a parent
        # File menu: actions inside this menu
        self.newAction = QAction(QIcon(":/new.png"), "&New", self,
                                 shortcut=QKeySequence.New,
                                 statusTip="Create a new template",
                                 toolTip="New",
                                 triggered=self.on_newTemplate_action)
        #self.settingsAction = QAction(QIcon(":/settings.png"), "Se&ttings", self,
        #       shortcut="Ctrl+Alt+S",
        #       statusTip="Edit application settings",
        #       triggered=self.on_settings_action)
        self.exitAction = QAction(QIcon(":/quit.png"), "E&xit", self,
                                  shortcut="Ctrl+Q",
                                  statusTip="Exit the application",
                                  triggered=self.close)

        # Edit menu: actions inside this menu
        self.cutAction = QAction(QIcon(":/cut.png"), "Cu&t", self,
                                 shortcut=QKeySequence.Cut,
                                 enabled=False,
                                 statusTip="Cut to clipboard",
                                 toolTip="Cut",
                                 triggered=self.testTextEdit.cut)
        self.copyAction = QAction(QIcon(":/copy.png"), "&Copy", self,
                                  shortcut=QKeySequence.Copy,
                                  enabled=False,
                                  statusTip="Copy to clipboard",
                                  toolTip="Copy",
                                  triggered=self.testTextEdit.copy)
        self.pasteAction = QAction(QIcon(":/paste.png"), "&Paste", self,
                                   shortcut=QKeySequence.Paste,
                                   statusTip="Paste from clipboard",
                                   toolTip="Paste",
                                   triggered=self.testTextEdit.paste)
        self.select_allAction = QAction(QIcon(":/select_all.png"), "Select &All", self,
                                        shortcut=QKeySequence.SelectAll,
                                        statusTip="Select all",
                                        triggered=self.testTextEdit.selectAll)

        # Settings: testing a checkable action inside a menu
        self.appendAction = QAction("&Append Template", self,
                                    checkable=True,
                                    statusTip="Append created template to editor",
                                    triggered=self.on_appendAction_clicked)
        self.continuousAction = QAction("Add &Continuously", self,
                                        checkable = True,
                                        statusTip="Add template without interruption",
                                        triggered=self.on_continuousAction_clicked)

        # Help: actions inside this menu
        self.aboutAction = QAction("&About", self,
                                   statusTip="Show information about Betty",
                                   triggered=self.on_aboutAction_clicked)

    def _createMenus(self):
        """ FILE, EDIT (Cut, Copy, Paste), Format (Bold, UPPERCASE, etc., Help """

        # File: application's commands
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addSeparator()
        #self.fileMenu.addAction(self.settingsAction)
        #self.fileMenu.addSeparator()
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

        # Settings: check...
        self.settingsMenu = self.menuBar().addMenu("&Settings")
        self.settingsMenu.addAction(self.appendAction)
        #self.settingsMenu.addAction(self.continuousAction)

        # Help: About
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAction)

    def _createToolBars(self):

        # File: toolbars
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.setMovable(False)
        self.fileToolBar.addAction(self.newAction)

        # Edit: toolbars
        self.editToolBar = self.addToolBar("Edit")
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

        # TODO: add an icon identifier for Searching and Filing
        # Dock Widget
        self.tracker_dock = QDockWidget("Tracker", self)
        self.tracker_dock.setObjectName("Tracker")
        self.tracker_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        # Add widget to be inserted inside self.tracker_dock
        self.trackerListView = QListView()
        self.tracker_dock.setWidget(self.trackerListView)
        self.addDockWidget(Qt.RightDockWidgetArea, self.tracker_dock)

        # Add an action, you cannot customize tracker action by using QDockWidget.toggleViewAction()
        self.viewMenu.addAction(self.tracker_dock.toggleViewAction())
        #logging.info("[BET]: Tracker activated")

    # SLOTS: Define BET slots here
    def on_newTemplate_action(self):
        """ Event handler for File > New """

        from src.dialogs.new import New                     # Get the New dialog for template selection
        newDialog = New(self)                               # Initialize

        if newDialog.exec_():
            index = newDialog.templateListView.currentIndex()
            if index.row() == 0:                            # Filing
                from src.dialogs.filing import Filing       # Get the Filing template dialog
                superstar69 = Filing(self)                  # Sneaker manufactured by Adidas
                self.window_modal(superstar69)              # Somehow modal dialogs works
            elif index.row() == 1:                          # Search (SIW)
                from src.dialogs.search import Search       # Get the Searching template dialog
                topstar77 = Search(self)                    # Sneaker manufactured by Pony Int'l
                self.window_modal(topstar77)                # Fire In Your New Shoes - Kaskade f/ Dragonette
            else:
                # Waiting for another template to be created
                print('allstars17')

    # EVENT HANDLER: define it here
    def on_trackerListView_clicked(self):
        raw_data = self.trackerListView.currentIndex()
        row = raw_data.row()
        raw_template = self.TEMP_TEMPLATE_STORAGE_LIST[row]
        self.check_if_append(raw_template)
        self.setWindowTitle(' - '.join([self.TEMP_TEMPLATE_STORAGE_DATA[row], TITLE]))

    # UTILITIES: functional task use by BET window
    def check_if_append(self, template):
        """ Method for checking if 'Append Template' is activated by the user in the Menu bar """

        if APPEND:
            # Transmit the html template into the editor overriding any text
            self.testTextEdit.setHtml(template)
        else:
            # Append the html template to the last line into the editor
            self.testTextEdit.append(template)

    def add_to_storage(self, template):
        """ Method for storing generated templates """

        self.TEMP_TEMPLATE_STORAGE_LIST.append(template)

    def add_to_listview(self, users_marker):
        """ Method that will populate the Tracker list """

        # Add the user defined marker in the Tracker
        if users_marker:
            self.todays_marker = users_marker
            self.TEMP_TEMPLATE_STORAGE_DATA.append(users_marker)

        # Default marker is the current system Date & Time
        else:
            datetime_marker = QDateTime()
            self.todays_marker = datetime_marker.currentDateTime().toString('dd-MMM-yyyy hh:mm:ss')
            self.TEMP_TEMPLATE_STORAGE_DATA.append(self.todays_marker)      # Store the generated marker in temp list

        self.model.insertRows(len(self.TEMP_TEMPLATE_STORAGE_DATA), 1)      # Re-insert the list in the model
        self.trackerListView.setModel(self.model)                           # Update the model

    def add_to_windowtitle(self):
        """ Method that will set the window title based on the default (date & time) or user's marker """

        self.setWindowTitle(' - '.join([self.todays_marker, TITLE]))

    def window_modal(self, dialog):
        """ Method that accepts a dialog object for viewing """

        # Invoke the selected dialog
        if dialog.exec_():
            # Execute this statements if the user hits the 'Add' button
            TEMP_DIALOG_INFO.append(dialog.dialog_info)                 # Storage for dialog information used
            generated_template = dialog.previewTextEdit.toHtml()        # Retrieve any text this widget in html format
            self.add_to_listview(dialog.trackerLineEdit.text())         # Populate the Tracker
            self.add_to_storage(generated_template)                     # Populate the temporary storage
            self.check_if_append(generated_template)                    # Appending?
            self.add_to_windowtitle()                                   # Set the window title
            self.status.showMessage('New {} template added'.format(dialog.dialog_info), 6000)

    # TODO: this part here is terribly a bleeding one
    def non_modal(self, dialog):
        dialog.show()
        #dialog.setAttribute(Qt.WA_DeleteOnClose)
        dialog.setWindowModality(Qt.NonModal)
        # if the user hit 'Add' button, populate self.testTextEdit in BET
        # get any text inside the preview QTextEdit
        # this will return HTML to superstar
        #superstar = dialog.previewTextEdit.toHtml()
        print("non-modal: waiting")
        #self.add_to_tracker(dialog.trackerLineEdit.text())
        #self.add_to_storage(superstar)
        # TODO: you are stuck here, kaya matulog ka na!
        # trying to add a status message in the main form
        #self.status.showMessage("New Search template added", 6000)

    # MENU ACTIONS: define slots here for menu
    def on_aboutAction_clicked(self):

        QMessageBox.about(self, "About Betty", ABOUT)

    # TODO: this function has no meaning while Betty is currently running
    def on_settings_action(self):
        """ Event handler for File > Settings """

        from src.dialogs.settings import Settings

        dialog = Settings()
        if dialog.exec_():
            if dialog.appendCheckBox.isChecked():
                global APPEND
                APPEND = False

    def on_appendAction_clicked(self):  # much better

        global APPEND

        if self.appendAction.isChecked():
            APPEND = False
        else:
            APPEND = True

    def on_continuousAction_clicked(self):
        #logging.info("[BET]: forms will not close unless explicitly killed :)")
        pass

    # REUSE: only re-write QMainWindow's resident functions here
    def closeEvent(self, event):
        # Get the last applications last state before totally closing
        self._writeSettings()
        #logging.info("~~~~~~~~~~~~~~~~~~~~ BETTY TERMINATED ~~~~~~~~~~~~~~~~~~~")