"""
    Outline of classes.
    * BET(QMainWindow)
        + New(QDialog) -> moved to dialogs/new.py
    * Filing(QDialog) -> moved to dialogs/filing.py
    * Search(QDialog) -> moved to dialogs/search.py
"""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from PyQt5.QtWidgets import (QMainWindow, QLabel, QTextEdit, QDesktopWidget, QAction, QMessageBox, QDockWidget,
                             QListWidget)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import Qt, QSettings, QVariant, QSize, QPoint  # you imported something here that's never use!

from resources import bipc_resources   # Don't remove this!

# Application settings variables
APPEND = True   # default, any new template created will overwrite the previous one


# UTILITY functions: define handy function blocks here
def show_message_box():
    """ Handy message box creation """

    not_available_msg = QMessageBox()
    not_available_msg.setIcon(QMessageBox.Information)
    not_available_msg.setWindowTitle("BET | Message")
    not_available_msg.setText("'Filing' is not yet available. Send an email to GSMGBB for some updates.")
    not_available_msg.exec()


def show_whats_new():
    """ Handy 'print' statement that will tell you what new template is added on the main window. """

    print('[BET]: New template added')


# Main window for our application
class BET(QMainWindow):

    def __init__(self, version, parent=None):
        super(BET, self).__init__(parent)

        # resident variables
        self.__version__ = version

        self._widgets()
        self._properties()

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

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.resize(600, 350)   # width, height
        # set BET to center screen
        self.screenMainSize = QDesktopWidget().screenGeometry()
        print("[BET]: screen size:", self.screenMainSize)
        self.BETsize = self.geometry()
        # horizontal position = screenwidth - windowwidth /2
        hpos = (self.screenMainSize.width() - self.BETsize.width()) / 2
        vpos = (self.screenMainSize.height() - self.BETsize.height()) / 2
        self.move(hpos, vpos)
        print("[BET]: size", self.BETsize)
        self.setWindowTitle("BET %s" % self.__version__)
        #self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

    def _connections(self):
        """ Connect widget signals and slots """

        self.testTextEdit.copyAvailable.connect(self.copyAction.setEnabled)
        self.testTextEdit.copyAvailable.connect(self.cutAction.setEnabled)

    def _createActions(self):

        # Remember: when using QIcon, don't forget to update resources.qrc
        # Remember: when creating a QAction, it should have a parent
        # File menu: actions inside this menu
        self.newAction = QAction(QIcon(":/new.png"), "&New", self, shortcut=QKeySequence.New,
                                 statusTip="Create a new template", toolTip="New", triggered=self.on_newTemplate_action)
        self.settingsAction = QAction(QIcon(":/settings.png"), "Se&ttings", self, shortcut="Ctrl+Alt+S",
                                      statusTip="Edit application settings", triggered=self.on_settings_action)
        self.exitAction = QAction(QIcon(":/quit.png"), "E&xit", self, shortcut="Ctrl+Q",
                                  statusTip="Exit the application", triggered=self.close)

        # Edit menu: actions inside this menu
        self.cutAction = QAction(QIcon(":/cut.png"), "Cu&t", self, shortcut=QKeySequence.Cut, enabled=False,
                                 statusTip="Cut to clipboard", toolTip="Cut", triggered=self.testTextEdit.cut)
        self.copyAction = QAction(QIcon(":/copy.png"), "&Copy", self, shortcut=QKeySequence.Copy, enabled=False,
                                  statusTip="Copy to clipboard", toolTip="Copy", triggered=self.testTextEdit.copy)
        self.pasteAction = QAction(QIcon(":/paste.png"), "&Paste", self, shortcut=QKeySequence.Paste,
                                   statusTip="Paste from clipboard", toolTip="Paste", triggered=self.testTextEdit.paste)
        self.select_allAction = QAction(QIcon(":/select_all.png"), "Select &All", self, shortcut=QKeySequence.SelectAll,
                                        statusTip="Select all", triggered=self.testTextEdit.selectAll)

        # Settings: testing a checkable action inside a menu
        self.checkAction = QAction("Append Template", self, checkable=True,
                                   statusTip="Append created template to editor", triggered=self.testCheckAction)

    def _createMenus(self):
        """ FILE, EDIT (Cut, Copy, Paste), Format (Bold, UPPERCASE, etc., Help """

        # File: application's commands
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.settingsAction)
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

        # Settings: check...
        self.settingsMenu = self.menuBar().addMenu("Se&ttings")
        self.settingsMenu.addAction(self.checkAction)

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

        # Dock Widget
        self.tracker_dock = QDockWidget("Tracker", self)
        self.tracker_dock.setObjectName("Tracker")
        self.tracker_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        # Add widget to be inserted inside self.tracker_dock
        self.trackerListWidget = QListWidget()
        self.tracker_dock.setWidget(self.trackerListWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.tracker_dock)
        # Add an action, you cannot customize tracker action by using QDockWidget.toggleViewAction()
        self.viewMenu.addAction(self.tracker_dock.toggleViewAction())
        print("[BET]: Tracker activated")

    # SLOTS: Define BET slots here
    def on_newTemplate_action(self):
        """ Event handler for File > New """

        from dialogs.new import New

        print("[BET]: Selecting new template")  # BET prompt

        newWindow = New(self)
        # BET.windowList.append(newWindow)
        # TODO: make "Add new template" center here
        newWindow.move(self.x() + 175, self.y() + 125)  # attempting to move

        if newWindow.exec_():
            if newWindow.templateListWidget.currentItem().text() == "Search (SIW)":
                print("[BET]: Search template selected")  # BET prompt
                # show Search template
                from dialogs.search import Search

                searchDialog = Search(self)
                if searchDialog.exec_():
                    # if the user hit 'Generate', populate self.testTextEdit in BET
                    # get any text inside the preview QTextEdit
                    superstar = searchDialog.templateTextEdit.toHtml()
                    self.checkIfAppendTemplate(superstar)
            elif newWindow.templateListWidget.currentItem().text() == "Filing":
                # Show filing template dialog here
                from dialogs.filing import Filing

                filingDialog = Filing(self)
                print("[BET]: Filing template selected")  # BET prompt
                if filingDialog.exec_():
                    # TODO: your Filing template is somehow functional, once refined try to connect it here
                    superstar = filingDialog.previewTextEdit.toHtml()
                    self.checkIfAppendTemplate(superstar)
            else:
                print("[BET]: Unusual, no template selected?")

    # UTILITIES: functional task use by BET window
    def checkIfAppendTemplate(self, superstar):

        # Check if Appending is activated
        if APPEND:
            # transmit the data to the main window overriding any text
            self.testTextEdit.setHtml(superstar)
        else:
            self.testTextEdit.append(superstar)

    # TODO: retain the previous state when the user closed the application
    def on_settings_action(self):
        """ Event handler for File > Settings """

        from dialogs.settings import Settings

        dialog = Settings()
        if dialog.exec_():
            if dialog.appendCheckBox.isChecked():
                global APPEND
                APPEND = False

    def testCheckAction(self):  # much better

        global APPEND

        if self.checkAction.isChecked():
            APPEND = False
        else:
            APPEND = True
