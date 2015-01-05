import os
import time
import codecs
import json
import logging

import misaka

def logger(str):
    print(str)

def parse_filename(filename):
    date = filename.split('_')[0]
    try:
        dt = time.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise Exception('Post filename is invalid')
    return dt

class Post(object):

    """
    Post class stores the information needed
    about the post
    """

    def __init__(self, src_path, dst_path, filename, ext_name):
        self.filename = filename
        self.ext_name = ext_name
        self.dst_name = "post/" + self.filename + ".html"
        self.src_full_path = src_path + self.filename + self.ext_name
        self.dst_full_path = dst_path + self.filename + ".html"
        
        if self.filename == 'about':
            self.create_time = time.time()
        else:
            self.create_time = parse_filename(self.filename)
            self.create_time_str = time.strftime("%d %b %Y", self.create_time)

        f = codecs.open(self.src_full_path, mode="r", encoding="utf8")
        # Use the first line as title
        self.title = f.readline()
        f.seek(0)
        self.text = f.read()


class Genie(object):

    MAX_POSTS_PER_PAGE = 15

    def __init__(self):
        """
        Initialize misaka Markdown parser 
        and settings
        """
        self._load_settings()
        self.posts = []
        self.ext = (
            misaka.EXT_STRIKETHROUGH |
            misaka.EXT_NO_INTRA_EMPHASIS |
            misaka.EXT_AUTOLINK |
            misaka.EXT_TABLES |
            misaka.EXT_FENCED_CODE
        )

    def _load_settings(self):
        f = open("genie.settings", "r")
        settings = json.load(f)
        self.in_file_path = settings['in_file_path']
        self.out_file_path = settings['out_file_path']
        self.blog_name = settings['blog_name']

    def _generate_page_with(self, posts, current_page=1, more_page=False):
        if not posts:
            return 
        post_titles = ""
        out_file = ""
        bottom_nav = ""
        if current_page == 1:
            out_file = "index.html"
        else:
            out_file = str(current_page) + '.html'

        for post in posts:
            # The About page, ignore it.
            if post.filename == "about":
                continue
            # Generate post entry.
            post_titles += '<div class="entry"><a class="title" href="' + post.dst_name + '">' + \
                post.title + '</a><span class="date">' + \
                post.create_time_str + '</span></div>\n'

        if current_page == 1:
            bottom_nav += '<span class="previous"><a href="">&nbsp</a></span>'      
        elif current_page > 1:
            previous_page = None
            if current_page == 2:
                previous_page = "index.html"
            else:
                previous_page = str(current_page - 1) + ".html"
            bottom_nav += '<span class="previous"><a href="' + \
                previous_page + '">Previous</a></span>'
        # More pages there.
        if more_page:
            next_page = str(current_page + 1) + ".html"
            bottom_nav += '<span class="next"><a href="' + \
                next_page + '">Next</a></span>'
        result = self.index_template.format(
            content=post_titles, blog_name=self.blog_name, bottom_nav=bottom_nav).encode('utf-8')

        fout = open(self.out_file_path + out_file, "w+")
        fout.write(result)
        fout.close()

    def _generate_index(self):
        start = 0
        end = self.MAX_POSTS_PER_PAGE
        page = 1
        if len(self.posts) <= self.MAX_POSTS_PER_PAGE:
            self._generate_page_with(
                self.posts, current_page=page, more_page=False)
            return
        else:
            self._generate_page_with(
                self.posts[start:end], current_page=page, more_page=True)
            page += 1
            while end <= len(self.posts):
                start = end
                end += self.MAX_POSTS_PER_PAGE
                more = True
                if end >= len(self.posts):
                    more = False
                self._generate_page_with(
                    self.posts[start:end], current_page=page, more_page=more)
                page += 1

    def _generate_post(self, text, out_file_name):
        html = misaka.html(text, extensions=self.ext)
        result = self.blog_template.format(
            content=html, blog_name=self.blog_name).encode('utf-8')

        fout = open(out_file_name, "w+")
        fout.write(result)
        fout.close()

    def _get_templates(self):
        blog_template_file = codecs.open(
            "./templates/post_template.html", mode="r", encoding="utf8")
        index_template_file = codecs.open(
            './templates/index_template.html', mode="r", encoding="utf8")
        self.blog_template = blog_template_file.read()
        self.index_template = index_template_file.read()
        blog_template_file.close()
        index_template_file.close()

    def _get_posts(self):
        src_path = self.in_file_path
        dst_path = self.out_file_path + 'post/'
        if os.path.isdir(src_path):
            files = os.listdir(src_path)
            for f in files:
                part = os.path.splitext(f)
                # Read markdown files only
                # "Part" is a tuple like ('filename', 'ext_name')
                if part[1] in [".md", ".markdown", '.mdown', '.mkd', '.mkdn']:
                    post = Post(src_path, dst_path, part[0], part[1])
                    self.posts.append(post)

        logger('Find {0} articles'.format(len(self.posts)))

    def _render(self):
        # Sort post in create time ascending
        self.posts.sort(lambda p1, p2: cmp(p2.create_time, p1.create_time))
        # Generate html for every post we have
        logger('Start rendering')
        for post in self.posts:
            raw_text = post.text
            self._generate_post(raw_text, post.dst_full_path)
        logger('Done')
        self._generate_index()

    def update(self):
        self._get_templates()
        self._get_posts()
        self._render()


def main():
    g = Genie()
    g.update()

if __name__ == '__main__':
    main()
