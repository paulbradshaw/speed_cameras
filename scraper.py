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
# this line uses xpath, which is supported by lxml.etree (which has created root) to grab the contents of any <text tags and put them all in a list variable called 'lines'
lines = root.findall('.//text')
    #create an empty dictionary variable called 'record'
record = {}
# loop through each item in the list, and assign it to a variable called 'line'
for line in lines:
    #create a variable called 'fontvalue', and use the get method to give it the value of the <font attribute of 'line'
    fontvalue = line.get("font")
    #print that variable
    print fontvalue
    #if that variable has a value of '3'
    if fontvalue == "3":
        #create a variable called 'date', use the find method to grab the contents of any <b> tag (identified with XPath) in 'line', grab the text within that, and store it in the variable
        date = line.find('.//b').text
        #continue on to next if statement
        continue
    #if 'fontvalue' is 5 AND the length of the text in 'line' is less than 5 characters (counted with the len function)    
    if fontvalue == "5" and len(line.text)<5:
        #grab the text in 'line' and put it in a new variable called 'code'
        code = line.text
        continue
    #if 'fontvalue' is 5 AND the length of the text in 'line' is more than 4 characters
    if fontvalue == "5" and len(line.text)>4:
        #grab the text in 'line' and store it in a field called 'location' in the dictionary variable 'record'
        record["location"] = line.text
        #store the value of the 'date' variable in a field called 'date' in the dictionary variable 'record'
        record["date"] = date
        #store the value of the 'code' variable in a field called 'code' in the dictionary variable 'record'
        record["code"] = code
        #print the value of 'record'
        print record
        #save those values in scraperwiki's sqlite database, with 'code' as the unique key
        scraperwiki.sqlite.save(['code'], record)
