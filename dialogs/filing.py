# BET > dialogs > filing.py

__author__ = 'Jero'

from PyQt5.QtWidgets import (QLabel, QLineEdit, QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox,
                             QTextEdit, QPushButton, QGroupBox)
from PyQt5.QtGui import QTextDocument

from resources.constants import TYPE_TM, FILING, FILING_SPECIAL, FILING_TEMPLATE, STYLE


class Filing(QDialog):  # Main dialog for filing template

    def __init__(self, parent=None):
        super(Filing, self).__init__(parent)
        self._widgets()
        self._layout()
        self._properties()
        self._connections()

    def _widgets(self):

        self.trackerLineEdit = QLineEdit()
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
        self.addButton = QPushButton("&Add")
        self.addButton.setEnabled(False)
        self.clearButton = QPushButton("&Clear")

    def _layout(self):

        tracker_layout = QHBoxLayout()
        tracker_layout.addWidget(self.trackerLineEdit)
        tracker_layout.addStretch()

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
        self.resize(410, 550)  # width, height
        self.setWindowTitle("Filing Template | Testing")

    def _connections(self):

        self.previewButton.clicked.connect(self.on_previewButton_clicked)
        self.addButton.clicked.connect(self.accept)
        self.clearButton.clicked.connect(self.on_clearButton_clicked)

    # EVENT HANDLER starts here
    def on_clearButton_clicked(self):

        self.TMNCLineEdit.clear()
        self.special_instructionsLineEdit.clear()
        self.previewTextEdit.clear()

    def on_previewButton_clicked(self):

        # Check if self.special_instructionsLineEdit has no content
        if self.special_instructionsLineEdit.text():
            special_instruction = FILING_SPECIAL.format(self.special_instructionsLineEdit.text())
        else:
            special_instruction = ''

        # Consolidate
        html = FILING_TEMPLATE.substitute(special=special_instruction,
                                          filing=FILING.format(self.TMNCLineEdit.text(),
                                                               self.ToTMComboBox.currentText()))

        # Show result
        self.previewTextEdit.setHtml(html)

        # Enable self.addButton
        self.addButton.setEnabled(True)

        print("[BET]: Preview button clicked under Filing form")