#!/usr/bin/env python3
import sys, os
import markdown
from PyQt4 import QtCore
from PyQt4.QtGui import ( QApplication, QMainWindow, QHBoxLayout, QWidget, QTextEdit,
    QFileDialog
)

sys.path.append(os.path.dirname(__file__))
from ui_mainwindow import Ui_MainWindow
import highlighter, resources_rc

HOMEDIR = os.path.expanduser('~')

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.filename = HOMEDIR
        # setup ui
        self.setupUi(self)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(4,0,0,0)
        self.textEdit = TextEdit(self.centralwidget)
        self.textView = TextView(self.centralwidget)
        self.textView.setReadOnly(True)
        self.horizontalLayout.addWidget(self.textEdit)
        self.horizontalLayout.addWidget(self.textView)
        self.textView.hide()

        # Connect Actions to slots
        self.openFileAction.triggered.connect(self.openFile)
        self.saveFileAction.triggered.connect(self.saveFile)
        self.saveFileAsAction.triggered.connect(self.saveFileAs)
        self.exportHtmlAction.triggered.connect(self.exportHtml)
        self.closeAction.triggered.connect(self.close)
        self.previewModeAction.triggered.connect(self.togglePreviewMode)
        self.boldFmtAction.triggered.connect(self.setBold)
        self.italicFmtAction.triggered.connect(self.setItalic)
        self.codeFmtAction.triggered.connect(self.setCode)
        self.ulistFmtAction.triggered.connect(self.setUlist)
        self.olistFmtAction.triggered.connect(self.setOlist)
        self.linkFmtAction.triggered.connect(self.setLink)
        self.imageFmtAction.triggered.connect(self.setImage)

        # Add toolbar actions
        spacer = QWidget(self.toolBar)
        spacer.setSizePolicy(1|2|4,1|4)
        self.toolBar.addWidget(spacer)
        self.toolBar.addAction(self.closeAction)
        # Show window
        self.show()

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
        text = pattern + cur.selectedText()
        text = ('\n' + pattern).join(text.splitlines())
        cur.insertText(text)
        self.textEdit.setTextCursor(cur)

    def setLink(self):
        self.formatText('[', ']()')

    def setImage(self):
        self.formatText('![', ']()')

    def openFile(self):
        filename = QFileDialog.getOpenFileName(self, "Select File to Open", self.filename,
                                      "All Files (*);;Markdown Files (*.md);;HTML Files (*.html *.htm)" )
        if filename == '': return
        self.loadFile(filename)

    def loadFile(self, filename):
        with open(filename, 'r') as doc:
            text = doc.read()
        if filename.endswith('.md'):
            self.textEdit.highlighter.enableHighlighter(True)
        else:
            self.textEdit.highlighter.enableHighlighter(False)
        self.textEdit.setText(text)
        self.setWindowTitle(filename)
        self.filename = filename
        os.chdir(os.path.dirname(filename))
        self.previewModeAction.setChecked(False)
        self.togglePreviewMode(False)

    def saveFileAs(self):
        filename = QFileDialog.getSaveFileName(self, "Select File to Save", self.filename,
                                      "All Files (*);;Markdown Files (*.md)" )
        if filename == '': return
        self.filename = filename
        self.setWindowTitle(filename)
        self.saveFile()

    def saveFile(self):
        if self.filename == HOMEDIR:
            self.saveFileAs()
            return
        text = self.textEdit.toPlainText()
        with open(self.filename, 'w') as doc:
            doc.write(text)

    def exportHtml(self):
        name = os.path.splitext(self.filename)[0] + '.html'
        filename = QFileDialog.getSaveFileName(self, "Select File to Save", name,
                                      "HTML Files (*.html *.htm)" )
        if filename == '': return
        text = self.textEdit.toPlainText()
        html = markdown.markdown(text)
        with open(filename, 'w') as doc:
            doc.write(html)

    def togglePreviewMode(self, checked):
        if checked:
            text = self.textEdit.toPlainText()
            html = markdown.markdown(text)
            self.textEdit.hide()
            self.textView.show()
            self.textView.setHtml(html)
        else:
            self.textView.hide()
            self.textEdit.show()

class TextEdit(QTextEdit):
    def __init__(self, parent):
        QTextEdit.__init__(self, parent)
        self.setTabStopWidth(32)
        self.highlighter = highlighter.MarkdownHighlighter(self)

class TextView(QTextEdit):
    def __init__(self, parent):
        QTextEdit.__init__(self, parent)
        self.setTabStopWidth(32)

    def loadResource(self, res_type, url):
        """ this function is reimplemented and called internally by QTextEdit """
        if res_type == 2 and os.path.exists(url.toString()):
            #print(url.toString())
            img_file = open(url.toString(), 'rb')
            data = img_file.read()
            img_file.close()
            #self.document().addResource(res_type, url, QtCore.QVariant(data))
            #self.viewport().update()    # force repaint to show image
        return QTextEdit.loadResource(self, res_type, url)

def main():
    app = QApplication(sys.argv)
    win = Window()
    if len(sys.argv)>1 and os.path.exists(os.path.abspath(sys.argv[-1])):
        win.loadFile(os.path.abspath(sys.argv[-1]))
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
