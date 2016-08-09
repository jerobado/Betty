# User-defined models to be created here

from PyQt5.QtCore import (Qt,
                          QModelIndex,
                          QAbstractListModel)
from PyQt5.QtGui import QIcon


class TrackerListModel(QAbstractListModel):
    """
        A model for holding a list of newly created template.

        Accepts default date and time or 'User's marks'
    """

    def __init__(self, trackerlist, parent=None):
        super(TrackerListModel, self).__init__(parent)
        self.__trackerlist = trackerlist

    def data(self, index, role):
        # TODO: something does not know where to append the last tracker name
        if role == Qt.DisplayRole:
            row = index.row()
            value = self.__trackerlist[row]
            return value

        if role == Qt.EditRole:
            return self.__trackerlist[index.row()]

    def setData(self, index, value, role=Qt.DisplayRole):
        if role == Qt.EditRole:
            row = index.row()
            self.__trackerlist[row] = value
            return True

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable

    def rowCount(self, parent):
        return len(self.__trackerlist)

    def insertRows(self, position, rows, parent = QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        # Still works!
        self.endInsertRows()
        return True


class WorktypeListModel(QAbstractListModel):
    """
        A model for holding the worktypes usually done by the Core team.

        Accepts WORKTYPE from constants.py
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