import os
from bs4 import BeautifulSoup

__author__ = 'laurent'


# A well-formatted 'Next Step' is made of a h3 header followed by a <p> tag containing an <a> tag
def has_well_formatted_next_step(tag):
    return tag.name == 'h3' \
           and tag.string == 'Next Step' \
           and tag.next_sibling.find('a') is not None

topDir = r'C:\Users\lvaylet\Documents\My Projects\esb-basics\Content\Labs'
extensionToSearchFor = '.htm'
filesToExclude = ['Description.htm', 'Wrap-Up.htm']

topicsWithNoNextStep = []

for dirPath, dirNames, files in os.walk(topDir):
    for f in files:
        if f not in filesToExclude and f.lower().endswith(extensionToSearchFor):
            htmFileName = os.path.join(dirPath, f)
            # print("Processing " + htmFileName + "...")
            with open(htmFileName, 'r', encoding='utf-8') as htmFile:
                html = htmFile.read()
                soup = BeautifulSoup(html, 'html.parser')

                # Make sure every Topic ends with a "Next Step" section
                if soup.find(has_well_formatted_next_step) is None:
                    topicsWithNoNextStep.append(htmFileName.replace(topDir, ''))

print("These Topics have no well-formatted 'Next Step' section. It might be missing, mistyped, using the wrong header "
      "level or lacking a link to the next section.")
print('  ' + '\n  '.join(topicsWithNoNextStep))
