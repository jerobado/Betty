""" BIPC Template: email template generator for BIPC

    Interface: GUI (PyQt5)
    Language: Python 3.4.3
    Created: 10 Mar 2015 12:06 AM
    Due date: before the year ends ^^ -new deadline since new design is still underway
 """

__author__ = 'Niño'
__version__ = 0.1

from design import APP, BETWindow, BIPCTemplateGUI

if __name__ == '__main__':
    window = BIPCTemplateGUI()
    window = BETWindow()
    window.show()
    APP.exec_()