""" BIPC Template: email template generator for BIPC

    Interface: GUI (PyQt5)
    Language: Python 3.4.3
    Created: 10 Mar 2015 12:06 AM
    Next release date (NRD): Dec 1, 2015 -v0.3
 """

__author__ = 'Niño'
# TODO: reminder, your are now currently working for another version of this app
__version__ = 0.3   # current version, see NRD

from main_window import BET
from resources.constants import APP

if __name__ == '__main__':
    APP.setOrganizationName("GIPSC Core Team")
    APP.setOrganizationDomain("bakermckenzie.com")
    APP.setApplicationName("BET")
    window = BET(__version__)
    window.show()
    APP.exec_()
