import os
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom

FEED_AUTHOR = "mat"
FEED_NAME = "mat@home"
FEED_DESC = "mat messing with music at home"
FEED_URL = "https://leplatrem.github.io/mixx/rss.xml"
FEED_BASE_URL = "https://leplatrem.github.io/mixx/"

ALLOWED_EXT = (".mp3",".mp4")
INPUT_DIR = os.getenv("INPUT_DIR", "media")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "rss.xml")

items = []

for filename in os.listdir(INPUT_DIR):
    if filename.lower().endswith(ALLOWED_EXT):
        path = os.path.join(INPUT_DIR, filename)
        if os.path.isfile(path):
            item = {
                "title": os.path.splitext(filename)[0],
                "name": filename,
                "timestamp": os.path.getctime(path),
            }
            items.append(item)

items.sort(key=lambda x: x["timestamp"], reverse=True)

rss = Element("rss", version="2.0", attrib={"xmlns:atom": "http://www.w3.org/2005/Atom"})
channel = SubElement(rss, "channel")
SubElement(channel, "title").text = FEED_NAME
SubElement(channel, "link").text = FEED_URL
SubElement(channel, "description").text = FEED_DESC
SubElement(channel, "author").text = FEED_AUTHOR
SubElement(channel, "atom:link", href=FEED_URL, rel="self", type="application/rss+xml")

for item in items:
    entry = SubElement(channel, "item")
    SubElement(entry, "title").text = item["title"]
    SubElement(entry, "link").text = f"{FEED_BASE_URL}{item['name']}"
    SubElement(entry, "guid").text = f"{FEED_BASE_URL}{item['name']}"
    pubDate = datetime.fromtimestamp(item["timestamp"]).strftime("%a, %d %b %Y %H:%M:%S %z")
    SubElement(entry, "pubDate").text = pubDate

rss_str = xml.dom.minidom.parseString(tostring(rss)).toprettyxml(indent="  ")

parent = os.path.dirname(OUTPUT_FILE)
if parent:
    os.makedirs(parent, exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(rss_str)

print(f"RSS feed generated at {OUTPUT_FILE}")
