from lxml import etree
import os
from urllib.parse import urlparse
from testsuite_app.models import *
import zipfile
import tempfile
from . import db_helper

EPUB_NS = "http://www.idpf.org/2007/ops"
OPF_NS = "http://www.idpf.org/2007/opf"
XHTML_NS = "http://www.w3.org/1999/xhtml"
CONTAINER_NS = "urn:oasis:names:tc:opendocument:xmlns:container"
DC_NS = "http://purl.org/dc/elements/1.1/"
NSMAP = {"epub": EPUB_NS, "opf": OPF_NS, "xhtml": XHTML_NS, "odc": CONTAINER_NS, "dc": DC_NS}

# helper function
def parse_xml(path):
    p = etree.XMLParser(remove_blank_text = True)
    f = open(path)
    fdata = f.read()
    return etree.XML(fdata.encode('utf-8'), parser = p)


class EpubParser:

    def __init__(self):
        self.dirname = ""
        self.description = ""
        self.title = ""
        self.folder = ""
        self.testsuite = None
        self.filename = ""
        self.epub = None # the database object representing this epub
        self.epubid = ""
        self.category = None

    def parse(self, filename, category, testsuite):
        # first, extract the file to a temp folder
        zip = zipfile.ZipFile(filename)
        tempdir = tempfile.mkdtemp()
        zip.extractall(tempdir)
        
        self.filename = os.path.basename(filename)
        self.folder = tempdir
        self.testsuite = testsuite
        self.category = category
        opfpath = self.parse_container()
        self.epub = db_helper.add_epub(self.epubid, self.title, self.description, category, filename)
        navpath = self.parse_opf(opfpath)
        
        self.parse_nav(navpath)

    # return the OPF path
    def parse_container(self):
        full_container_path = os.path.join(self.folder, "META-INF/container.xml")
        doc = parse_xml(full_container_path)
        opf_path = doc.xpath("//odc:rootfile[@media-type='application/oebps-package+xml']/@full-path", namespaces = NSMAP)[0]
        return os.path.join(self.folder, opf_path)

    def parse_opf(self, opfpath):
        doc = parse_xml(opfpath)
        # TODO this probably won't work for a list of space-separated @properties values
        navpath = doc.xpath("//*[@properties='nav']/@href")[0]
        navpath = os.path.join(os.path.dirname(opfpath), navpath)
        self.description = doc.xpath("//dc:description/text()", namespaces = NSMAP)[0]
        self.title = doc.xpath("//dc:title/text()", namespaces = NSMAP)[0]
        self.epubid = doc.xpath("//dc:identifier[@id='uid']/text()", namespaces=NSMAP)[0]
        return navpath

    def parse_nav(self, navpath):
        print("Parsing {0}".format(navpath))
        self.dirname = os.path.dirname(navpath)
        navdoc = parse_xml(navpath)
        toc_elm = navdoc.xpath("//xhtml:nav[@epub:type='toc']/xhtml:ol", namespaces = NSMAP)[0]
        self.process_toc(toc_elm, self.category)

    """read the Nav document into a database
    approach:
    1. look at every li
    2. if it's not a test, throw it out
    3. if it is a test, add it to the database

    elm: <ol>"""
    def process_toc(self, elm, epub):
        order_in_book = 0
        for li in elm.xpath("//xhtml:nav[@epub:type='toc']//xhtml:li", namespaces = NSMAP):
            xpathres = li.xpath("xhtml:a/@href", namespaces = NSMAP)
            test_section = None
            if len(xpathres) != 0:
                href = xpathres[0]
                uri = urlparse(os.path.join(self.dirname, href))
                test_section = self.get_test(uri)
                if test_section != None:
                    xhtml = etree.tostring(test_section).strip() # trim whitespace
                    name = self.get_label(li)
                    desc = self.get_desc(test_section)
                    testid = uri.fragment
                    required = test_section.attrib['class'].find('ctest') != -1
                    foldername = os.path.basename(self.folder)
                    adv = test_section.attrib['class'].find('atest') != -1
                    allow_na = test_section.attrib['class'].find('allow-na') != -1
                    db_helper.add_test(name, desc, self.category, required, 
                        testid, self.testsuite, xhtml, self.epub, adv, allow_na, order_in_book)
                    order_in_book += 1

    # if the URI points to a test: return the test's section element
    # note: uri is absolute
    def get_test(self, uri):
        if uri.fragment == "":
            #print "Not a test: {0}".format(uri.path)
            return None
        doc = parse_xml(uri.path)
        xpathres = doc.xpath("//*[@id='{0}']".format(uri.fragment))
        if len(xpathres) == 0:
            print("Not found: {0}".format(uri.fragment))
            return None
        elm = xpathres[0]
        if elm.attrib.has_key('class') == False:
            return None

        #ftest and atest are for accessibility
        if elm.attrib['class'].find('ctest') != -1 \
            or elm.attrib['class'].find('otest') != -1 \
            or elm.attrib['class'].find('ftest') != -1 \
            or elm.attrib['class'].find('atest') != -1: 
            return elm
        else:
            return None


    # assumption: structure is <li><a><..>label</..></a>
    def get_label(self, elm):
        stringify = etree.XPath("string()")
        label = stringify(elm.xpath("xhtml:a", namespaces = NSMAP)[0])
        if label == None:
            s = etree.tostring(elm, pretty_print = True)
            print("** Warning: no label for element: ")
            print("\t{0}".format(s))
        return label

    # elm is a section
    # return the contents of the child element with @class='desc'
    def get_desc(self, elm):
        desc_elm = elm.xpath("descendant::*[@class = 'desc']", namespaces = NSMAP)[0]
        stringify = etree.XPath("string()")
        desc = stringify(desc_elm)
        return desc




