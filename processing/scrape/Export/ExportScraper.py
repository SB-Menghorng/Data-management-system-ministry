import os.path

from processing.scrape.Export.Countries import Srilanka


class Export:
    def __init__(self, destinationDir):
        self.destination_dir = os.path.join(destinationDir, 'Export')

    def srilanka(self):
        Srilanka.exp_sri_lanka(os.path.join(self.destination_dir, 'Srilanka'))


# test = Export(r"D:\Intership\Labour ministry of combodain\demo")
# test.srilanka()
