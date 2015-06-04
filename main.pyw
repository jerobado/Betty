""" BIPC Template: email template generator for BIPC

    Interface: GUI (PyQt5)
    Language: Python 3.4.3
    Created: 10 Mar 2015 12:06 AM
    Next release date (NRD): Sep 1, 2015 -v0.3
 """

# TODO: create a new QDialog for filing template

__author__ = 'Niño'
# TODO: reminder, your are now currently working for another version of this app
__version__ = 0.3   # current version, see NRD

from design import APP, BETWindow, Search

if __name__ == '__main__':
    window = BETWindow(__version__)
    window.show()
    APP.exec_()