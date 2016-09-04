""" Betty: special instruction generator for BIPC

    Interface: GUI (PyQt5)
    Language: Python 3.4.4
    Created: 10 Mar 2015 12:06 AM
    Next release date (NRD): Dec 1, 2016 -v0.6
 """


def check_version():
    """ Dummy function for checking my tools current version """

    import sys
    import logging

    from PyQt5.QtCore import QT_VERSION_STR
    from PyQt5.Qt import PYQT_VERSION_STR
    from sip import SIP_VERSION_STR

    from resources.constants import __version__

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    logging.info("[BET]: Betty version {}".format(__version__))
    logging.info("[BET]: Python version {}".format(sys.version[:5]))
    logging.info("[BET]: Qt version {}".format(QT_VERSION_STR))
    logging.info("[BET]: PyQt version {}".format(PYQT_VERSION_STR))
    logging.info("[BET]: SIP version {}".format(SIP_VERSION_STR))


def icon_settings():
    """ Simple line I found on the Net to show the icon in the taskbar. """

    import ctypes
    APP_ID = u'bakermckenzie.gipsc.betty.06'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)

if __name__ == '__main__':
    from src.main_window import Betty
    from resources.constants import APP

    check_version()
    icon_settings()
    window = Betty()
    window.show()
    APP.exec_()
