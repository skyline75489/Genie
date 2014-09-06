import os
import time
import codecs
import json
import logging

import misaka


logger = logging.getLogger()

class Post(object):

    """Post class stores the information
    about the post
    """

    def __init__(self, src_path, dst_path, file_name, ext_name):
        self.file_name = file_name
        self.ext_name = ext_name
        self.dst_name = self.file_name + ".html"
        self.src_full_path = src_path + self.file_name + self.ext_name
        self.dst_full_path = dst_path + self.file_name + ".html"
        # The last-modified time of post file
        self.mtime_unix = os.path.getmtime(self.src_full_path)
        self.mtime = time.ctime(self.mtime_unix)
        f = codecs.open(self.src_full_path, mode="r", encoding="utf8")
        # Use the first line as post title
        self.title = f.readline()
        f.seek(0)
        self.text = f.read()


class Genie(object):
    
    MAX_POSTS_PER_PAGE = 15
    
    def __init__(self):
        """Initialize misaka Markdown parser 
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
        
    def _generate_page_with(self, posts, out_file, current_page=1):
        post_titles = ""
        for post in posts:
            # The About page, ignore it
            if post.file_name == "about":
                continue
            post_titles += '<div class="entry"><a class="title" href="' + post.dst_name + '">' + \
                post.title + '</a><span class="date">' + post.mtime + '</span></div>\n'

        result = self.index_template.format(
            content=post_titles, blog_name=self.blog_name, bottom_nav="").encode('utf-8')

        fout = open(self.out_file_path + out_file, "w")
        fout.write(result)
        fout.close()
        
    def _generate_index(self):
        start = 0
        end = self.MAX_POSTS_PER_PAGE
        self._generate_page_with(self.posts, 'index.html')

    def _generate_post(self, text, out_file_name):
        html = misaka.html(text, extensions=self.ext)
        result = self.blog_template.format(
            content=html, blog_name=self.blog_name).encode('utf-8')

        fout = open(out_file_name, "w")
        fout.write(result)
        fout.close()
        
    def _generate_archive(self):
        pass
        
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
        dst_path = self.out_file_path
        if os.path.isdir(src_path):
            files = os.listdir(src_path)
            for f in files:
                part = os.path.splitext(f)
                # Read markdown files only
                # "Part" is a tuple like ('file_name', 'ext_name')
                if part[1] in [".md", ".markdown"]:
                    post = Post(src_path, dst_path, part[0], part[1])
                    self.posts.append(post)
                    
    def _render(self):
        # Sort post in last-modified time ascending
        self.posts.sort(lambda p1, p2: cmp(p2.mtime_unix, p1.mtime_unix))
        # Generate html for every post we have
        for post in self.posts:
            raw_text = post.text
            self._generate_post(raw_text, post.dst_full_path)

        self._generate_index()
                
    def update(self):
        self._get_templates()
        self._get_posts()
        self._render()

if __name__ == '__main__':
    g = Genie()
    g.update()
