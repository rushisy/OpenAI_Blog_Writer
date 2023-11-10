import requests #used to download raw xml data from napkintheory's feed
import xml.etree.ElementTree as ET #used to iterate the raw xml file
from lxml.html import fromstring #used to clean-up the html formatting, so i am left with clean text


# download rss feed from substack

link = "https://napkintheory.substack.com/feed"
f = requests.get(link)

# make a file and put the entire raw xml data into it
# note rss data and xml data are the same xml formatting, difference is rss is more recently uploaded data (useful).

f1 = open("feed.xml", "w") 
f1.write(f.text)
f1.close()
f.close()

# clean up data

tree = ET.parse('feed.xml')
root = tree.getroot()[0] #enter 'rss', start at 'channel' (bunch of item containers r in this child)

# make placeholders to input data into

titles = []
description = []
content = []

# iterate the child and search for 'item' identifiers -- they contain the actual article data

for item in root.iter('item'):
    titles.append(fromstring(item[0].text).text_content()) #title
    description.append(fromstring(item[1].text).text_content()) #description
    content.append(fromstring(item[7].text).text_content()) #content

# note data is already clean by this point, using lxml.html api (live saver)

print(titles)
print(description)
print(content)

#integrate w openai somehow