""" Betty: special instruction generator for BIPC

    Interface: GUI (PyQt5)
    Language: Python 3.5.2
    Created: 10 Mar 2015 12:06 AM
    Next release date (NRD): Jun 1, 2017 -v0.7
 """


def check_tools_version() -> None:
    """ Dummy function for checking my tools current version """

    import sys
    import logging
    from PyQt5.QtCore import QT_VERSION_STR
    from PyQt5.Qt import PYQT_VERSION_STR
    from sip import SIP_VERSION_STR
    from resources._constants import __version__

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    if sys.version[:5] == '3.5.2':
        logging.info("[BET]: Betty version {0}".format(__version__))
        logging.info("[BET]: Python version {0}".format(sys.version[:5]))
        logging.info("[BET]: Qt version {0}".format(QT_VERSION_STR))
        logging.info("[BET]: PyQt version {0}".format(PYQT_VERSION_STR))
        logging.info("[BET]: SIP version {0}".format(SIP_VERSION_STR))


def configure_app_icon() -> None:
    """ This will show the icon of Betty in the taskbar """

    import ctypes
    APP_ID = u'bakermckenzie.gipsc.betty.07'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)

if __name__ == '__main__':
    from src.main_window import Betty
    from resources._constants import APP

    check_tools_version()
    configure_app_icon()
    window = Betty()
    window.show()
    APP.exec()
