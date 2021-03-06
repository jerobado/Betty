# Project-BET > resources > models.py
# User-defined models to be created here

from PyQt5.QtCore import (Qt,
                          QModelIndex,
                          QAbstractListModel)
from PyQt5.QtGui import QIcon
from resources._constant import (TEMP_TEMPLATE_STORAGE_LIST,
                                 TEMP_TEMPLATE_DIALOG_INFO,
                                 TEMP_TEMPLATE_DATECREATED,
                                 TEMP_TEMPLATE_SEARCH_TAT,
                                 TEMP_TEMPLATE_SEARCH_IMPORTANCE,
                                 FILING_TOOLTIP,
                                 SEARCH_TOOLTIP)


class TrackerListModel(QAbstractListModel):
    """
        A model for holding a list of newly created template.

        Accepts default date and time or 'User's marks'
    """

    def __init__(self, trackerlist, parent=None):
        super(TrackerListModel, self).__init__(parent)
        self.__trackerlist = trackerlist

    def data(self, index, role):
        if role == Qt.DisplayRole:
            row = index.row()
            value = self.__trackerlist[row]
            return value

        if role == Qt.DecorationRole:
            row = index.row()
            icon_info = TEMP_TEMPLATE_DIALOG_INFO[row]

            if icon_info == 'Filing':
                return QIcon(':/file_32.png')

            if icon_info == 'Searching':
                return QIcon(':/magnify_32.png')

        if role == Qt.EditRole:
            return self.__trackerlist[index.row()]

        if role == Qt.ToolTipRole:
            row = index.row()
            template = TEMP_TEMPLATE_STORAGE_LIST[row]
            dialog_info = TEMP_TEMPLATE_DIALOG_INFO[row]
            date_created = TEMP_TEMPLATE_DATECREATED[row]

            if dialog_info == 'Filing':
                return FILING_TOOLTIP.format(template, dialog_info, date_created)
            else:
                tat = TEMP_TEMPLATE_SEARCH_TAT[row]
                importance = TEMP_TEMPLATE_SEARCH_IMPORTANCE[row]
                return SEARCH_TOOLTIP.format(template, dialog_info, importance, tat, date_created)

    def setData(self, index, value, role=Qt.DisplayRole):
        if role == Qt.EditRole:
            row = index.row()
            self.__trackerlist[row] = value
            return True

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable

    def rowCount(self, parent):
        return len(self.__trackerlist)

    def insertRows(self, position, rows, parent=QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        # Still works!
        self.endInsertRows()
        return True


class WorktypeListModel(QAbstractListModel):
    """
        A model for holding the worktypes usually done by the Core team.

        Accepts WORKTYPE from _constants.py
    """

    def __init__(self, worktypes, parent=None):
        super(WorktypeListModel, self).__init__(parent)
        self.__worktype = worktypes

    def data(self, index, role):
        if role == Qt.DisplayRole:
            row = index.row()
            value = self.__worktype[row]
            return value

        if role == Qt.DecorationRole:
            row = index.row()
            value = self.__worktype[row]

            if value == 'Filing':
                return QIcon(':/file_32.png')

            if value == 'Search (SIW)':
                return QIcon(':/magnify_32.png')

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def rowCount(self, parent):
        return len(self.__worktype)