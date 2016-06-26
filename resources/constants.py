# Betty > resources > constants.py
# Define global and constant variables here

__author__ = 'Jero'

import sys
from string import Template
from PyQt5.QtWidgets import QApplication
from main import __author__, __version__

# used by main.py
APP = QApplication(sys.argv)
LOGFILE = "log\log_sessions.log"

# Use by the two templates
STYLE = """
    p {
        font-family: "Arial";
        font-size: 10pt;
    }
    """

# used by dialogs/search.py
WITH_ARTWORK = "<div><p><b>Artwork attached to illustrate how the mark will appear on pack.</b></p></div>"
WITH_IMAGE = "<div><p>The trade mark to be searched is as shown in the attached image file.</p></div>"

# TOOLTIPS
ARTWORK_TOOLTIP = """Artwork attached to illustrate how the mark will appear on pack.<br> \
                Always verify with the sender if the image provided is the actual image to be searched or the image \
                is just an artwork."""
IMAGE_TOOLTIP = "The trade mark to be searched is as shown in the attached image file."

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

# next is Google
GOOGLE_TAT = {
    'Low/Medium': """
        <div><p><b>DEADLINE: {}.</b> Please provide your search report ON or BEFORE the specified deadline. \
        If the due date falls on a weekend, holiday or non-working day, please send us your search \
        analysis before then.</p></div>""",
    'Critical': """
        <div><p><b>DEADLINE: URGENT, {}.</b> Please provide your search report ON or BEFORE the specified deadline. \
        If the due date falls on a weekend, holiday or non-working day, please send us your search \
        analysis before then.</p></div>"""
}
GOOGLE_DEFAULT = """
        <div><p>In determining your analysis, please note that we are only concerned with the ability to \
        <b><u>use</u></b> the mark, <b><u>not to register</u></b> the mark.</p></div>"""


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
SEARCH_TEMPLATE = Template("$default $special $artwork $TAT $image")

# used by dialogs/filing.py
TYPE_TM = ['Advertising Strip',
           'Arabic Characters',
           'Bengali Characters',
           'Black and White',
           'Chinese Characters',
           'Colour',
           'Combined',
           'Cyrillic Characters',
           'Design Application',
           'Design Only',
           'Device Only',
           'Farsi Characters',
           'Foreign Language Mark',
           'Form',
           'Form and Word',
           'Greek Characters',
           'Gujerati Characters',
           'Gurmukhi (Punjabi) Characters',
           'Hangul Characters',
           'Hebrew Characters',
           'Hindi Characters',
           'Hiragana Characters',
           'Hungarian Characters',
           'ICELANDIC CHARACTERS',
           'Japanese Characters',
           'Kanarese Characters',
           'Katakana Characters',
           'Korean Characters',
           'Label',
           'Malayalam Characters',
           'Marathi Characters',
           'Misc and Word',
           'Miscellaneous',
           'Packaging',
           'Polish Characters',
           'Pushtu Characters',
           'Signature',
           'Sindhi Characters',
           'Sinhala Characters',
           'Slogan',
           'Slogan (Trademark)',
           'Slogan-Design',
           'Slogan-Design (Trademark)',
           'Slogan-Device',
           'Slogan-Device (Trademark)',
           'Smell',
           'Sound',
           'Stylised Word',
           'Tamil Characters',
           'Telugu Characters',
           'Thai Characters',
           'Three Dimensional',
           'Turkish Characters',
           'Two Dimensional',
           'Urdu Characters',
           'Vietnamese Characters',
           'VISUAL GRAPHICS',
           'Word',
           'Word in standard characters',
           'Word Mark',
           'Word-Design',
           'Word-Device',
           'Word-Label']

WORK_TYPE = ['Filing', 'Search (SIW)']

GE_DEFAULT = """
        </div><p><b>
        The description of goods should be exactly as listed in the record. If you believe that the description \
        proposed by our client is likely to be rejected, you should review and confirm any revision to the goods with \
        GIPSC before filing the application.
        </p></b></div>"""
FILING = """
        <p>The trade mark to be filed is as shown in the attached image file. The type of trade mark is <b>{0}</b>.</p>

        <p>Please note that the mark is referred to in GIPM and should be referred to in all correspondence
        as <b>{1}</b>.</p>

        <p>For your information, as part of our trade mark naming conventions, we use descriptive terms (e.g., DEVICE,
        STYLISED, FOREIGN CHARACTERS, SLOGAN, PACKAGING, THREE-DIMENSIONAL, LABEL, etc.) to aid in the identification
        of trade marks, which differ from PLAIN BLOCK CAPITAL LETTERS. Such descriptive terms are added to the end of
        a trade mark, but they DO NOT FORM PART OF THE TRADE MARK itself.</p>"""
FILING_SPECIAL = "<p><b>{0}</b></p>"
FILING_TEMPLATE = Template("$default $special $filing")

# use by main_window.py
ABOUT = """
        <div>
            <b>Betty {0}</b>
            <hr>
        </div>
        <div>
            <i>Betty is a program that can be use alongside BIPC for creating workplan.</i>
            <br><br>
            The main goal of <i>Betty</i> is to provide rapid creation of special instruction templates that adheres \
            to the standard process use by the Core Team.
            <br><br>
            Released: 1 Sep 2016
            <br>
            Author: {1}
            <br>
            Site: <a href="https://github.com/mokachokokarbon/Project-BET"
                     style="text-decoration:None">Fork me on GitHub!</a>
        </div>
        """.format(__version__, __author__)
TITLE = "Betty {}".format(__version__)
