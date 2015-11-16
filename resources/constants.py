# BET > resources > constants.py
# Define global and constant variables here

__author__ = 'Jero'

import sys

from PyQt5.QtWidgets import QApplication

from string import Template

# used by main.pyw
APP = QApplication(sys.argv)

# Use by the two templates
STYLE = """
    p {
        font-family: "Arial";
        font-size: 10pt;
    }
    """

# used by dialogs/search.py
WITH_ARTWORK = "<div><p>Artwork attached to illustrate how the mark will appear on pack.</p></div>"
WITH_IMAGE = "<div><p>The trade mark to be searched is as shown in the attached image file.</p></div>"

# TOOLTIPS
ARTWORK_TOOLTIP = """Artwork attached to illustrate how the mark will appear on pack.<br> \
                Always verify with the sender if the image provided is the actual image to be searched or the image \
                is just an artwork."""
IMAGE_TOOLTIP = "The trade mark to be searched is as shown in the attached image file."


# TEST: trying to consolidate TAT template in a dictionary, Unilever first TODO: so far, so good
UN_TAT = {
    'Low/Medium': """
        <div><p><b>DEADLINE: {}.</b> Please provide your search report ON or BEFORE the specified deadline. \
        If the due date falls on a weekend, holiday or non-working day, please send us your search \
        analysis before then.</p></div>""",
    'Critical': """
        <div><p><b>DEADLINE: URGENT, {}.</b> Please provide your search report ON or BEFORE the specified deadline. \
        If the due date falls on a weekend, holiday or non-working day, please send us your search \
        analysis before then.</p></div>"""
}

# next is GE
GE_TAT = {
    'Low/Medium': """
        <div><p><b>DEADLINE: {}.</b> Please provide your search report ON or BEFORE the specified deadline. \
        If the due date falls on a weekend, holiday or non-working day, please send us your search \
        analysis on the next business day.</p></div>""",
    'Critical': """
        <div><p><b>DEADLINE: EXPEDITED, {}.</b> Please provide your search report ON or BEFORE the specified deadline. \
        If the due date falls on a weekend, holiday or non-working day, please send us your search \
        analysis on the next business day.</p></div>"""
}
SEARCH_SPECIAL = "<div><p><b>{}</b></p></div>"
SEARCH_TEMPLATE = Template("$special $artwork $TAT $image")

# used by dialogs/filing.py
TYPE_TM = ['Arabic Characters',
           'Chinese Characters',
           'Design Only',
           'Device Only',
           'Hangul Characters',
           'Katakana Characters',
           'Stylised Word',
           'Three Dimensional',
           'Word-Device',
           'Word-Design',
           'Word in standard characters']
WORK_TYPE = ['Filing', 'Search (SIW)']
FILING = """
        <p>The trade mark to be filed is as shown in the attached image file. The type of trade mark is <b>{0}</b>.</p>

        <p>Please note that the mark is referred to in GIPM and should be referred to in all correspondence
        as <b>{1}</b>.</p>

        <p>For your information, as part of our trade mark naming conventions, we use descriptive terms (e.g., DEVICE,
        STYLISED, FOREIGN CHARACTERS, SLOGAN, PACKAGING, THREE-DIMENSIONAL, LABEL, etc.) to aid in the identification
        of trade marks, which differ from PLAIN BLOCK CAPITAL LETTERS. Such descriptive terms are added to the end of
        a trade mark, but they DO NOT FORM PART OF THE TRADE MARK itself.</p>"""
FILING_SPECIAL = "<p><b>{0}</b></p>"
FILING_TEMPLATE = Template("$special $filing")