import re
from bs4 import BeautifulSoup

__author__ = 'laurent'


def bs_preprocess(html):
    """remove distracting whitespaces and newline characters"""
    pat = re.compile('(^[\s]+)|([\s]+$)', re.MULTILINE)
    html = re.sub(pat, '', html)        # remove leading and trailing whitespaces
    html = re.sub('\n', ' ', html)      # convert newlines to spaces (this preserves newline delimiters)
    html = re.sub('[\s]+<', '<', html)  # remove whitespaces before opening tags
    html = re.sub('>[\s]+', '>', html)  # remove whitespaces after closing tags
    return html


def squeeze_ordered_lists(html):
    """collapse successive <ol> tags with 'start' attribute
       <ol><li>1</li></ol><ol start="2"><li>2</li></ol> -> <ol><li>1</li><li>2</li></ol>"""
    # TODO Using regexp with HTML is very dirty. Try to do it with BeautifulSoup instead.
    pat = re.compile('</ol>[\s]*<ol .*? start="[\d]+">')
    html = re.sub(pat, '', html)
    return html

with open('Starting_Talend_Studio.htm', encoding='utf-8') as file:
    html = file.read()
    # html = bs_preprocess(html)
    html = squeeze_ordered_lists(html)
    soup = BeautifulSoup(html, 'html.parser')

# Trim leading and trailing and spaces in paragraphs
# for p in soup.find_all('p'):
#     if p.string:
#         p.string.replace_with(p.string.strip())

# Remove empty (or whitespaced) p tags with no children
for tag in soup.findAll(lambda tag: tag.name == 'p' and tag.find(True) is None and (tag.string is None or not tag.string.strip())):
    tag.extract()

# Remove <br/> tags
for tag in soup.find_all('br'):
    tag.extract()

# Replace <b> tags with <span class="Emphasis">
for tag in soup.find_all('b'):
    new_tag = soup.new_tag('span')
    new_tag.string = tag.string
    new_tag['class'] = 'Emphasis'
    tag.replace_with(new_tag)

# Replace <span style="font-weight: bold;"> tags with <span class="Emphasis">
for tag in soup.find_all('span', attrs={'style': 'font-weight: bold;'}):
    tag['class'] = 'Emphasis'
    del tag['style']

# Remove local formatting from <h1> tags
for tag in soup.find_all(lambda tag: tag.name == 'h1' and tag.has_attr('style')):
    del tag['style']

# Remove local formatting from <ol> tags
for tag in soup.find_all(lambda tag: tag.name == 'ol' and tag.has_attr('style')):
    del tag['style']

# Wrap <li> content with <p> when content is only text
for tag in soup.findAll(lambda tag: tag.name == 'li' and tag.find(True) is None):
    tag.string.wrap(soup.new_tag('p'))

# Unwrap <img> tags inside of <p> tags inside <li> tags
# <li>...<p><img></img></p>...</li> -> <li>...<img></img></li>
for tag in soup.select('li > p > img'):
    tag.parent.unwrap()

# Output sanitized html
with open('output.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))
