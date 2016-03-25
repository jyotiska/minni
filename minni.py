import os
import sys
from datetime import datetime

page_content_start = """<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>%s</title><style type="text/css">body{background-color: #eee;margin:40px auto;max-width:650px;line-height:1.6;font-size:18px;color:#444;padding:0 10px}h1,h2,h3{line-height:1.2}</style></head><body><header><h1>%s</h1><p>%s</p><hr></header><p>"""
page_content_end = """</p><hr><p><center>Generated using <a href="https://github.com/jyotiska/minni">minni</a></center></p></body></html>"""


def create_directory():
    """Check if directories exist, create otherwise."""
    if not os.path.exists("posts"):
        os.makedirs("posts")


def create_post(title):
    """Create a new post."""
    filename = "posts/" + title.lower().replace(" ", "_") + ".html"
    post_date = "Posted at: " + datetime.now().strftime("%d-%m-%Y")

    html_content = page_content_start % (title, title, post_date) + "\n\n" + "<!-- Write your content here -->" + "\n\n\n\n" + page_content_end

    outfile = open(filename, 'w')
    outfile.write(html_content)
    outfile.close()

    print "Post created at:", filename

if __name__ == '__main__':
    command = sys.argv[1]

    if command == "init":
        create_directory()
    elif command == "new":
        title = sys.argv[2]
        create_post(title)
    else:
        sys.exit(0)
