import os
import time
import codecs
import json
import misaka as misaka

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
    def __init__(self):
        """Initialize misaka Markdown parser 
        and settings
        """
        self._load_settings()
        self.posts = []
        self.ext = (
        misaka.EXT_STRIKETHROUGH|
        misaka.EXT_NO_INTRA_EMPHASIS|
        misaka.EXT_AUTOLINK|
        misaka.EXT_TABLES|
        misaka.EXT_FENCED_CODE
        )

    def _load_settings(self):
        f = open("genie.settings", "r")
        settings = json.load(f)
        self.in_file_path = settings['in_file_path']
        self.out_file_path = settings['out_file_path']
        self.blog_name = settings['blog_name']

    def _generate_index(self):
        post_titles = ""
        for post in self.posts:
            # The About page, ignore this
            if post.file_name == "about":
                continue
            post_titles += '<a class="title" href="' + post.dst_name + '">' + post.title + '</a><span>' + post.mtime + '</span><br>\n'

        result = self.index_template.format(content=post_titles, blog_name=self.blog_name).encode('utf-8')

        fout = open(self.out_file_path + "index.html", "w")
        fout.write(result)
        fout.close()

    def _generate_post(self, text, out_file_name):
        html = misaka.html(text,extensions=self.ext)
        result = self.blog_template.format(content=html, blog_name=self.blog_name).encode('utf-8')

        fout = open(out_file_name, "w")
        fout.write(result); 
        fout.close()

    def _read_template_files(self):
        blog_template_file = codecs.open("./templates/blog_template.html", mode="r", encoding="utf8")
        index_template_file = codecs.open('./templates/index_template.html', mode="r", encoding="utf8")
        self.blog_template = blog_template_file.read()
        self.index_template = index_template_file.read()
        blog_template_file.close()
        index_template_file.close()


    def _read_post_files(self):

        src_path = self.in_file_path
        dst_path = self.out_file_path
        if os.path.isdir(src_path):
            files = os.listdir(src_path)
            for f in files:
                part = os.path.splitext(f)
                # read .md files only
                # part is a tuple like ('file_name', 'ext_name')
                if part[1] in [".md", ".markdown"]:
                    post = Post(src_path, dst_path, part[0], part[1])
                    self.posts.append(post)

    def update(self):
        self._read_template_files()
        self._read_post_files()

        # Sort post in modified time ascending
        self.posts.sort(lambda p1, p2:cmp(p2.mtime_unix, p1.mtime_unix))
        # Generate html for every post we have
        for post in self.posts:
            raw_text = post.text
            self._generate_post(raw_text, post.dst_full_path)

        self._generate_index()

g = Genie()
g.update()

