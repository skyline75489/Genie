Genie
=====

##The Simplest Static Blog Generator

### NOTE: Genie is currently in development and not useable for end user.

Genie is a static blog generator written in python.
It is inspired by many projects like [Pelican](http://getpelican.com/), [Simple](https://github.com/isnowfy/simple) and
[Rux](https://github.com/hit9/rux). It is probably the simplest static blog generator you'll ever seen.

## Demo

[My Blog(Chinese)](https://skyline75489.github.io/)
## Features

* Generate static html from [Markdown](http://daringfireball.net/projects/markdown/)
* No tags, No categories, No RSS feed, No comments...
* Extremely simple configuration(only one json file)
* Really easy to use(only one python file)
* [Github Flavored Markdown(GFM)](http://github.github.com/github-flavored-markdown/) supported(using [Misaka](http://misaka.61924.nl/))
* Syntax highlighting supported(using [highlight.js](http://highlightjs.org/))


## Installation


Just clone this repo to wherever you like

```
$ git clone git@github.com:skyline75489/Genie.git
```

## Usage

Choose your own blog name, input and output path in ```genie.settings```
.

My settings is like this:
```
{
	"in_file_path":"input/",
	"out_file_path":"output/",
	"blog_name":"Skyline75489"
}
```

Write some posts in Markdown and save them as ```xxx.md``` in the input path. It will generate into ```xxx.html``` in the output path.
The first line of the file will be the title of the post. So you should write something like this:

```
This is the title
=================

And this is what I want to say...

```
Right! Just like writing README.md.


When you finished your writing, run

```
$ python genie.py
```

If everything goes fine, then well done! You have a new blog site now. It's really easy, isn't it?

If you want to see what it looks like, you can do this:

```bash
$ cd your-dst-path
$ python -m SimpleHTTPServer
```

## Customize your site!

The templates and the CSS files is quite simple too. You can change them to anything you like!

## License

The MIT License
