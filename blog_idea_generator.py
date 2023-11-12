import requests #used to download raw xml data from napkintheory's feed
import xml.etree.ElementTree as ET #used to iterate the raw xml file
from lxml.html import fromstring #used to clean-up the html formatting, so i am left with clean text
from openai import OpenAI


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

titlesText = ""
descriptionText = ""
contentText = ""
i = 1

# iterate the child and search for 'item' identifiers -- they contain the actual article data

for item in root.iter('item'):
    title = fromstring(item[0].text).text_content()
    subtitle = fromstring(item[1].text).text_content()
    article = fromstring(item[7].text).text_content()

    titles.append(title) #title
    titlesText += "title " + str(i) + ": " + title + "\n"
    
    description.append(subtitle) #description
    descriptionText += "description " + str(i) + ": " + subtitle + "\n"
    
    content.append(article) #content
    contentText += "content " + str(i) + ": " + article + "\n"

    i+=1


# note data is already clean by this point, using lxml.html api (live saver), integrating with openai api

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a blog idea generator based on the content the user will submit. Provide some topics they could write about, but not the of ANY topics the input given is related too."},
        {"role": "user", "content": "educate me my boi" + titlesText + descriptionText + "remember no topics about what is given to you, think what other NON RELATED topics they could enjoy writing about"}
    ]
)
print(response.choices[0].message)
