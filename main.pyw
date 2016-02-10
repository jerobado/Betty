""" BIPC Template: email template generator for BIPC

    Interface: GUI (PyQt5)
    Language: Python 3.4.3
    Created: 10 Mar 2015 12:06 AM
    Next release date (NRD): Mar 1, 2016 -v0.4
 """

__author__ = 'Jero'
__version__ = 0.4   # Current version, see NRD

from main_window import BET
from resources.constants import APP


# TEST: just checking my PyQt version
def check_version():

    import sys
    from PyQt5.QtCore import QT_VERSION_STR
    from PyQt5.Qt import PYQT_VERSION_STR
    from sip import SIP_VERSION_STR

    print("[BET]: Python version", sys.version[:5])
    print("[BET]: Qt version", QT_VERSION_STR)
    print("[BET]: PyQt version", PYQT_VERSION_STR)
    print("[BET]: SIP version", SIP_VERSION_STR)


# For showing the icon in the taskbar
def icon_settings():

    import ctypes
    APP_ID = u'bakermckenzie.gipsc.betty.03'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)

if __name__ == '__main__':
    check_version()
    icon_settings()
    APP.setOrganizationName("GIPSC Core Team")
    APP.setOrganizationDomain("bakermckenzie.com")
    APP.setApplicationName("Betty")
    window = BET(__version__)
    window.show()
    APP.exec_()
