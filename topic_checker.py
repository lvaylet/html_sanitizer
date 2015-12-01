import os
import sys
from bs4 import BeautifulSoup

__author__ = 'laurent'

if sys.platform == 'win32':
    topDir = r'C:\Users\lvaylet\Documents\My Projects\esb-basics\Content\Labs'
else:
    topDir = r'/Users/laurent/Documents/GitHub/training-esb-basics/Content/Labs'
print(topDir)

extensionToSearchFor = '.htm'

for dirPath, dirNames, files in os.walk(topDir):
    for f in files:
        if f.lower().endswith(extensionToSearchFor):
            htmFileName = os.path.join(dirPath, f)
            print("Processing " + htmFileName + "...")
            with open(htmFileName, 'r', encoding='utf-8') as htmFile:
                html = htmFile.read()
                soup = BeautifulSoup(html, 'html.parser')

                # Make sure every topic ends with a "Next Step" h3 header wrapping a link
                def has_well_formatted_next_step(tag):
                    return tag.name == 'h3' and tag.string == 'Next Step' and tag.next_sibling.find('a') is not None
                if soup.find(has_well_formatted_next_step) is None:
                    print("  WARNING: No well-formatted 'Next Step' header found. It might be missing, mistyped or lacking a link to the next section.")
