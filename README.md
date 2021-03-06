        ██████╗ ██╗   ██╗███████╗████████╗ █████╗ ████████╗██╗ ██████╗
        ██╔══██╗╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██║██╔════╝
        ██████╔╝ ╚████╔╝ ███████╗   ██║   ███████║   ██║   ██║██║     
        ██╔═══╝   ╚██╔╝  ╚════██║   ██║   ██╔══██║   ██║   ██║██║     
        ██║        ██║   ███████║   ██║   ██║  ██║   ██║   ██║╚██████╗
        ╚═╝        ╚═╝   ╚══════╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝

                    ┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ┌┐ ┬  ┌─┐┌─┐┌─┐┬┌┐┌┌─┐
                    └─┐ │ ├─┤ │ ││    ├┴┐│  │ ││ ┬│ ┬│││││ ┬
                    └─┘ ┴ ┴ ┴ ┴ ┴└─┘  └─┘┴─┘└─┘└─┘└─┘┴┘└┘└─┘ 
                    ┌┬┐┬ ┬┌─┐  ┌─┐┬ ┬┌┬┐┬ ┬┌─┐┌┐┌  ┬ ┬┌─┐┬ ┬
                     │ ├─┤├┤   ├─┘└┬┘ │ ├─┤│ ││││  │││├─┤└┬┘
                     ┴ ┴ ┴└─┘  ┴   ┴  ┴ ┴ ┴└─┘┘└┘  └┴┘┴ ┴ ┴

# pystatic
Dead simple static site generator. To build a website you need only one line of Python, the rest is Markdown, HTML, and CSS.

