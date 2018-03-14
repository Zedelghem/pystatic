################################################
################################################
###              Pystatic, v 1.0             ###
###                                          ###
###            as of March 13, 2018          ###
###  https://github.com/Zedelghem/pystatic/  ###
###                                          ###
###                     by                   ###
###                                          ###
###              Borys Jastrzębski           ###
###                                          ### 
###         Licensed under GNU GPL 3.0       ###
################################################
################################################

import glob
from dateutil import parser
import locale
from os import makedirs, listdir, path
import codecs
import markdown
import shutil

locale.setlocale(locale.LC_ALL, '')

# Setting up the post class to make things clearer and easier
class Post (object):
    def __init__(self, path, filename, author='boro93', extension="md"):
        self.path = path
        self.filename = filename
        self.extension = extension
        
    def build_pretty_date(self, titleseparator="_", numberseparator="-", date_format="%b %d"):
        if hasattr(self, 'timestamp'):
            self.date = parser.parse(self.timestamp.split(" ")[0].split(titleseparator)[0]).strftime(date_format).capitalize()
            self.time = self.timestamp.split(" ")[1]
        else:
            self.date = parser.parse(self.filename.split(titleseparator)[0]).strftime(date_format).capitalize()
    
    def get_content(self, headerseparator="---", obligatory=['title'], optional=['author', 'timestamp']):
        
        # Completing the post list by importing title and content from the files
        ########################################################################
        ### Structure of the default file ###
        ## It should have a header delineated by "---" at the bottom that includes:
        # 1. [Obligatory] title
        # 2. [Optional] author (if empty, default author used)
        # 3. [Optional] Timestamp (date and time in the iso format) to enforce order in case of multiple posts a day
        ########################################################################

        # Load post file
        post_file = open(self.path + "/" + self.filename + "." + self.extension, 'r')
        current_post = post_file.read()
        post_file.close()
        
        # Chop current_post into header and the rest
        current_post = current_post.split(headerseparator)
        
        # Extract header
        raw_header = current_post[0].rstrip().split("\n")
        
        # Extract header details and assign them to self.options
        header = {}
        for entry in raw_header:
            if entry.split(": ")[0] in obligatory + optional:
                header[entry.split(": ")[0]] = entry.split(": ")[1]
        
        # If title was not set, 
        try:
            self.title = header['title']
        except:
            print("You need to set title in the header of the post", self.filename, "!")
        
        if 'author' in header.keys():
            self.author = header['author']
        if 'timestamp' in header.keys():
            self.timestamp = header['timestamp']
        
        # Delete header from current_post
        del(current_post[0])
        
        # Extract content
        self.content = current_post[0].rstrip()


# Function to generate post objects for every file of specific extention in a given path
def generate_posts(directory, extension="md"):
    # Loading filenames in the posts directory
    posts_paths = list(glob.glob(directory + "/*" + extension))
    # Strip extension
    posts_fnames = [post.split("/")[-1].replace("." + extension, "") for post in posts_paths]
    # Generate post object and store them in a dict
    posts_list = [Post(directory, fname, extension=extension) for fname in posts_fnames]
    
    return posts_list

# Function to filter out files with badly formatted dates in the filenames
def filter_bad_dates(posts_list, titleseparator="_", numberseparator="-"):
    
    to_ignore = []
    
    # Check if parts of the datestamp are in fact integers
    for index, post in enumerate(posts_list):
        datecheck = post.filename.split(titleseparator)[0].split(numberseparator)
        try:
            for num in datecheck:
                int(num)
        except:
            to_ignore.append(index)
            continue
        
        # Check if YYYY has 4 nums, MM 2 and DD 2
        if len(datecheck[0]) != 4 or len(datecheck[1]) != 2 or len(datecheck[2]) != 2:
            to_ignore.append(index)
            print("Date in the filename badly formatted. Looking for isoformat (YYYY-MM-DD).")
        elif int(datecheck[1]) > 12 or int(datecheck[2]) > 31:
            to_ignore.append(index)
            print("Date in the filename badly formatted. There are only 12 months and max 31 days a month.")
    
    posts_to_return = [post for index, post in enumerate(posts_list) if index not in to_ignore]
    
    return posts_to_return

def order(posts_list, reversed_true_or_not=True):
    return sorted(posts_list, key=lambda post: post.filename, reverse=reversed_true_or_not)

# Copytree from https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
def copytree(src, dst, symlinks=False, ignore=None):
    for item in listdir(src):
        s = path.join(src, item)
        d = path.join(dst, item)
        if path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def build_site_folders():
    makedirs("site", exist_ok=True)
    makedirs("site/posts", exist_ok=True)
    makedirs("site/assets", exist_ok=True)
    makedirs("site/css", exist_ok=True)

