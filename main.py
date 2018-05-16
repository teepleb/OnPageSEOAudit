import requests
import sys
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


class Page():
    def __init__(self, url):
        self.url = url
        self.page_source = ""

    def requestPage(self):
        return requests.get(self.url)

    def getPageSource(self):
        if self.page_source != "":
            return self.page_source
        else:
            self.page_source = self.requestPage().text
            return self.page_source

class Parser():
    def __init__(self, page_source):
        self.title = ""
        self.desc = ""
        self.canonical = ""
        self.headers = {}
        self.parseHTML(page_source)
    
    def parseHTML(self, html_string):
        parsed_html = BeautifulSoup(html_string, "lxml")
        self.title = parsed_html.head.find('title').text
        self.desc = parsed_html.head.find('meta', attrs={'name': 'description'})['content']
        self.canonical = parsed_html.head.find('link', attrs={'rel': 'canonical'})['href']

    @property
    def getTitle(self):
        return self.title

    @property
    def getDesc(self):
        return self.desc

    @property
    def getCanonical(self):
        return self.canonical

    @property
    def getHeaders(self):
        return self.headers

def printIntro(section_title):
    # This function will print the header for each section in a nicer way, for now.
    print("\n")
    print("---" * 5 + "-" * (len(section_title) + 2) + "---" * 5)
    print("***" * 5 + " " + section_title + " " + "***" * 5)
    print("---" * 5 + "-" * (len(section_title) + 2) + "---" * 5)

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print("No URL was provided, please try again and enter a valid URL.")
    else:
        current_page = Page(sys.argv[1])
        parser = Parser(current_page.getPageSource())


        printIntro("TITLE")
        # title - content, length, etc.
        
        if len(parser.getTitle) >= 60:
            print("Your TITLE is: {0}".format(parser.getTitle))
            print("WARNING: Your TITLE tag is too long. You should reduce it to be less than 60 characters.")
        elif len(parser.getTitle) <= 0:
            print("WARNING: You currently do not have a TITLE tag, you should add one.")
        else:
            print("Your TITLE is: {0}".format(parser.getTitle))
        
        printIntro("DESCRIPTION")
        # description - content, length, etc.
        print("Your DESC is: {0}".format(parser.getDesc))
        if len(parser.getDesc) >= 300:
            print("WARNING: Your DESC is too long. You should reduce it to be less than 300 characters for best display.")
        elif len(parser.getDesc) <= 50:
            print("WARNING: You're missing out on SERP space! Add some more content to your description. Keep in mind it needs to be between 50-300 characters for best performance.")

        printIntro("CANONICAL")
        # canonicals - url
        print("Your CANONICAL is: {0}".format(parser.getCanonical))
        if parser.getCanonical != current_page.url:
            print("WARNING: Your current canonical does not match the page URL submitted.")
        elif parser.getCanonical == "":
            print("WARNING: You do not have a proper canonical setup on the page.")

        printIntro("STRUCTURED DATA")
        # schema, open graph, twitter cards, etc.

        printIntro("HEADERS")
        # header tags (h1 x 1, h2, h3, etc.) - need to show frequency, h1 highest on page, and header tag content
        if parser.getHeaders:
            print("HEADERS")

        printIntro("INTERNAL LINKING")
        # on page linking - internal vs external, no follow vs follow, broken links, no special chars in urls aka they are friendly

        printIntro("BACKLINKS")
        # backlinks to page (future?)

        printIntro("ROBOTS.TXT")
        # double check for robots.txt

        printIntro("SITEMAP")
        # double check for sitemap
        # double check for Google Analytics
        # check page rendering for mobile
        # check page speed test
        # check external resources & show page size
        # display resource #s - html objects, js resources, css resources, images, other
        # are images optimized
        # does it pass W3C
        # does it us inline styling
        # is the page secure