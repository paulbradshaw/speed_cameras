#import our libraries
import scraperwiki
import urllib2
import lxml.etree

#create a variable called 'url' and then read what's there
url = "http://www.staffssaferroads.co.uk/media/114997/03092012_forwebsite.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

#convert to xml and print some info
xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
root = lxml.etree.fromstring(xmldata)

# this line uses xpath to find <text tags
# once this failed with 'Last run failed 2 minutes ago with status code 128'. 
#Editing the code and re-running solved it, as suggested at https://stackoverflow.com/questions/16721629/jenkins-returned-status-code-128-with-github
lines = root.findall('.//text[@font="5"]')
record = {}
for line in lines:
    #if the object is less than 5 characters long
    if len(line.text)<5:
        code = line.text
        print record
    #if the object is more than 4 chars
    if len(line.text)>4:
        record["location"] = line.text
        record["code"] = code
        print record
        scraperwiki.sqlite.save(['code'], record)
