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

## Installation note
You might miss dateutil or markdown in your Python configuration. They are both available through pip.
```python
pip install python-dateutil
pip install markdown
```

## Description
There are multiple Python-based static site generators but I wanted something extremely simple, even primitive; something you could use knowing zero Python and perhaps never even having to tweak options. A tool for everyone not willing to struggle with servers or learn a CMS just to write stuff. Lo and behold, here comes pystatic.

The pipeline is incredibly straightforward. You call the
```python
build_website("posts")
```

function (in the build.py file) with only one variable, path of the folder where you keep your posts, and the script builds your website with two templates, one for the main page and one for the post page. Posts should be written in markdown. You style templates in a .css file. The complete website is saved in the site folder. That's it. Folder structure is as follows.
```
|- pystatic.py
|- build.py
|- templates/
|-- index.html
|-- post.html
|-- css/
|--- style.css
|-- lib/
|--- (empty by default) any additional scripts you might need
|-- assets/
|--- (empty by default) whatever additional files you need
|--- ...
|- posts/
|-- 2018-03-12_best_title.md
|-- ...
|
|- site/
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
    ---
    ```

    Everything above '---' is a header, everything below '---' is post content. Only 'title' is obligatory, the rest can be ommited. 

    'Author' is an option for multi-author blogs. It assigns an author to a particular post if you want it.

    'Timestamp' overwrites the date in the filename and assigns time to the post so it can be used to handpick order of posts published on the same day.

3. The script does two main things. First, it generates an unordered list (\<ul>) of all posts and injects it to the template file for index.html. It does so by replacing a placeholder, by default it's '<!--###POSTS_LIST###-->'. Second, for every post it converts its content from Markdown to HTML (using Python markdown library) and creates a file for it using a template file for post. It also does so by replacing a placeholder, '<!--###POST_CONTENT###-->' by default.

4. Remember how the file tree is built – posts are in a folder at the same level as the CSS and assets folder. In the template you need to account for the need to get one level up to get to the .css file. For example, to refer to a style.css within your template file or a post file you need to use the following path.
    ```
    ../css/style.css
    ```

    Same applies to linking to scripts, images, etc. either from the template file or the post. So paths would look something like the following.
    ```
    ../assets/image01.jpeg
    ../lib/random_script.js
    ```

    I will think about accounting for it automatically but for now I think it would unnecessarily increase the number of options to keep in mind before running the script. I think it is easy enough to add two dots on your own.

## For tweakers: configuration file
As of version 1.1 (July 23, 2018) pystatic ships with a human-readable configuration file. It means you can set all of the options below without handling the code. Just open the CONFIG file in a text editor and follow the instructions.

## For ultratweakers: detailed structure of the build_website() function
The build_website() function has one positional (required) and eleven keyword arguments.

```python
build_website(in_path, ignore_empty_posts=True, index_template="templates/index.html", post_template="templates/post.html", css_and_assets_path="templates", extension="md", index_paste_where="<!--###POSTS_LIST###-->", post_paste_where="<!--###POST_CONTENT###-->", ul_class="postlist", post_wrapper="postcontent", headerseparator="---", obligatory_header=['title'], optional_header=['author', 'timestamp'])
```
Most of them are self explanatory. However, I explain all of them below for clarity.

**in_path** is the path of the folder with posts files. 

**ignore_empty_posts** sets whether you want to include empty posts in the list of posts on the main page as well as their files in the posts folder in the built site folder.

**index_template** gives the path to the template file for the index page (with posts list).

**post_template** gives the path to the template file for the individual post page.

**css_and_assets_path** sets the path for the folder holding css/, assets/ and lib/ folder. Note that changing this does not change the path for template files. You need to set them separately.

**extension** sets file extension for your posts files. At the moment it does no really make sanse to change it. For now all posts are by default parsed through markdown library and thus they should be written using markdown. However, the parser does not care about file extension. Therefore if you really want (or for some strange reasons need) to store your files in .txt or any other format, you may do so.

**index_paste_where** sets the placeholder for the \<ul> with posts list to be injected into the index page template.

**post_paste_where** sets the placeholder for the post content to be injected into the post template file.

**ul_class** sets the class of the \<ul> holding the list of your posts on the main website.

**post_wrapper** sets the class of the \<div> where the content of your post is stored in the individual post's .html file.

**headerseparator**, obviously, sets the string that separates header from the content of the post. If for some other reasons you need the first "---" of your file to be left in the post content, change this feature.

The two features below were introduced with ease of possible further development in mind. There is no much use in tweaking them at the moment.

**obligatory_header** provides a list of header options required by the generator to build post content and thus include the post in the built website. If you really want to always require yourself to include author and timestamp, you might add these two to the list.

**optional_header** provides a list of optional header options. Expanding it will not change anything at this moment. However, deleting one of the options will make it unusable. I would not change anything here for now.

## Roadmap?
There are, of course, tons of options that might be added like import or export to particular CMS, support for manipulation and creation of templates from the script, reading other than Markdown text-to-HTML interpreters, etc. However, I am rather happy with this version and for now I do not see any need to expand it for my purposes. I will think about extension if I come across a problem that bothers me or if anyone else ever uses pystatic. ;)

If you are looking for a similar ready to go tool, full of options, just browse https://www.staticgen.com.

Give pystatic a try and let me know what you think!

## License
It is GNU GPL 3.0. In other words, do whatever you wish but
1. Mention me and the licensce explicitly.
2. List changes you made to the code.
3. Make the source public.
4. Licence your code with GNU GPL 3.0 as well.
