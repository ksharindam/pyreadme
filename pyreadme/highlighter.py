# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MarkdownHighlighter(QSyntaxHighlighter):


    def __init__(self, parent=None):

        super(MarkdownHighlighter, self).__init__(parent)
        self.highlighter_enabled = True

        self.font_color             = '#000'
        self.link_color             = '#0000FF'
        self.code_color             = '#000'
        self.code_bg_color          = '#bbb'
        self.code_block_color       = '#8b0000'

        self.formatting_dict = {'bold': self.applyBold, 'italic': self.applyItalic, 'link': self.applyLink,
                                'inline-code': self.applyInlineCode, 'code-block': self.applyCodeBlock,
                                'h1': self.applyH1, 'h2': self.applyH2, 'h3': self.applyH3,
                                'h4': self.applyH4, 'h5': self.applyH5, 'h6': self.applyH6 }

        self.highlightingRules = []

        # Headers
        self.highlightingRules.append((QRegExp("^#[^#].*$"), 'h1'))
        self.highlightingRules.append((QRegExp("^##[^#].*$"), 'h2'))
        self.highlightingRules.append((QRegExp("^###[^#].*$"), 'h3'))
        self.highlightingRules.append((QRegExp("^####[^#].*$"), 'h4'))
        self.highlightingRules.append((QRegExp("^#####[^#].*$"), 'h5'))
        self.highlightingRules.append((QRegExp("^######.*$"), 'h6'))
        
        # font 
        #fontReg = QRegExp(".")
        #fontReg.setMinimal(True)
        #self.highlightingRules.append((fontReg, 'font'))

        # italic        
        italicReg = QRegExp("(_.+_)|([^*]\*[^*].*[^*]\*[^*])")
        italicReg.setMinimal(True)
        self.highlightingRules.append((italicReg, 'italic')) 

        # bold        
        boldReg = QRegExp("\*\*.+\*\*")
        boldReg.setMinimal(True)
        self.highlightingRules.append((boldReg, 'bold'))

        # Link
        linkReg = QRegExp("\[.+\](\(.*\))")
        linkReg.setMinimal(True)
        self.highlightingRules.append((linkReg, 'link'))

        # Inline code
        codeReg = QRegExp("`.*`")
        codeReg.setMinimal(True)
        self.highlightingRules.append((codeReg, 'inline-code'))

        # Code Block
        self.highlightingRules.append((QRegExp("^    .+$"), 'code-block'))
        
    def applyBold(self, charFormat):
        charFormat.setFontWeight(75)
    def applyItalic(self, charFormat):
        charFormat.setFontItalic(True)
    def applyLink(self, charFormat):
        charFormat.setForeground(QColor(self.link_color))
    def applyCodeBlock(self, charFormat):
        charFormat.setForeground(QColor(self.code_block_color))
        charFormat.setFontFamily('Monospace')
    def applyInlineCode(self, charFormat):
        charFormat.setForeground(QColor(self.code_color))
        charFormat.setBackground(QColor(self.code_bg_color))
        charFormat.setFontFamily('Monospace')
    def applyH1(self, charFormat):
        charFormat.setFontPointSize(28)
    def applyH2(self, charFormat):
        charFormat.setFontPointSize(24)
    def applyH3(self, charFormat):
        charFormat.setFontPointSize(20)
    def applyH4(self, charFormat):
        charFormat.setFontPointSize(18)
    def applyH5(self, charFormat):
        charFormat.setFontPointSize(16)
    def applyH6(self, charFormat):
        charFormat.setFontPointSize(14)

    def getFormat(self, format_list):
        charFormat = QTextCharFormat()
        for format in format_list:
            self.formatting_dict[format](charFormat)
        return charFormat

    def highlightBlock(self, text):
        """ HighlightBlock became complex due to implementation of combined formatting 
            a quick _brown fox **jumps over** the lazy__ dog
            above markdown text has brown fox with only itaic and jumps over with bold-italic
            formats.
            In this case for each type of formatting start and end pos of each text block is
            stored in a list (formatted_blocks). Then an start/end to next start/end pos is
            considered as a text block, then all required formattings are applied to that block"""
        if not self.highlighter_enabled: return

        self.setCurrentBlockState(0)
        formatted_blocks = []
        for expression, format in self.highlightingRules:
            index = expression.indexIn(text)
            
            while index >= 0:

                length = expression.matchedLength()
                formatted_blocks.append([index, index+length, format])
                index = expression.indexIn(text, index + length)

        indices = []
        for item in formatted_blocks:
            indices += [item[0], item[1]]
        indices.sort()
        for i, pos in enumerate(indices):
            if i == len(indices) - 1 : break
            format_list = []
            for each in formatted_blocks:
                if each[0] <= pos < each[1]:
                    format_list.append(each[2])
            format = self.getFormat(format_list)
            self.setFormat(pos, indices[i+1]-pos, format)

    def enableHighlighter(self, enable):
        self.highlighter_enabled = enable