![Default template thumbnail](https://raw.githubusercontent.com/Zedelghem/pystatic/master/templates/assets/template_thumb.png)

## Quick start
Install and run pystatic in three simple steps:

1. Clone, fork or otherwise install this repo from GitHub, i.e.:

```
git clone https://github.com/Zedelghem/pystatic.git
```

2. Navigate to the location where the pystatic build.py file was installed
```
cd /path/to/pystatic (where build.py lives)
```

3. Run the build script from the command line:
```
python build.py
```

## Installation note
You might miss dateutil, rfeed or markdown in your Python configuration. They are all available through pip.
```python
pip install python-dateutil
pip install markdown
pip install rfeed
```

When installing markdown, make sure you use version 3.1 if you intend to use footnotes in your posts. Otherwise there is the risk the extension will not load.

## Description
There are multiple Python-based static site generators but I wanted something extremely simple, even primitive; something you could use knowing zero Python and perhaps never even having to tweak options. A tool for everyone not willing to struggle with servers or learn a CMS just to write stuff. Lo and behold, here comes pystatic.

The pipeline is incredibly straightforward. You may call the
```python
build_website("posts")
```

function with only one variable, path of the folder where you keep your posts, and the script builds your website with two templates, one for the main page and one for the post page. Posts should be written in markdown. You style templates in a .css file. The complete website is saved in the site folder. That's it.

> For the sake of future extensions the build_website function call in the build.py file looks slightly more complicated. It calls another function which reads in the configuration file, easy to understand by humans. So now you do not need to edit even that one line of code yourself. You can head straight to the pystatic.cfg file.

Folder structure is as follows.
```
|- build.py     (function call file, run this to build)
|- pystatic.py  (main script library file)
|- pystatic.cfg (the human readable configuration file)
|- LICENSE      (GPL 3.0)
|
|- posts/       (this is where you keep your markdown post files)
|-- 2018-03-12_best_title.md
|-- ...
|
|- templates/   (this is where you store the template files to generate website from)
|-- index.html
|-- post.html
|-- css/
|--- style.css
|-- lib/        (empty by default)
|-- assets/
|--- ...        (whatever additional files you need)
|
|- site/        (this is the generated website)
|-- index.html
|-- posts/
|--- 2018-03-12_best_title.html
|--- ...
|-- css/
|--- style.css
|-- assets/
|-- lib/
```

## Main information (enough to get things done)
1. Every post is a separate file. Filenames should look as follows:
    ```
    YYYY-MM-DD_here_goes_the_title.md
    ```
    
    so, for example:
    
    ```
    2018-03-12_helloworld.md
    ```
    
    This structure is important, this is where pystatic takes first information about the post from.

2. Every post should start with a header. Header looks as follows:
    ```
    title: Hello World
    author: Zedelghem
    timestamp: 2018-03-12 13:30
    tags: english essay literature
    excerpt: A test of a manual excerpt with <a href="http://google.com">a random link</a>.
    ---
    ```

    Everything above '---' is a header, everything below '---' is post content. Only 'title' is obligatory, the rest can be ommited. The order of the options does not matter to the script.

    **'Author'** is an option for multi-author blogs. It assigns an author to a particular post if you want it.

    **'Timestamp'** overwrites the date in the filename and assigns time to the post so it can be used to handpick order of posts published on the same day.

    **'Tags'** is a list of classes that will be added to the \<li> object representing your post on the front page as well as to the \<section> and \<h1> representing your post on the individual post page.

    **'Excerpt'** sets the manual excerpt for the post, if would like to do so. However, excerpts need to be turned on in the configuration file to work.

3. The script does two main things. First, it generates an unordered list (\<ul>) of all posts and injects it to the template file for index.html. It does so by replacing a placeholder, by default it's \<!--###POSTS_LIST###-->. Second, for every post it converts its content from Markdown to HTML (using Python markdown library) and creates a file for it using a template file for post. It also does so by replacing a placeholder, \<!--###POST_CONTENT###--> by default. The title for the post page is automatically set to the title of the post, again by replacing a placeholder, \<!--###POSTPAGE_TITLE###--> by default.

4. Remember how the file tree is built – the posts folder is at the same level as the CSS, assets and the lib folder. In the template you need to account for the need to get one level up to get to the .css file. For example, to refer to a style.css within your template file or a post file you need to use the following path.
    ```
    ../css/style.css
    ```

    The same principle applies to linking to scripts, images, etc. either from the template file or the post. So paths would look something like the following.
    ```
    ../assets/image01.jpeg
    ../lib/random_script.js
    ```

    I will think about accounting for it automatically but for now I think it would unnecessarily increase the number of options to keep in mind before running the script. I think it is easy enough to add two dots on your own.

## For tweakers: configuration file
As of version 1.1 (July 23, 2018) pystatic ships with a human-readable configuration file. It means you can set all of the options below without handling the code. Just open the pystatic.cfg file in a text editor and follow the instructions.

## For ultratweakers: detailed structure of the build_website() function
The build_website() function has one positional (required) and ~~eleven~~ multiple keyword arguments, all of which can be found along with explanation in the configuration file.

```python
build_website(in_path, ignore_empty_posts=True, index_template="templates/index.html", post_template="templates/post.html", css_and_assets_path="templates", extension="md", index_paste_where="<!--###POSTS_LIST###-->", post_paste_where="<!--###POST_CONTENT###-->", title_paste_where="<!--###POSTPAGE_TITLE###-->",ul_class="postlist", post_wrapper="postcontent", headerseparator="---", obligatory_header=['title'], optional_header=['author', 'timestamp', 'tags', 'excerpt'], excerpt_type="chars", excerpt_len="500", excerpts_on=False, readmore="Read more >>", posts_per_page=0, pages_in_multiple_files=False, postlist_date_format="%d %b '%y", rss_feed_on=True, rss_feed_url="rss", blurb_is_manual_excerpt=False, rss_max_posts_number=10, blog_domain="", rss_feed_description='', rss_feed_title="My blog's RSS feed")

```
Most of them are self explanatory. However, I explain some of them below for clarity.

**in_path** is the path of the folder with posts files. 

**ignore_empty_posts** sets whether you want to include empty posts in the list of posts on the main page as well as their files in the posts folder in the built site folder.

**index_template** gives the path to the template file for the index page (with posts list).

**post_template** gives the path to the template file for the individual post page.

**css_and_assets_path** sets the path for the folder holding css/, assets/ and lib/ folder. Note that changing this does not change the path for template files. You need to set them separately.

**extension** sets file extension for your posts files. At the moment it does no really make sanse to change it. For now all posts are by default parsed through markdown library and thus they should be written using markdown. However, the parser does not care about file extension. Therefore if you really want (or for some strange reasons need) to store your files in .txt or any other format, you may do so.

**index_paste_where** sets the placeholder for the \<ul> with posts list to be injected into the index page template.

**post_paste_where** sets the placeholder for the post content to be injected into the post template file.

**title_paste_where** sets the placeholder for the <title> of the post .html page.

**ul_class** sets the class of the \<ul> holding the list of your posts on the main website.

**post_wrapper** sets the class of the \<section> where the content of your post is stored in the individual post's .html file.

**headerseparator**, obviously, sets the string that separates header from the content of the post. If for some other reasons you need the first "---" of your file to be left in the post content, change this feature.

**obligatory_header** provides a list of header options required by the generator to build post content and thus include the post in the built website. For now, the only required parameter is title. If you really want to always require yourself or your authors to include other things, you might add them to the list.

**optional_header** provides a list of optional header options. Expanding it will not change anything at this moment. However, deleting one of the options will make it unusable. I would not change anything here for now.

**excerpts_on** sets whether excerpts, both manual and automatic, are on (=True) or off (=False). By default they are off.

**excerpt_type** sets the unit of length of the automatic excerpt. It can be set to characters or words. By default it is set to characters (chars).

**excerpt_len** sets the length of the automatic excerpt in the unit of lenth chosen in *excerpt_type*. It is 500 by default. So the default excerpt is 500 characters long.

**readmore** sets the value of the readmore span shown after an excerpt (if the excerpts_on is set True, of course).

**posts_per_page** sets the number of posts per page of the list of posts (front page). If posts_per_page is set to 0, pagination is turned off.

**pages_in_multiple_files** sets whether the pagination on the front page is interpreted as multiple .html files (True) or as multiple \<ul>s within one .html file (False). Note that the value of pages_in_multiple_files matters only when posts_per_page has been set to anything other than 0.

**postlist_date_format** sets the format of the date shown next to the post in the post list on the front page. For all available options see https://docs.python.org/2/library/datetime.html#timedelta-objects.

## Roadmap?
There are, of course, tons of options that might be added like import or export to particular CMS, support for manipulation and creation of templates from the script, reading other than Markdown text-to-HTML interpreters, etc. ~~However, I am rather happy with this version and for now I do not see any need to expand it for my purposes. I will think about extension if I come across a problem that bothers me or if anyone else ever uses pystatic. ;)~~

Okay, so things changed a bit. There was a fantastic response from @alex7217, also I need to implement a bilingual blog for myself, and some new features are coming:

1. ~~Optional excerpts~~ (Done),
2. ~~Option for pagination~~ (Done),
3. ~~An optional navigation~~ (Partially done: there is an automatic navigation generated for paginaton with pages in separate files) / ~~post tagging~~ (Done, filtration can be added in CSS),
4. Some new templates. (In progress: I am currently preparing the Tufte CSS-based default template)
5. Option for navigation with stable webpages in manually set order, like "About me", etc.
6. Convention for sidenotes inspired by Tufte CSS (in progress)
7. ~~Add RSS feed, proposed by Trav/Treasuretron~~ (Done)
8. Add pystatic as a package to PyPI so it can be installed through pip

All of this will be done with utmost simplicity of use in mind. So worry not - the spirit of pystatic is not lost!

If you are looking for a similar ready to go tool, full of options, just browse https://www.staticgen.com.

Give pystatic a try and let me know what you think!

## License
It is GNU GPL 3.0. In other words, do whatever you wish but
1. Mention me and the license explicitly.
2. List changes you made to the code.
3. Make the source public.
4. Licence your code with GNU GPL 3.0 as well.
