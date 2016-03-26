import os
import sys
import json
from datetime import datetime

page_content_start = """<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>%s</title><style type="text/css">body{margin:40px auto;max-width:650px;line-height:1.6;font-size:18px;color:#444;padding:0 10px}h1,h2,h3{line-height:1.2}</style></head><body><header><h1>%s</h1><p>%s</p><hr></header><p>"""
page_content_end = """</p><hr><p><center>Generated using <a href="https://github.com/jyotiska/minni">minni</a></center></p><script>(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)})(window,document,'script','//www.google-analytics.com/analytics.js','ga');ga('create','%s','auto');ga('send','pageview');</script></body></html>"""


def create_directory():
    """Check if directories exist, create otherwise."""
    if not os.path.exists("posts"):
        os.makedirs("posts")

    posts_list = []
    outfile = open('posts_list.json', 'w')
    outfile.write(json.dumps(posts_list))
    outfile.close()

    file_content = page_content_start % ("Blog Posts", "Blog Posts", "") + page_content_end % (ga_code)

    outfile = open('index.html', 'w')
    outfile.write(file_content)
    outfile.close()


def create_post(title):
    """Create a new post."""
    filename = "posts/" + title.lower().replace(" ", "_") + ".html"
    post_date = "Posted at: " + datetime.now().strftime("%d-%m-%Y")

    html_content = page_content_start % (title, title, post_date) + "\n\n" + "<!-- Write your content here -->" + "\n\n\n\n" + page_content_end % (ga_code)

    outfile = open(filename, 'w')
    outfile.write(html_content)
    outfile.close()

    posts_list = json.load(open('posts_list.json'))
    posts_list.append({"title": title, "filename": filename, "posted": post_date})
    posts_list = posts_list[::-1]

    each_post_content = ""
    for each_post in posts_list:
        each_post_content += '''<li><a href="%s">%s</a> - %s''' % (each_post["filename"], each_post["title"], each_post["posted"])
    posts_list_content = "<ul>%s</ul>" % (each_post_content)
    index_file_content = page_content_start % ("Blog Posts", "Blog Posts", "") + posts_list_content + page_content_end % (ga_code)

    index_file = open('index.html', 'w')
    index_file.write(index_file_content)
    index_file.close()

    outfile = open('posts_list.json', 'w')
    outfile.write(json.dumps(posts_list, indent=4))
    outfile.close()

    print "Post created at:", filename

if __name__ == '__main__':
    command = sys.argv[1]
    ga_code = 'UA-57540602-1'

    if command == "init":
        create_directory()
    elif command == "new":
        title = sys.argv[2]
        create_post(title)
    else:
        sys.exit(0)
