import os
import os.path
import re
import shutil

path = "C:\\temp"
files = os.listdir(path)

REGEXES = [(re.compile(r'<p>&#160;</p>'), ''),
           (re.compile(r'&#160;'), ''),
           (re.compile(r' style="list-style: decimal;"'), ''),
           (re.compile(r'</ol>\s*<ol MadCap:continue="true">'), ''),
           (re.compile(r'</ol>\s*<ol start="\d+">'), ''),
           (re.compile(r'<div></div>'), ''),
           (re.compile(r'<p>\s*(<img .* />)\s*</p>'), r'<div>\1</div>'),
           (re.compile(r'"<span style="font-weight: bold;">(.*?)</span>"'), r'<b>\1</b>'),
           (re.compile(r'<span style="font-weight: bold;">(.*?)</span>'), r'<b>\1</b>'),
           (re.compile(r'<span style="font-style: italic;">(.*?)</span>'), r'<i>\1</i>'),
           (re.compile(r'<span class="italic;">(.*?)</span>'), r'<i>\1</i>'),
           (re.compile(r'<span style="font-weight: bold;font-style: italic;">(.*?)</span>'), r'<b><i>\1</i></b>'),
           (re.compile(r'<h2><b>(.*?)</b></h2>'), r'<h2>\1</h2>')]

for f in files:
    file_name, file_extension = os.path.splitext(f)

    if file_extension in ('.htm', '.html'):
        generated_output_file = file_name + "_regex" + file_extension

        input_file = os.path.join(path, f)
        output_file = os.path.join(path, generated_output_file)

        with open(input_file, "r") as fi, open(output_file, "w+") as fo:
            file_content = fi.read()
            # file_content = htmlmin.minify(file_content, remove_optional_attribute_quotes=False, reduce_empty_attributes=False, pre_tags=(u'img'), remove_empty_space=True)
            for search, replace in REGEXES:
                file_content = search.sub(replace, file_content)
            fo.write(file_content)

        # Overwrite original file
        shutil.move(output_file, input_file)
