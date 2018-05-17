import requests
import sys
import re
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
        self.header_count = {"h1": 0, "h2": 0, "h3": 0, "h4": 0, "h5": 0, "h6": 0}
        self.headers = {}
        self.google_analytics = False
        self.image_count = 0
        self.is_secure = False
        self.parseHTML(page_source)
    
    def parseHTML(self, html_string):
        parsed_html = BeautifulSoup(html_string, "lxml")

        self.title = parsed_html.head.find('title').text

        self.desc = parsed_html.head.find('meta', attrs={'name': 'description'})['content']

        self.canonical = parsed_html.head.find('link', attrs={'rel': 'canonical'})['href']
    
        self.header_count['h1'] = len(parsed_html.body.find_all('h1'))
        self.header_count['h2'] = len(parsed_html.body.find_all('h2'))
        self.header_count['h3'] = len(parsed_html.body.find_all('h3'))
        self.header_count['h4'] = len(parsed_html.body.find_all('h4'))
        self.header_count['h5'] = len(parsed_html.body.find_all('h5'))
        self.header_count['h6'] = len(parsed_html.body.find_all('h6'))

        if self.header_count['h1'] > 1:
            self.headers['h1'] = []
            for value in parsed_html.body.find_all('h1'):
                self.headers['h1'].append(value.text)
        else:
            self.headers['h1'] = parsed_html.body.find('h1')

        if self.header_count['h2'] > 1:
            self.headers['h2'] = []
            for value in parsed_html.body.find_all('h2'):
                self.headers['h2'].append(value.text)
        else:
            self.headers['h2'] = parsed_html.body.find('h2')

        if self.header_count['h3'] > 1:
            self.headers['h3'] = []
            for value in parsed_html.body.find_all('h3'):
                self.headers['h3'].append(value.text)
        else:
            self.headers['h3'] = parsed_html.body.find('h3')

        if self.header_count['h4'] > 1:
            self.headers['h4'] = []
            for value in parsed_html.body.find_all('h4'):
                self.headers['h4'].append(value.text)
        else:
            self.headers['h4'] = parsed_html.body.find('h4')

        if self.header_count['h5'] > 1:
            self.headers['h5'] = []
            for value in parsed_html.body.find_all('h5'):
                self.headers['h5'].append(value.text)
        else:
            self.headers['h5'] = parsed_html.body.find('h5')

        if self.header_count['h6'] > 1:
            self.headers['h6'] = []
            for value in parsed_html.body.find_all('h6'):
                self.headers['h6'].append(value.text)
        else:
            self.headers['h6'] = parsed_html.body.find('h6')

        if parsed_html.head.find(text=re.compile('UA-')):
            self.google_analytics = True

        self.image_count = len(parsed_html.body.find_all('img'))

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
        return self.headers, self.header_count

    @property
    def getGoogleAnalytics(self):
        return self.google_analytics

    @property
    def getImageCount(self):
        return self.image_count


class PageSpeed(object):
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.endpoint = 'https://www.googleapis.com/pagespeedonline/v4/runPagespeed'

    def fetch(self, url, **kwargs):
        kwargs.setdefault('filter_third_party_resources', False)
        kwargs.setdefault('screenshot', False)
        kwargs.setdefault('strategy', 'desktop')

        params = kwargs.copy()
        params.update({'url': url})

        response = requests.get(self.endpoint, params=params)

        return PageSpeedResponse(response)

