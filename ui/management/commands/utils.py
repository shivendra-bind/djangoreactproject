import glob
import os
from bs4 import BeautifulSoup
from shutil import copytree


def inspect_parser(soup, tag):
    for x in soup.find_all(tag):
        if x.get("src") and x["src"].startswith("/static/"):
            x["src"] = '{% static "' + x["src"] + '" %}'
        if x.get("href") and x["href"].startswith("/static/"):
            x["href"] = '{% static "' + x["href"] + '" %}'
        if x.get("href") and x["href"].startswith("/favicon"):
            x["href"] = '{% static "' + x["href"] + '" %}'
        if x.get("href") and x["href"].startswith("/manifest"):
            x["href"] = '{% static "' + x["href"] + '" %}'


def render_html_static(html_dir):
    for html_file in glob.glob(os.path.join(html_dir, "*html")):
        soup = BeautifulSoup(open(html_file), "html.parser")
        soup.insert(0, "{% load static %}")
        inspect_parser(soup, "link")
        inspect_parser(soup, "script")
        fout = open(html_file, "wb")
        fout.write(soup.prettify("utf-8"))
        fout.close()
        print("done!!!")


def move_react_media(src, dest):
    copytree(src, dest, dirs_exist_ok=True)
    print(f"moved from {src} to {dest}")