def inject_markdowned_content(post_object, paste_where, wrapper_class, template):
    content_html = markdown.markdown(post_object.content)
    target = template.replace(paste_where, '<div class="' + wrapper_class + '">' + content_html + '</div>')

    output_file = codecs.open("site/posts/" + post_object.filename + ".html", "w", encoding="utf-8", errors="xmlcharrefreplace")
    output_file.write(target)
    output_file.close()

def build_posts_folder(posts_list, template_file, in_path="posts", ignore_empty=True, extension="md", paste_where="<!--###POST_CONTENT###-->", wrapper_class="postcontent"):
    
    # Load template file
    template_f = open(template_file)
    template = template_f.read()
    template_f.close()
    
    for post in posts_list:
        
        if ignore_empty:
            if post.content != "":
                inject_markdowned_content(post, paste_where, wrapper_class, template)
            else:
                print("Not adding", post.filename, "to the post index. It is empty! Write something first.")
        else:
            inject_markdowned_content(post, paste_where, wrapper_class, template)

# Build main page of the blog
def build_index_page(posts_list, template_file, paste_where="<!--###POSTS_LIST###-->", ul_class="postlist", ignore_empty=True):
    # Function will look for paste_where and replace it with the generated ul_list
    # Generate <ul> with <li> for every post in the posts_sorted
    ul_list = ['<ul class="' + ul_class + '">']

    for post in posts_list:
        if ignore_empty:
            # Ignore posts with empty content attribute
            if post.content == "":
                print("Not adding", post.filename, "to the posts folder. It is empty! Write something before publishing. ;)")
                continue
            else:
                ul_list.append('<li><span class="date">' + post.date + '</span><span class="title"><a href="posts/' + post.filename + ".html" + '">' + post.title + '</a></span></li>')
        else:
            ul_list.append('<li><span class="date">' + post.date + '</span><span class="title"><a href="posts/' + post.filename + ".html" + '">' + post.title + '</a></span></li>')
    
    ul_list.append("</ul>")
    
    # Below: take the .html blueprint in and inject the ul_list in the space provided
    template = open(template_file)
    target = template.read().replace(paste_where, "".join(ul_list))
    template.close()
    
    output_file = open("site/index.html", 'w')
    output_file.write(target)
    output_file.close()

    
def build_website(in_path, ignore_empty_posts=True, index_template="templates/index.html", post_template="templates/post.html", css_and_assets_path="templates", extension="md", index_paste_where="<!--###POSTS_LIST###-->", post_paste_where="<!--###POST_CONTENT###-->", ul_class="postlist", post_wrapper="postcontent", headerseparator="---", obligatory_header=['title'], optional_header=['author', 'timestamp']):
    # Call everything
    try:
        fresh_posts = generate_posts(in_path, extension)
    except:
        print("Could not generate posts. Did you provide correct path to the post folder?")
    
    try:
        filtered_posts = filter_bad_dates(fresh_posts)
    except:
        print("Could not filter posts. Dunno why.")
    
    try:
        ordered_posts = order(filtered_posts)
    except:
        print("Could not order posts. It's impossible.")
    
    try:
        for post in ordered_posts:
            post.get_content(headerseparator=headerseparator, obligatory=obligatory_header, optional=optional_header)
            post.build_pretty_date(date_format="%b %d")
    except:
        print("Something went wrong with generating content and prettyfying dates. WHY?")

    # Delete target folder so it can be rebuilt without conflicts
    try:
        shutil.rmtree("site", ignore_errors=True)
    except:
        print("Could not delete previous site folder. Check file permissions for the script.")
    
    try:
        build_site_folders()
    except:
        print("Folders could not be built. Check file permissions.")
    
    try:
        build_index_page(ordered_posts, index_template, ignore_empty=ignore_empty_posts, paste_where=index_paste_where, ul_class=ul_class)
    except:
        print("Could not build index page. Did you provide a template?")
    
    try:
        build_posts_folder(ordered_posts, post_template, ignore_empty=ignore_empty_posts, in_path=in_path, extension=extension, paste_where=post_paste_where, wrapper_class=post_wrapper)
    except:
        print("Could not build post pages. Did you provide a template?")
    
    # Copy all css, assets and lib
    try:
        copytree(css_and_assets_path + "/css", "site/css")
    except:
        print("Tried to copy contents of", css_and_assets_path, "/css folder but the folder does not exist! Make one, even empty!")
    
    try:
        copytree(css_and_assets_path + "assets", "site/assets")
    except:
        print("Tried to copy contents of", css_and_assets_path, "/assets folder but the folder does not exist! Make one, even empty!")
    
    try:
        copytree(css_and_assets_path + "/lib", "site/lib")
    except:
        print("Tried to copy contents of", css_and_assets_path, "/lib folder but the folder does not exist! Make one, even empty!")