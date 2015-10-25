# define global and constant variables here

import sys

from PyQt5.QtWidgets import QApplication

from string import Template

__author__ = 'Jero'

# used by main.pyw
APP = QApplication(sys.argv)

# used by dialogs/search.py
SPECIAL_INS = "<div><p><b>{}</b></p></div>"
WITH_ARTWORK = "<div><p>Artwork attached to illustrate how the mark will appear on pack.</p></div>"
WITH_IMAGE = "<div><p>The trade mark to be searched is as shown in the attached image file.</p></div>"
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
TEMPLATE = Template("$special $artwork $TAT $image")
STYLE = """
    div {
        font-family: "Arial";
        font-size: 10pt;
    }
    """

# used by dialogs/filing.py
TYPE_TM = ['Arabic Characters',
           'Design Only',
           'Device Only',
           'Stylised Word',
           'Word-Device',
           'Word-Design',
           'Word in standard characters']
WORK_TYPE = ['Filing', 'Search (SIW)']
