import os
from lxml import etree
import zipfile

class EpubIdCheck:
    file_id_map = {}

    def get_filename_for_id(self, id):
        return self.file_id_map[id]

    # make a list of IDs and the files they are in
    def process_epubs(self, folder):
        files = os.listdir(folder)
        for f in files:
            ext = os.path.splitext(f)[1]
            if ext == ".epub":
                print("Checking EPUB IDs {0}".format(f))
                zip = zipfile.ZipFile(os.path.join(folder, f))
                opf = zip.read('EPUB/package.opf')
                dom = etree.fromstring(opf)
                idelm = dom.xpath("*/*[@id='uid']")[0]
                self.file_id_map[idelm.text] = os.path.join(folder, f)

        # for k in self.file_id_map.keys():
        #     print "{0} : {1}".format(k, self.file_id_map[k])

