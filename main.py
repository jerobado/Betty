""" BIPC Template: email template generator for BIPC

    Interface: GUI (PyQt5)
    Language: Python 3.4.3
    Created: 10 Mar 2015 12:06 AM
    Next release date (NRD): May 10, 2015 -v0.2
 """

__author__ = 'Niño'
# TODO: reminder, your are now currently working for another version of this app
__version__ = 0.2   # current version, see NRD

from design import APP, BETWindow, BIPCTemplateGUI

if __name__ == '__main__':
    window = BIPCTemplateGUI()
    window = BETWindow()
    window.show()
    APP.exec_()