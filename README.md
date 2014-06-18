Genie
=====

##The Tinest Static Blog Generator

Genie is a static blog generator written in python.
It is inspired by many projects like [Pelican](http://getpelican.com/), [Simple](https://github.com/isnowfy/simple) and
[Rux](https://github.com/hit9/rux). It is perhaps the tinest blog generator you'll ever seen.

## Demo

[My Blog(Chinese)](http://skyline75489.github.io/)
## Features

* Generate static html from [Markdown](http://daringfireball.net/projects/markdown/)
* No tags, No categories, No RSS feed, No Comments...
* Extremely simple configuration

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

Write some posts in pure Markdown and save them as ```xxx.md``` in the input path.
The first line of the file will be the title of the post. So you should write like this:

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

Done! It's really easy, isn't it?

## Custom your site!

The templates and the (only) CSS file is quite simple too. You can change them to anything you like!

## License

The MIT License
