""" Betty: special instruction generator for BIPC

    Interface: GUI (PyQt5)
    Language: Python 3.4.3
    Created: 10 Mar 2015 12:06 AM
    Next release date (NRD): Jul 1, 2016 -v0.4a
    Next release date (NRD): Aug 1, 2016 -v0.4b
    Next release date (NRD): Sep 1, 2016 -v0.4
 """

__author__ = 'GSMGBB'
__version__ = '0.4'   # Current version, see NRD


# TEST: just checking my PyQt version
def check_version():

    import sys
    import logging

    from PyQt5.QtCore import QT_VERSION_STR
    from PyQt5.Qt import PYQT_VERSION_STR
    from sip import SIP_VERSION_STR

    from resources.constants import LOGFILE

    logging.basicConfig(filename=LOGFILE,
                        filemode='w',
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    logging.info("~~~~~~~~~~~~~~~~~~~~~ BETTY STARTED ~~~~~~~~~~~~~~~~~~~~~")
    logging.info("[BET]: Python version {}".format(sys.version[:5]))
    logging.info("[BET]: Qt version {}".format(QT_VERSION_STR))
    logging.info("[BET]: PyQt version {}".format(PYQT_VERSION_STR))
    logging.info("[BET]: SIP version {}".format(SIP_VERSION_STR))


# For showing the icon in the taskbar
def icon_settings():

    import ctypes
    APP_ID = u'bakermckenzie.gipsc.betty.04'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)

if __name__ == '__main__':
    from main_window import BET
    from resources.constants import APP

    check_version()
    icon_settings()
    window = BET(__version__)
    window.show()
    APP.exec_()
