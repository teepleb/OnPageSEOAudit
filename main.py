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
        pass
    
    def parseHTML(self, html_string):
        pass

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print("No URL was provided, please try again and enter a valid URL.")
    else:
        current_page = Page(sys.argv[1])
        page_source = current_page.getPageSource()
        
        # title - content, length, etc.
        
        # description - content, length, etc.
        # canonicals - url
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
