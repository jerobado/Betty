# BET > dialogs > filing.py

__author__ = 'Jero'

from PyQt5.QtWidgets import (QLabel, QLineEdit, QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox,
                             QTextEdit, QPushButton, QGroupBox)

from resources.constants import TYPE_TM, FILING, FILING_SPECIAL, FILING_TEMPLATE


# TODO: create filing dialog here...
class Filing(QDialog):  # Main dialog for filing template

    def __init__(self, parent=None):
        super(Filing, self).__init__(parent)
        self._widgets()
        self._layout()
        self._properties()
        self._connections()

    def _widgets(self):

        self.TMNCLabel = QLabel("TMNC:")
        self.ToTMLabel = QLabel("Type of Trade Mark:")
        self.special_instructionsLabel = QLabel("Special Instructions:")
        self.previewLabel = QLabel("Preview:")
        self.TMNCLineEdit = QLineEdit()
        self.ToTMComboBox = QComboBox()
        self.ToTMComboBox.insertItems(0, TYPE_TM)
        self.special_instructionsLineEdit = QLineEdit()
        self.special_instructionsLineEdit.setPlaceholderText("Read correspondence for further instructions")
        self.previewTextEdit = QTextEdit()
        self.previewButton = QPushButton("Pr&eview")
        self.generateButton = QPushButton("&Generate")
        self.clearButton = QPushButton("&Clear")

    def _layout(self):

        grid = QGridLayout()
        grid.addWidget(self.TMNCLabel, 0, 0)
        grid.addWidget(self.TMNCLineEdit, 0, 1)
        grid.addWidget(self.ToTMLabel, 1, 0)
        grid.addWidget(self.ToTMComboBox, 1, 1)
        grid.addWidget(self.special_instructionsLabel, 2, 0)
        grid.addWidget(self.special_instructionsLineEdit, 2, 1)

        # input widgets inside the QGroupBox
        input_group = QGroupBox("Input Fields")
        input_group.setLayout(grid)

        # arrange the buttons horizontally
        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self.previewButton)
        buttons.addWidget(self.generateButton)
        buttons.addWidget(self.clearButton)

        # set everything vertically
        vertical = QVBoxLayout()
        vertical.addWidget(input_group)
        vertical.addWidget(self.previewLabel)
        vertical.addWidget(self.previewTextEdit)
        vertical.addLayout(buttons)

        # now let your parent arrange everything for you
        self.setLayout(vertical)

    def _properties(self):

        self.resize(410, 550)  # width, height
        self.setWindowTitle("Filing Template | Testing")

    def _connections(self):

        self.clearButton.clicked.connect(self.on_clearButton_clicked)
        self.previewButton.clicked.connect(self.on_previewButton_clicked)

    # EVENT HANDLER starts here
    def on_clearButton_clicked(self):

        self.TMNCLineEdit.clear()
        self.special_instructionsLineEdit.clear()
        self.previewTextEdit.clear()

    def on_previewButton_clicked(self):

        # Check if self.special_instructionsLineEdit has no content
        if not self.special_instructionsLineEdit.text():
            special_instruction = FILING_SPECIAL.format(self.special_instructionsLineEdit.text())
        else:
            special_instruction = ''

        # Consolidate
        html = FILING_TEMPLATE.substitute(special=special_instruction,
                                          filing=FILING.format(self.TMNCLineEdit.text(),
                                                               self.ToTMComboBox.currentText()))

        # Show result
        self.previewTextEdit.setHtml(html)
        print("[BET]: Preview button clicked under Filing form")