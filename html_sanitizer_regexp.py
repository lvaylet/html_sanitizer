import re
import os
import sys

__author__ = 'laurent'

html = """
<?xml version="1.0" encoding="utf-8"?>
<html xmlns:MadCap="http://www.madcapsoftware.com/Schemas/MadCap.xsd">
  <head>
    <title>Deploying services from TAC</title>
  </head>
  <body>
    <h2>Publishing Services from TAC</h2>
    <p>&#160;</p>
    <h3>Overview</h3>
    <p>&#160;</p>
    <p>In this lab, you will discover how a user with Operation Manager privileges can use the Publisher to publish a service to Nexus and then deploy these services with the ESB Conductor.</p>
    <h3>Modifying the services</h3>
    <p>In order to be sure that your service has been deployed, you will make few changes in the simpleSOAP and simpleREST_readyToDeploy services.</p>
    <ol style="list-style: decimal;">
      <li>In the Studio in the <span style="font-weight: bold;">Repository</span>, in <strong>Services</strong>, double-click <strong>simpleSOAPPortType_simpleSOAPOperation</strong>.</li>
      <li><p>Double-click the <strong>tXMLMap</strong> component to open the Map editor.</p></li>
      <li>In the 
      <strong>response</strong> table, click 
      <span class="code">(...)</span> to edit the <strong>out</strong> field.</li>
    </ol>
    <ol MadCap:continue="true">
      <li>
        In the 
        <strong>Expression builder</strong>, modify the string as follows:
        <p><img src="../../Resources/Images/DeployTAC_ModifyingSvc_expBuilder_SOAP.png" /></p>
      </li>
      <li>Click 
      <strong>OK</strong> and then click <strong>OK</strong> to save the new mapping.</li>
    </ol>
    <ol start="6">
      <li>Save the service.</li>
    </ol>
    <p><span style="font-style: italic;">Note</span> Go to the Wrap-Up section for a quick summary of the concepts reviewed in this lesson.</p>
  </body>
</html>
"""

# Remove &#160; characters
html = re.sub(r'&#160;', r' ', html)

# Replace bold and italic styles with proper HTML5 tags <strong> and <em>
html = re.sub(r'<span style="font-weight: bold;">(.*?)</span>', r'<strong>\1</strong>', html)
html = re.sub(r'<span style="font-style: italic;">(.*?)</span>', r'<em>\1</em>', html)
html = re.sub(r'<span class="Emphasis">(.*?)</span>', r'<strong>\1</strong>', html)
html = re.sub(r'<b>(.*?)</b>', r'<strong>\1</strong>', html)
html = re.sub(r'<i>(.*?)</i>', r'<em>\1</em>', html)

# Capitalize span.Code class
html = re.sub(r'<span class="code">', r'<span class="Code">', html)

# Clean up and squeeze ordered and unordered lists
html = re.sub(r' style="list-style: decimal;"', r'', html)
html = re.sub(r'</ol>\s*<ol MadCap:continue="true">', r'', html)
html = re.sub(r'</ol>\s*<ol start="\d+">', r'', html)

# Adjust whitespaces around <strong>, <em> and <span> tags
html = re.sub(r'\n\s+<strong>', r'<strong>', html)
html = re.sub(r'\n\s+<em>', r'<em>', html)
html = re.sub(r'\n\s+<span', r'<span', html)

# Wrap text-only (i.e. no images) <li> tags with <p> tags
html = re.sub(r'<li>([^<].*?)</li>', r'<li><p>\1</p></li>', html)

# Remove existing <p> tags around <img> tags...
html = re.sub(r'<p>(<img.*?/>)</p>', r'\1', html)
# ... and add them back, while also wrapping the neighbors with <p> tags
html = re.sub(r'(?s)<li>((?:(?!</li>).)*?)<img(.*?)/>(.*?)</li>', r'<li><p>\1</p><p><img\2/></p><p>\3</p></li>', html)
# Adjust whitespaces around <p> tags
html = re.sub(r'<p>\n\s*', r'<p>', html)
html = re.sub(r'\n\s*</p>', r'</p>', html)
# Remove empty <p> tags
html = re.sub(r'<p>\s*</p>', r'', html)

#html = re.sub(r'(\s*)<li><p>', r'\1<li>\1  <p>', html)

print(html)

if sys.platform == 'win32':
    topDir = r'C:\Users\lvaylet\Documents\My Projects\esb-advanced\Content\Labs'
else:
    topDir = r'/Users/laurent/Documents/GitHub/training-esb-advanced/Content/Labs'
extensionToSearchFor = '.htm'

for dirPath, dirNames, files in os.walk(topDir):
    for f in files:
        if f.lower().endswith(extensionToSearchFor):
            print(os.path.join(dirPath, f))
            with open(os.path.join(dirPath, f), 'r', encoding='utf-8') as htmFile:
                html = htmFile.read()
                #print(html)
