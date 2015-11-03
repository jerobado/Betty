""" BIPC Template: email template generator for BIPC

    Interface: GUI (PyQt5)
    Language: Python 3.4.3
    Created: 10 Mar 2015 12:06 AM
    Next release date (NRD): Dec 1, 2015 -v0.3
 """

__author__ = 'Niño'
# TODO: reminder, your are now currently working for another version of this app
__version__ = 0.3   # Current version, see NRD

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

if __name__ == '__main__':
    # Shibuya daw :)
    check_version()
    APP.setOrganizationName("GIPSC Core Team")
    APP.setOrganizationDomain("bakermckenzie.com")
    APP.setApplicationName("BET")
    window = BET(__version__)
    window.show()
    APP.exec_()