class PageSpeedResponse():
    def __init__(self, response):
        response.raise_for_status()

        self._response = response
        self._request = response.url
        self.json = response.json()

    @property
    def url(self):
        return self.json.get('id')

    @property
    def title(self):
        return self.json.get('title')

    @property
    def response_code(self):
        return self.json.get('responseCode')

    @property
    def speed(self):
        return self.json.get('ruleGroups').get('SPEED').get('score')

    @property
    def css_response_bytes(self):
        return self.json.get('pageStats').get('cssResponseBytes')

    @property
    def html_response_bytes(self):
        return self.json.get('pageStats').get('htmlResponseBytes')

    @property
    def image_response_bytes(self):
        return self.json.get('pageStats').get('imageResponseBytes')

    @property
    def javascript_response_bytes(self):
        return self.json.get('pageStats').get('javascriptResponseBytes')

    @property
    def number_css_resources(self):
        return self.json.get('pageStats').get('numberCssResources')

    @property
    def number_hosts(self):
        return self.json.get('pageStats').get('numberHosts')

    @property
    def number_js_resources(self):
        return self.json.get('pageStats').get('numberJsResources')

    @property
    def number_resources(self):
        return self.json.get('pageStats').get('numberResources')

    @property
    def number_static_resources(self):
        return self.json.get('pageStats').get('numberStaticResources')

    @property
    def other_response_bytes(self):
        return self.json.get('pageStats').get('otherResponseBytes')

    @property
    def text_response_bytes(self):
        return self.json.get('pageStats').get('textResponseBytes')

    @property
    def total_request_bytes(self):
        return self.json.get('pageStats').get('totalRequestBytes')

    @property
    def total_roundtrips(self):
        return self.json.get('pageStats').get('numTotalRoundTrips')

    @property
    def total_render_blocking_roundtrips(self):
        return self.json.get('pageStats').get('numRenderBlockingRoundTrips')


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
        page_speed = PageSpeed()
        page_speed_response = page_speed.fetch(current_page.url, strategy='desktop')


        printIntro("TITLE")
        # title - content, length, etc.
        
        if len(parser.getTitle) >= 60:
            print("Your TITLE is: {0}".format(parser.getTitle))
            print("\nWARNING: Your TITLE tag is too long. You should reduce it to be less than 60 characters.")
        elif len(parser.getTitle) <= 0:
            print("\nWARNING: You currently do not have a TITLE tag, you should add one.")
        else:
            print("Your TITLE is: {0}".format(parser.getTitle))
        
        printIntro("DESCRIPTION")
        # description - content, length, etc.
        print("Your DESC is: {0}".format(parser.getDesc))
        if len(parser.getDesc) > 160:
            print("\nWARNING: Your DESC is too long. You should reduce it to be less than 160 characters for best display.")
        elif len(parser.getDesc) <= 50:
            print("\nWARNING: You're missing out on SERP space! Add some more content to your description. Keep in mind it needs to be between 50-300 characters for best performance.")

        printIntro("CANONICAL")
        # canonicals - url
        print("Your CANONICAL is: {0}".format(parser.getCanonical))
        if parser.getCanonical != current_page.url:
            print("\nWARNING: Your current canonical does not match the page URL submitted.")
        elif parser.getCanonical == "":
            print("\nWARNING: You do not have a proper canonical setup on the page.")     

        printIntro("HEADERS")
        # header tags (h1 x 1, h2, h3, etc.) - need to show frequency, h1 highest on page, and header tag content
        print("The current amount of headers are: \n")
        if parser.getHeaders:
            headers, header_count = parser.getHeaders
            print("H1: {0}".format(header_count['h1']))
            print("H2: {0}".format(header_count['h2']))
            print("H3: {0}".format(header_count['h3']))
            print("H4: {0}".format(header_count['h4']))
            print("H5: {0}".format(header_count['h5']))
            print("H6: {0}".format(header_count['h6']))

            if header_count['h1'] > 1:
                print("\nFirst H1: {0}".format(headers['h1'][0].text))
                print("Remaining H1s:")
                for value in headers['h1']:
                    print(value)
                print("\nWARNING: You have more than one H1 on your page. Please reduce to having only one on the page.")
            elif header_count['h1'] == 0:
                print("\nWARNING: You do not have an H1 on your page, please add one.")
            else:
                print("\n First H1 -> {0}".format(headers['h1'].text))

        printIntro("INTERNAL LINKING")
        # on page linking - internal vs external, no follow vs follow, broken links, no special chars in urls aka they are friendly

        printIntro("GOOGLE ANALYTICS")
        # double check for Google Analytics
        if parser.getGoogleAnalytics == True:
            print("You have Google Analytics on your page.")
        else:
            print("WARNING: You do not have Google Analytics on your page, you should add that ASAP.")

        printIntro("MOBILE")
        # check page rendering for mobile

        printIntro("PAGE SPEED")
        # check page speed test
        print("Your page speed is: {0}/100".format(page_speed_response.speed))

        printIntro("EXTERNAL RESOURCES")
        # check external resources & show page size
        # display resource #s - html objects, js resources, css resources, images, other
        print("Your total external resources are: {0}".format(page_speed_response.number_resources))
        print("Your total external resource size is: {0}".format(page_speed_response.total_request_bytes))
        print("This page has {0} CSS resources that are {1} bytes in size.".format(page_speed_response.number_css_resources, page_speed_response.css_response_bytes))
        print("This page has {0} JS resources that are {1} bytes in size.".format(page_speed_response.number_js_resources, page_speed_response.javascript_response_bytes))
        print("This page has {0} IMAGE resources that are {1} bytes in size.".format(parser.getImageCount, page_speed_response.image_response_bytes))

        printIntro("EXTRA NOTES/WARNINGS")
        # does it us inline styling
        if '<style' in current_page.page_source:
            print("WARNING: You should limit your inline CSS as much as possible to reduce file bloat.")
        elif 'style=' in current_page.page_source:
            print("WARNING: You should limit your inline CSS as much as possible to reduce file bloat.")
            
        # is the page secure
        if not 'https' in current_page.url:
            print("WARNING: You should switch to HTTPS as soon as possible, this is critical in future Google updates.")
        # schema, open graph, twitter cards, etc.