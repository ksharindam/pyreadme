#!/usr/bin/env python
import sys, os

from PyQt4 import QtCore, QtGui
from ui_mainwindow import Ui_MainWindow
import markdown, highlighter, resources

HOMEDIR = os.environ['HOME']

class Window(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.filename = HOMEDIR
        self.setupUi()
        self.show()

    def setupUi(self):
        Ui_MainWindow.setupUi(self, self)
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(4,0,0,0)
        self.textEdit = TextEdit(self.centralwidget)
        self.textView = QtGui.QTextEdit(self.centralwidget)
        self.textView.setReadOnly(True)
        self.horizontalLayout.addWidget(self.textEdit)
        self.horizontalLayout.addWidget(self.textView)
        self.textView.hide()
        # Create actions
        self.openFileAction = QtGui.QAction(QtGui.QIcon(':/open.png'), 'Open', self)
        self.openFileAction.setShortcut('Ctrl+O')
        self.openFileAction.triggered.connect(self.openFile)

        self.saveFileAction = QtGui.QAction(QtGui.QIcon(':/save.png'), 'Save', self)
        self.saveFileAction.setShortcut('Ctrl+S')
        self.saveFileAction.triggered.connect(self.saveFile)

        self.saveFileAsAction = QtGui.QAction(QtGui.QIcon(':/save-as.png'), 'Save As', self)
        self.saveFileAsAction.setShortcut('Ctrl+Shift+S')
        self.saveFileAsAction.triggered.connect(self.saveFileAs)

        self.exportHtmlAction = QtGui.QAction(QtGui.QIcon(':/web.png'), 'Export Html', self)
        self.exportHtmlAction.triggered.connect(self.exportHtml)

        self.closeAction = QtGui.QAction(QtGui.QIcon(':/quit.png'), 'Quit', self)
        self.closeAction.setShortcut('Ctrl+Q')
        self.closeAction.triggered.connect(self.close)

        self.previewModeAction = QtGui.QAction(QtGui.QIcon(':/preview.png'), 'Preview Mode', self)
        self.previewModeAction.setCheckable(True)
        #self.previewModeAction.setShortcut('Ctrl+Q')
        self.previewModeAction.triggered.connect(self.togglePreviewMode)

        self.boldFmtAction = QtGui.QAction(QtGui.QIcon(':/bold.png'), 'Bold', self)
        self.boldFmtAction.setShortcut('Ctrl+B')
        self.boldFmtAction.triggered.connect(self.setBold)

        self.italicFmtAction = QtGui.QAction(QtGui.QIcon(':/italic.png'), 'Italic', self)
        self.italicFmtAction.setShortcut('Ctrl+I')
        self.italicFmtAction.triggered.connect(self.setItalic)

        self.codeFmtAction = QtGui.QAction(QtGui.QIcon(':/code.png'), 'Inline Code', self)
        #self.codeFmtAction.setShortcut('Ctrl+I')
        self.codeFmtAction.triggered.connect(self.setCode)

        self.ulistFmtAction = QtGui.QAction(QtGui.QIcon(':/bullet.png'), 'Unordered List', self)
        #self.ulistFmtAction.setShortcut('Ctrl+I')
        self.ulistFmtAction.triggered.connect(self.setUlist)

        self.olistFmtAction = QtGui.QAction(QtGui.QIcon(':/number.png'), 'Ordered List', self)
        #self.olistFmtAction.setShortcut('Ctrl+I')
        self.olistFmtAction.triggered.connect(self.setOlist)

        self.linkFmtAction = QtGui.QAction(QtGui.QIcon(':/link.png'), 'Insert Link', self)
        #self.linkFmtAction.setShortcut('Ctrl+I')
        self.linkFmtAction.triggered.connect(self.setLink)

        self.imageFmtAction = QtGui.QAction(QtGui.QIcon(':/image.png'), 'Insert Image', self)
        #self.imageFmtAction.setShortcut('Ctrl+I')
        self.imageFmtAction.triggered.connect(self.setImage)

        # Add menu actions
        self.menu_File.addAction(self.openFileAction)
        self.menu_File.addAction(self.saveFileAction)
        self.menu_File.addAction(self.saveFileAsAction)
        self.menu_File.addAction(self.exportHtmlAction)
        self.menu_File.addAction(self.closeAction)
        self.menuView.addAction(self.previewModeAction)
        self.menuFormat.addAction(self.boldFmtAction)
        self.menuFormat.addAction(self.italicFmtAction)
        self.menuFormat.addAction(self.codeFmtAction)
        self.menuFormat.addAction(self.ulistFmtAction)
        self.menuFormat.addAction(self.olistFmtAction)
        self.menuFormat.addAction(self.linkFmtAction)
        self.menuFormat.addAction(self.imageFmtAction)

        # Add toolbar actions
        self.toolBar.addAction(self.openFileAction)
        self.toolBar.addAction(self.saveFileAction)
        self.toolBar.addAction(self.saveFileAsAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.previewModeAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.boldFmtAction)
        self.toolBar.addAction(self.italicFmtAction)
        self.toolBar.addAction(self.codeFmtAction)
        self.toolBar.addAction(self.ulistFmtAction)
        self.toolBar.addAction(self.olistFmtAction)
        self.toolBar.addAction(self.linkFmtAction)
        self.toolBar.addAction(self.imageFmtAction)
        spacer = QtGui.QWidget(self.toolBar)
        spacer.setSizePolicy(1|2|4,1|4)
        self.toolBar.addWidget(spacer)
        self.toolBar.addAction(self.closeAction)
        # Connect Signals

    def onTextSelect(self):
        cur = self.textEdit.textCursor()
        print(cur.selectedText())

    def formatText(self, format1, format2):
        cur = self.textEdit.textCursor()
        text = cur.selectedText()
        cur.insertText(format1 + text + format2)
        cur.setPosition(cur.position()-len(format2))
        self.textEdit.setTextCursor(cur)

    def setBold(self):
        self.formatText('**', '**')

    def setItalic(self):
        self.formatText('_', '_')

    def setCode(self):
        self.formatText('`', '`')

    def setUlist(self):
        self.setList('* ')

    def setOlist(self):
        self.setList('1. ')

    def setList(self, pattern):
        cur = self.textEdit.textCursor()
        anc = cur.anchor()
        pos = cur.position()
        cur.setPosition(anc)
        cur.movePosition(3)
        cur.setPosition(pos, 1)
        text = pattern + unicode(cur.selectedText())
        text = ('\n' + pattern).join(text.splitlines())
        cur.insertText(text)
        self.textEdit.setTextCursor(cur)

    def setLink(self):
        self.formatText('[', ']()')

    def setImage(self):
        self.formatText('![', ']()')

    def openFile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, "Select File to Open", self.filename,
                                      "All Files (*);;Markdown Files (*.md);;HTML Files (*.html *.htm)" )
        if not filename.isEmpty():
            self.loadFile(filename)

    def loadFile(self, filename):
        with open(filename, 'r') as doc:
            text = doc.read()
        if filename.endsWith('.md'):
            self.textEdit.highlighter.enableHighlighter(True)
        else:
            self.textEdit.highlighter.enableHighlighter(False)
        self.textEdit.setText(text)
        self.setWindowTitle(filename)
        self.filename = filename
        self.previewModeAction.setChecked(False)

    def saveFileAs(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, "Select File to Save", self.filename,
                                      "All Files (*);;Markdown Files (*.md)" )
        if filename.isEmpty(): return
        self.filename = filename        
        self.setWindowTitle(filename)
        self.saveFile()

    def saveFile(self):
        if self.filename == HOMEDIR:
            self.saveFileAs()
            return
        text = self.textEdit.toPlainText().toUtf8()
        with open(self.filename, 'w') as doc:
            doc.write(text)

    def exportHtml(self):
        name = os.path.splitext(unicode(self.filename))[0] + '.html'
        filename = QtGui.QFileDialog.getSaveFileName(self, "Select File to Save", name,
                                      "HTML Files (*.html *.htm)" )
        if filename.isEmpty(): return
        text = unicode(self.textEdit.toPlainText())
        html = markdown.markdown(text)
        with open(filename, 'w') as doc:
            doc.write(html)

    def togglePreviewMode(self, checked):
        if checked:
            text = unicode(self.textEdit.toPlainText())
            html = markdown.markdown(text)
            self.textEdit.hide()
            self.textView.show()
            self.textView.setHtml(html)
        else:
            self.textView.hide()
            self.textEdit.show()

class TextEdit(QtGui.QTextEdit):
    def __init__(self, parent):
        QtGui.QTextEdit.__init__(self, parent)
        self.setTabStopWidth(32)
        self.highlighter = highlighter.MarkdownHighlighter(self)

def main():
    app = QtGui.QApplication(sys.argv)
    win = Window()
    if len(sys.argv)>1 and os.path.exists(os.path.abspath(sys.argv[-1])):
        win.loadFile(QtCore.QString.fromUtf8(os.path.abspath(sys.argv[-1])))
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
