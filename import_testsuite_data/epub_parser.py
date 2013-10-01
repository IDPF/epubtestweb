from lxml import etree
import os
from urlparse import urlparse
from testsuite_app.models import *
import import_db_helper

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
    return etree.XML(fdata, parser = p)


class EpubParser:

    def __init__(self):
        self.dirname = ""
        self.description = ""
        self.title = ""
        self.folder = ""
        self.testsuite = None
        self.epub_category = None # the book itself is a category
        self.restriction = 3

    def parse(self, folder, parent_category, testsuite, restriction):
        self.folder = folder
        self.testsuite = testsuite
        self.restriction = import_db_helper.category_restriction_to_int(restriction)
        opfpath = self.parse_container()
        navpath = self.parse_opf(opfpath)
        if self.restriction >= 2:
            self.epub_category = import_db_helper.add_category('2', self.title, parent_category, testsuite)
        else:
            self.epub_category = parent_category
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
        return navpath

    def parse_nav(self, navpath):
        print "Processing {0}".format(navpath)
        self.dirname = os.path.dirname(navpath)
        navdoc = parse_xml(navpath)
        toc_elm = navdoc.xpath("//xhtml:nav[@epub:type='toc']/xhtml:ol", namespaces = NSMAP)[0]
        self.process_toc(toc_elm, self.epub_category)

    """recursive function to read the Nav document into a database
    approach:
    1. look at every li
    2. if it's not a test, it's a category
    3. unless it contains no tests

    elm: <ol>
    parent_category: a models.Category object"""
    def process_toc(self, elm, parent_category):
        for c in elm.xpath("xhtml:li", namespaces = NSMAP):
            # Test or Category?
            xpathres = c.xpath("xhtml:a/@href", namespaces = NSMAP)
            test_section = None
            if len(xpathres) != 0:
                href = xpathres[0]
                uri = urlparse(os.path.join(self.dirname, href))
                test_section = self.get_test(uri)
                if test_section != None:
                    xhtml = etree.tostring(test_section).strip() # trim whitespace
                    name = self.get_label(c)
                    desc = self.get_desc(test_section)
                    testid = uri.fragment
                    required = test_section.attrib['class'].find('ctest') != -1
                    import_db_helper.add_test(name, desc, parent_category, required, testid, self.testsuite, xhtml)

            if test_section == None:
                # does this container eventually contain a test? otherwise we won't include it.
                if self.test_for_tests(c):
                    desc = self.get_label(c)
                    if self.restriction >= 3:
                        new_category = import_db_helper.add_category('3', desc, parent_category, self.testsuite)
                    else:
                        new_category = parent_category
                    # if this element has a nested list
                    # note that test list items don't have nested lists
                    nested_ol = c.xpath("xhtml:ol", namespaces = NSMAP)
                    if len(nested_ol) > 0:
                        self.process_toc(nested_ol[0], new_category)


    # does an <li> element contain tests?
    def test_for_tests(self, elm):
        child_links = elm.xpath("descendant::xhtml:li/xhtml:a/@href", namespaces = NSMAP)
        for a in child_links:
            uri = urlparse(os.path.join(self.dirname, a))
            if self.get_test(uri) != None:
                return True
        return False


    # if the URI points to a test: return the test's section element
    # note: uri is absolute
    def get_test(self, uri):
        if uri.fragment == "":
            #print "Not a test: {0}".format(uri.path)
            return None
        doc = parse_xml(uri.path)
        xpathres = doc.xpath("//*[@id='{0}']".format(uri.fragment))
        if len(xpathres) == 0:
            print "Not found: {0}".format(uri.fragment)
            return None
        elm = xpathres[0]
        if elm.attrib.has_key('class') == False:
            return None

        if elm.attrib['class'] == 'ctest' or elm.attrib['class'] == 'otest':
            return elm
        else:
            return None


    # assumption: structure is <li><a><..>label</..></a>
    def get_label(self, elm):
        stringify = etree.XPath("string()")
        label = stringify(elm.xpath("xhtml:a", namespaces = NSMAP)[0])
        if label == None:
            s = etree.tostring(elm, pretty_print = True)
            print "** Warning: no label for element: "
            print "\t{0}".format(s)
        return label

    # elm is a section
    # return the contents of the child element with @class='desc'
    def get_desc(self, elm):
        desc_elm = elm.xpath("descendant::*[@class = 'desc']", namespaces = NSMAP)[0]
        stringify = etree.XPath("string()")
        desc = stringify(desc_elm)
        return desc



