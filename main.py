import os

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *
from pyqt_line_number_widget import LineNumberWidget

app = QApplication([])

class LineWindow(QTextBrowser):
    def __init__(self, *_args):
        super().__init__(*_args)

    def wheelEvent(self, e: QtGui.QWheelEvent):
        pass

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.fileOpened = None
        self.savedText = None
        self.setWindowTitle("Text Editor")
        self.setMinimumWidth(800)
        self.setMinimumHeight(450)

        self.lay = QHBoxLayout()

        self.textWindow = QTextEdit(self)
        self.textWindow.move(60, 20)
        self.textWindow.verticalScrollBar().valueChanged.connect(self.moveLineWindow)

        self.lineWidget = LineWindow(self)
        self.lineWidget.setFixedWidth(60)
        self.lineWidget.move(0, 20)
        self.lineWidget.setPlainText("1")
        self.lineWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.textWindow.textChanged.connect(self.textUpdate)

        self.lay.addWidget(self.lineWidget)
        self.lay.addWidget(self.textWindow)

        self.setLayout(self.lay)
        self.createMenuBar()

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        self.resizeWidgets()

    def textUpdate(self):
        if self.lineWidget:
            n = int(self.textWindow.document().lineCount())
            lineString = "1"
            x = 1
            while n > x:
                x += 1
                lineString += f"\n{x}"
            self.lineWidget.document().setPlainText(lineString)

        if self.fileOpened:
            if self.savedText != self.textWindow.document().toPlainText():
                self.setWindowTitle(self.windowTitle() + "*")
            else:
                self.setWindowTitle(f"Text Editor - {str(os.path.basename(self.fileOpened))}")

    def moveLineWindow(self):
        self.lineWidget.verticalScrollBar().setValue(self.textWindow.verticalScrollBar().value())

    def resizeWidgets(self):
        self.textWindow.setFixedWidth(self.width()-60)
        self.textWindow.setFixedHeight(self.height())
        self.lineWidget.setFixedHeight(self.height())

    def createMenuBar(self):
        self.menuBar = self.menuBar()

        self.saveAction = QAction("Save", self)
        self.saveAction.setShortcut(QKeySequence.Save)
        self.saveAction.triggered.connect(self.saveFile)

        self.openAction = QAction("Open", self)
        self.openAction.setShortcut(QKeySequence.Open)
        self.openAction.triggered.connect(self.openFile)

        fileMenu = self.menuBar.addMenu("File")
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.openAction)
        self.setMenuBar(self.menuBar)

    def openFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files(*);;Text Files(*.txt)",
                                                   options=options)
        if file_name:
            f = open(file_name, "r")
            self.textWindow.setPlainText(f.read())
            f.close()
            self.fileOpened = file_name
            self.setWindowTitle(f"Text Editor - {str(os.path.basename(self.fileOpened))}")

    def saveFile(self):
        if self.fileOpened:
            f = open(self.fileOpened, "w")
            text = self.textWindow.document().toPlainText()
            f.write(text)
            f.close()
            self.savedText = text
            self.setWindowTitle(f"Text Editor - {str(os.path.basename(self.fileOpened))}")
        else:
            self.saveFileAs()

    def saveFileAs(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files(*);;Text Files(*.txt)",
                                                   options=options)
        if file_name:
            f = open(file_name, "w")
            text = self.textWindow.document().toPlainText()
            f.write(text)
            f.close()
            self.savedText = text
            self.fileOpened = file_name
            self.setWindowTitle(f"Text Editor - {str(os.path.basename(file_name))}")


window = Window()
window.show()
app.exec()
