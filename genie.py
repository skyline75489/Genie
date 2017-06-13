#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import codecs
import json
import logging
import functools

import mistune

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
            create_time = parse_filename(self.filename)
            self.create_time_str = time.strftime("%d %b %Y", create_time)

            self.create_time = time.mktime(create_time)

        f = codecs.open(self.src_full_path, mode="r", encoding="utf8")
        # Use the first line as title
        self.title = f.readline()
        f.seek(0)
        self.text = f.read()


class Genie(object):

    MAX_POSTS_PER_PAGE = 10
    
    def __init__(self):
        """
        Initialize settings
        """
        self.load_settings()
        self.posts = []
        self.about = None

    def load_settings(self):
        f = open("genie.settings", "r")
        settings = json.load(f)
        self.in_file_path = settings['in_file_path']
        self.out_file_path = settings['out_file_path']
        self.blog_name = settings['blog_name']

    def generate_page_with(self, posts, current_page=1, more_page=False):
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
            content=post_titles, blog_name=self.blog_name, bottom_nav=bottom_nav)

        with open(self.out_file_path + out_file, "w+") as f:
            f.write(result)

    def generate_index(self):
        start = 0
        end = self.MAX_POSTS_PER_PAGE
        page = 1
        if len(self.posts) <= self.MAX_POSTS_PER_PAGE:
            self.generate_page_with(
                self.posts, current_page=page, more_page=False)
            return
        else:
            self.generate_page_with(
                self.posts[start:end], current_page=page, more_page=True)
            page += 1
            while end < len(self.posts):
                start = end
                end += self.MAX_POSTS_PER_PAGE
                more = True
                if end >= len(self.posts):
                    end = len(self.posts)
                    more = False
                self.generate_page_with(
                    self.posts[start:end], current_page=page, more_page=more)
                page += 1

    def generate_post(self, text, out_file_name):
        html = mistune.markdown(text, escape=False)
        result = self.blog_template.format(
            content=html, blog_name=self.blog_name)

        with open(out_file_name, "w+") as f:
            f.write(result)

    def get_templates(self):
        blog_template_file = codecs.open(
            "./templates/post_template.html", mode="r", encoding="utf8")
        index_template_file = codecs.open(
            './templates/index_template.html', mode="r", encoding="utf8")
        self.blog_template = blog_template_file.read()
        self.index_template = index_template_file.read()
        blog_template_file.close()
        index_template_file.close()

    def get_posts(self):
        src_path = self.in_file_path
        dst_path = self.out_file_path + 'post/'
        if os.path.isdir(src_path):
            files = os.listdir(src_path)
            for f in files:
                prefix, ext = os.path.splitext(f)
                # Read markdown files only
                if ext in [".md", ".markdown", '.mdown', '.mkd', '.mkdn']:
                    post = Post(src_path, dst_path, prefix, ext)
                    if prefix.endswith('about'):
                        self.about = post
                    self.posts.append(post)
                
        posts_count = len(self.posts)
        if self.about:
            posts_count -= 1
        logger('Find {0} articles'.format(posts_count))

    def render(self):
        # Sort post in create time ascending
        self.posts.sort(key=lambda p: p.create_time, reverse=True)
        # Generate html for every post we have
        logger('Start rendering')
        for post in self.posts:
            raw_text = post.text
            self.generate_post(raw_text, post.dst_full_path)
        logger('Done')
        if self.about:
            self.posts.remove(self.about)
        self.generate_index()

    def update(self):
        self.get_templates()
        self.get_posts()
        self.render()


def main():
    g = Genie()
    g.update()

if __name__ == '__main__':
    main()
