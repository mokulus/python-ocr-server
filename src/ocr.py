import os
import subprocess


class OcrRunner:
    def __init__(self, filename):
        self.filename = filename
        self._text = None

    def run(self):
        subprocess.run(["tesseract", self.filename, self._base_output_name()])
        with open(self._txt_output_name()) as file:
            text = "".join(file.readlines())
        os.remove(self._txt_output_name())
        self._text = text
        return text

    def text(self):
        return self._text

    def _base_output_name(self):
        return f"{self.filename}.tess"

    def _txt_output_name(self):
        return f"{self._base_output_name()}.txt"