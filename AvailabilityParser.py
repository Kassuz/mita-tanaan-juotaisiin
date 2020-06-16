from html.parser import HTMLParser

# Parses html file and extracts a specific json from it 

class AvailabilityParser(HTMLParser):
    extractData = False
    jsonData = ""
    
    def handle_starttag(self, tag, attrs):
        if tag == "script" and len(attrs) == 2 and attrs[0][1] == "application/json" and attrs[1][0] == "data-stock-data":
            self.extractData = True
    
    def handle_data(self, data):
        if self.extractData:
            self.jsonData = data
    
    def handle_endtag(self, tag):
        if self.extractData and tag == "script":
            self.extractData = False