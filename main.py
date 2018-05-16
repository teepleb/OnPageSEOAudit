import requests
import sys


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
    def __init__(self):
        self.title = ""
        self.desc = ""
        self.canonical = ""
    
    def parseHTML(self, html_string):
        self.title = "Testing Title"
        self.desc = "This is a description example or sample."
        self.canonical = "websiteurl"
    @property
    def getTitle(self):
        return self.title
    @property
    def getDesc(self):
        return self.desc
    @property
    def getCanonical(self):
        return self.canonical

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print("No URL was provided, please try again and enter a valid URL.")
    else:
        current_page = Page(sys.argv[1])
        html_parser = Parser()
        page_source = current_page.getPageSource()

        html_parser.parseHTML(page_source)
        
        print("\n" * 3)
        print("***" * 5 + " TITLE " + "***" * 5)
        # title - content, length, etc.
        print("Your TITLE is: {0}".format(html_parser.getTitle))
        if len(html_parser.getTitle) >= 60:
            print("WARNING: Your TITLE tag is too long. You should reduce it to be less than 60 characters.")
        elif len(html_parser.getTitle) <= 0:
            print("WARNING: You currently do not have a TITLE tag, you should add one.")
        
        print("\n" * 3)        
        print("***" * 5 + " DESCRIPTION " + "***" * 5)
        # description - content, length, etc.
        print("Your DESC is: {0}".format(html_parser.getDesc))
        if len(html_parser.getDesc) >= 300:
            print("WARNING: Your DESC is too long. You should reduce it to be less than 300 characters for best display.")
        elif len(html_parser.getDesc) <= 50:
            print("WARNING: You're missing out on SERP space! Add some more content to your description. Keep in mind it needs to be between 50-300 characters for best performance.")

        print("\n" * 3)
        print("***" * 5 + " CANONICALS " + "***" * 5)
        # canonicals - url
        print("Your CANONICAL is: {0}".format(html_parser.getCanonical))

        # schema, open graph, twitter cards, etc.
        # header tags (h1 x 1, h2, h3, etc.) - need to show frequency, h1 highest on page, and header tag content
        # on page linking - internal vs external, no follow vs follow, broken links, no special chars in urls aka they are friendly
        # backlinks to page (future?)
        # double check for robots.txt
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
