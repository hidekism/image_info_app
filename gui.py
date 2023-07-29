# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(730, 576)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setMinimumSize(QtCore.QSize(0, 290))
        self.table.setColumnCount(3)
        self.table.setObjectName("table")
        self.table.setRowCount(0)
        self.verticalLayout.addWidget(self.table)
        self.copyButton = QtWidgets.QPushButton(self.centralwidget)
        self.copyButton.setMinimumSize(QtCore.QSize(0, 32))
        self.copyButton.setObjectName("copyButton")
        self.verticalLayout.addWidget(self.copyButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radio_html = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_html.setObjectName("radio_html")
        self.horizontalLayout_2.addWidget(self.radio_html)
        self.radio_css = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_css.setObjectName("radio_css")
        self.horizontalLayout_2.addWidget(self.radio_css)
        self.radio_custom = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_custom.setObjectName("radio_custom")
        self.horizontalLayout_2.addWidget(self.radio_custom)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.fliepath = QtWidgets.QLineEdit(self.centralwidget)
        self.fliepath.setMinimumSize(QtCore.QSize(0, 64))
        self.fliepath.setObjectName("fliepath")
        self.verticalLayout.addWidget(self.fliepath)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.custom_text = QtWidgets.QTextEdit(self.centralwidget)
        self.custom_text.setMaximumSize(QtCore.QSize(16777215, 32))
        self.custom_text.setObjectName("custom_text")
        self.horizontalLayout.addWidget(self.custom_text)
        self.browseButton = QtWidgets.QPushButton(self.centralwidget)
        self.browseButton.setMinimumSize(QtCore.QSize(100, 0))
        self.browseButton.setMaximumSize(QtCore.QSize(100, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.browseButton.setFont(font)
        self.browseButton.setObjectName("browseButton")
        self.horizontalLayout.addWidget(self.browseButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 730, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.copyButton.setText(_translate("MainWindow", "Copy"))
        self.radio_html.setText(_translate("MainWindow", "HTML"))
        self.radio_css.setText(_translate("MainWindow", "CSS形式"))
        self.radio_custom.setText(_translate("MainWindow", "カスタム"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.browseButton.setText(_translate("MainWindow", "Browse"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
