import os
import argparse
from os import makedirs, path
from shutil import copytree, copyfile, rmtree
from jinja2 import Environment, FileSystemLoader, Template
from markdown import markdown



class Config:
    root = "file:///Users/jzrake/Work/Website/site"


def emdash(html):
    return html.replace(" --- ", " &#8212 ")


def to_html(page, directory):
    if page.endswith('.html'):
        return emdash(open(path.join(directory, page), 'r').read())
    elif page.endswith('.md'):
        return emdash(markdown(open(path.join(directory, page), 'r').read()))



def render_directory(source_dir, target_dir, template):
    for page in os.listdir(source_dir):
        if path.isfile(path.join(source_dir, page)) and not page.startswith('.'):
            base = path.splitext(path.basename(page))[0]
            print(base)
            html = Template(to_html(page, source_dir)).render(root=Config.root)
            dst = open(path.join(target_dir, base + '.html'), 'w')
            dst.write(template.render(content=html, root=Config.root, page=base))



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--deploy", action='store_true')

    args = parser.parse_args()

    if args.deploy:
        Config.root = "http://www.columbia.edu/~jjz2125"


    try:
        rmtree("site")
    except FileNotFoundError:
        pass


    makedirs('site')
    makedirs('site/articles')
    makedirs('site/articles/coding-for-scientists')
    copytree('static', 'site/static')
    copyfile('style.css', 'site/style.css')


    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('main.html')

    render_directory('content', 'site', template)
    render_directory('content/articles', 'site/articles', template)
    render_directory('content/articles/coding-for-scientists', 'site/articles/coding-for-scientists', template)
