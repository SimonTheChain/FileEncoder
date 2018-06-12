#!/usr/bin/python
# -*- coding: utf-8 -*-

# File Encoder
#
# Author: Simon Lachaîne


import sys
import io
import file_encoder_ui as main_frame
from PyQt5 import QtWidgets
from chardet.universaldetector import UniversalDetector


ENCODINGS = [
    "iso-8859-15",
    "utf-8",
]


def show_message(text):
    msg = QtWidgets.QMessageBox()

    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(text)
    msg.setWindowTitle("Input needed")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()


class TranscoderApp(QtWidgets.QMainWindow, main_frame.Ui_FileEncoder):
    def __init__(self, parent=None):
        super(TranscoderApp, self).__init__(parent=parent)

        self.source = ""
        self.destination = ""
        self.directory = ""

        self.setupUi(self)

        self.source_btn.clicked.connect(self.source_dlg)
        self.destination_btn.clicked.connect(self.destination_dlg)
        self.encoding_combo.addItems(ENCODINGS)
        self.transcode_btn.clicked.connect(self.transcode)

        self.show()

    def source_dlg(self):
        self.source = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption="Please select a source file",
            directory=self.directory
        )

        if self.source:
            self.source_lbl.setText(self.source[0])
            detector = UniversalDetector()
            self.progress.setValue(0)

            with io.open(self.source[0], "rb") as source_file:

                line_nb = 1
                for line in source_file.readlines():
                    self.encoding_lbl.setText("Processing line number " + str(line_nb))
                    detector.feed(line)
                    line_nb += 1

                    if detector.done:
                        break

            detector.close()

            if not detector.result["encoding"]:
                self.encoding_lbl.setText("Unable to decode")

            else:
                self.encoding_lbl.setText(detector.result['encoding'])
                confidence = int(detector.result['confidence'] * 100)
                self.lcd.display(confidence)
                self.progress.setValue(confidence)

    def destination_dlg(self):
        self.destination = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption="Please select a destination and name for the new file",
            directory=self.directory
        )

        if self.destination:
            self.destination_lbl.setText(self.destination[0])

    def transcode(self):
        with io.open(self.source[0], "r") as source_file:
            with io.open(self.destination[0], "w", encoding=self.encoding_combo.currentText()) as new_file:
                new_file.write(source_file.read())


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = TranscoderApp()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
