"""
    Outline of classes.
    * BET(QMainWindow)
        + New(QDialog) -> moved to dialogs/new.py
    * Filing(QDialog) -> moved to dialogs/filing.py
    * Search(QDialog) -> moved to dialogs/search.py
"""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

#import logging

from PyQt5.QtCore import Qt, QDateTime, QSettings, QPoint, QSize, QAbstractListModel
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (QMainWindow, QLabel, QTextEdit, QAction, QDockWidget, QListWidget,
                             QAbstractItemView, QMessageBox, QListView)
from resources import bipc_resources   # Don't remove this!
from resources.constants import ABOUT, TITLE

# Application settings variables
APPEND = True   # default, any new template created will overwrite the previous one


# Main window for our application
class BET(QMainWindow):

    def __init__(self, version, parent=None):
        super(BET, self).__init__(parent)

        # resident variables
        self.__version__ = version
        self.sarah = ''
        self.TEMP_TEMPLATE_STORAGE_LIST = []
        self.TEMP_TEMPLATE_STORAGE_DATA = []

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
        #self.setWindowIcon(QIcon('images/logo_128.png'))

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

        self.trackerListWidget.itemDoubleClicked.connect(self.on_trackerListWidget_itemDoubleClicked)
        self.testTextEdit.copyAvailable.connect(self.copyAction.setEnabled)
        self.testTextEdit.copyAvailable.connect(self.cutAction.setEnabled)

    def _createActions(self):

        # TODO: implement a good shortcut system when navigating your application
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
        self.trackerListWidget = QListWidget()
        self.trackerListWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.tracker_dock.setWidget(self.trackerListWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.tracker_dock)

        # Add an action, you cannot customize tracker action by using QDockWidget.toggleViewAction()
        self.viewMenu.addAction(self.tracker_dock.toggleViewAction())
        #logging.info("[BET]: Tracker activated")

    # SLOTS: Define BET slots here
    def on_newTemplate_action(self):
        """ Event handler for File > New """

        from src.dialogs.new import New

        #logging.info("[BET]: Selecting new template")

        newWindow = New(self)

        if newWindow.exec_():
            index = newWindow.templateListView.currentIndex()
            if index.row() == 1:    # Search (SIW)
            #if newWindow.templateListWidget.currentItem().text() == "Search (SIW)":
                #logging.info("[BET]: Search template selected")
                # show Search template
                from src.dialogs.search import Search

                searchDialog = Search(self)

                #self.non_modal(searchDialog)
                self.window_modal(searchDialog)
            elif index.row() == 0:  # Filing
            #elif newWindow.templateListWidget.currentItem().text() == "Filing":
                # Show filing template dialog here
                from src.dialogs.filing import Filing

                filingDialog = Filing(self)
                #logging.info("[BET]: Filing template selected")  # BET prompt
                if filingDialog.exec_():  # this will show the dialog first
                    superstar = filingDialog.previewTextEdit.toHtml()
                    self.add_to_tracker(filingDialog.trackerLineEdit.text())
                    self.add_to_storage(superstar)
                    self.check_if_append(superstar)
                    self.add_to_windowtitle()
                    self.status.showMessage("New Filing template added", 6000)
            else:
                #logging.warning("[BET]: Unusual, no template selected?")
                pass

    # EVENT HANDLER: define it here
    def on_trackerListWidget_itemDoubleClicked(self):

        selected_template_html = self.TEMP_TEMPLATE_STORAGE_LIST[self.trackerListWidget.currentRow()]
        self.check_if_append(selected_template_html)
        self.setWindowTitle(' - '.join([self.trackerListWidget.currentItem().text(), TITLE]))

    # UTILITIES: functional task use by BET window
    def check_if_append(self, superstar):

        # Check if Appending is activated
        if APPEND:
            # Transmit the data to the main window overriding any text
            self.testTextEdit.setHtml(superstar)
        else:
            self.testTextEdit.append(superstar)

    def add_to_tracker(self, users_marker):
        # TODO: define a View here

        self.sarah = users_marker
        # Check if the user put something on the marker
        if self.sarah:
            # Populate the tracker widget
            self.trackerListWidget.addItem(self.sarah)
        else:
            # Set the default market to current date and time
            default_marker = QDateTime()
            marker_of_the_day = default_marker.currentDateTime()
            self.sarah = marker_of_the_day.toString('dd-MMM-yyyy hh:mm:ss')
            self.trackerListWidget.addItem(self.sarah)

    def add_to_storage(self, template):
        # TODO: define a data model here

        self.TEMP_TEMPLATE_STORAGE_LIST.append(template)

    def add_to_windowtitle(self):
        """ This will set the window title based on the custom marker set by the user """

        self.setWindowTitle(' - '.join([self.sarah, TITLE]))

    def window_modal(self, dialog):
        if dialog.exec_():  # this will show the dialog first
            # if the user hit 'Add' button, populate self.testTextEdit in BET
            # get any text inside the preview QTextEdit
            # this will return HTML to superstar
            superstar = dialog.templateTextEdit.toHtml()
            self.add_to_tracker(dialog.trackerLineEdit.text())
            self.add_to_storage(superstar)
            self.check_if_append(superstar)
            self.add_to_windowtitle()
            # trying to add a status message in the main form
            self.status.showMessage("New Search template added", 6000)

    # TODO: this part here is terribly a bleeding one
    def non_modal(self, dialog):
        dialog.show()
        #dialog.setAttribute(Qt.WA_DeleteOnClose)
        dialog.setWindowModality(Qt.NonModal)
        # if the user hit 'Add' button, populate self.testTextEdit in BET
        # get any text inside the preview QTextEdit
        # this will return HTML to superstar
        #superstar = dialog.templateTextEdit.toHtml()
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