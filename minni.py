import os
import sys
import json
from datetime import datetime

page_content_start = open("templates/header").read()
page_content_end = open("templates/footer").read()


def create_directory():
    """Check if directories exist, create otherwise."""
    if not os.path.exists("posts"):
        os.makedirs("posts")

    if not os.path.exists("contents"):
        os.makedirs("contents")

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

    # Create an empty contents file
    filename = "posts/" + title.lower().replace(" ", "_") + ".html"
    outfile = open("contents/" + title.lower().replace(" ", "_") + ".html", 'w')
    outfile.close()

    # Calculate the post date based on current date
    post_date = "Posted on: " + datetime.now().strftime("%d-%m-%Y")

    # Put the post in the posts list JSON file
    posts_list = json.load(open('posts_list.json'))
    posts_list.append({"title": title, "filename": filename, "posted": post_date})
    posts_list = posts_list[::-1]

    # Write all posts list in the index file
    each_post_content = ""
    for each_post in posts_list:
        each_post_content += '''<li><a href="%s">%s</a> - %s</li>''' % (each_post["filename"], each_post["title"], each_post["posted"])
    posts_list_content = "<ul>%s</ul>" % (each_post_content)
    index_file_content = page_content_start % ("Blog Posts", "Blog Posts", "") + posts_list_content + page_content_end % (ga_code)

    index_file = open('index.html', 'w')
    index_file.write(index_file_content)
    index_file.close()

    posts_list = posts_list[::-1]
    outfile = open('posts_list.json', 'w')
    outfile.write(json.dumps(posts_list, indent=4))
    outfile.close()

    print "Content file created. You can edit directly at: %s. Use <publish> with minni to publish all posts" % (filename)


def publish():
    posts_list = json.load(open('posts_list.json'))

    for post in posts_list:
        title = post["title"]
        post_date = post["posted"]
        source_filename = "contents/" + post["filename"].split("/")[1]
        dest_filename = post["filename"]

        outfile = open(dest_filename, 'w')
        outfile.write(page_content_start % (title, title, post_date))
        outfile.write(open(source_filename).read())
        outfile.write(page_content_end % (ga_code))
        outfile.close()

        print "Published %s" % (title)

    # Write all posts list in the index file
    each_post_content = ""
    for each_post in posts_list:
        each_post_content += '''<li><a href="%s">%s</a> - %s</li>''' % (each_post["filename"], each_post["title"], each_post["posted"])
    posts_list_content = "<ul>%s</ul>" % (each_post_content)
    index_file_content = page_content_start % ("Blog Posts", "Blog Posts", "") + posts_list_content + page_content_end % (ga_code)

    index_file = open('index.html', 'w')
    index_file.write(index_file_content)
    index_file.close()

    print "Re-created index file"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python minni.py <init/new/publish>"
        sys.exit(0)
    else:
        command = sys.argv[1]
        ga_code = 'UA-75679673-1'
        if command == "init":
            create_directory()
        elif command == "new":
            title = sys.argv[2]
            create_post(title)
        elif command == "publish":
            publish()
        else:
            print "Usage: python minni.py <init/new/publish>"
            sys.exit(0)
