#        ██████╗ ██╗   ██╗███████╗████████╗ █████╗ ████████╗██╗ ██████╗
#        ██╔══██╗╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██║██╔════╝
#        ██████╔╝ ╚████╔╝ ███████╗   ██║   ███████║   ██║   ██║██║     
#        ██╔═══╝   ╚██╔╝  ╚════██║   ██║   ██╔══██║   ██║   ██║██║     
#        ██║        ██║   ███████║   ██║   ██║  ██║   ██║   ██║╚██████╗
#        ╚═╝        ╚═╝   ╚══════╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝
#
#┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ┌┐ ┬  ┌─┐┌─┐┌─┐┬┌┐┌┌─┐  ┌┬┐┬ ┬┌─┐  ┌─┐┬ ┬┌┬┐┬ ┬┌─┐┌┐┌  ┬ ┬┌─┐┬ ┬
#└─┐ │ ├─┤ │ ││    ├┴┐│  │ ││ ┬│ ┬│││││ ┬   │ ├─┤├┤   ├─┘└┬┘ │ ├─┤│ ││││  │││├─┤└┬┘
#└─┘ ┴ ┴ ┴ ┴ ┴└─┘  └─┘┴─┘└─┘└─┘└─┘┴┘└┘└─┘   ┴ ┴ ┴└─┘  ┴   ┴  ┴ ┴ ┴└─┘┘└┘  └┴┘┴ ┴ ┴ 
#
##################################################################################
##################################################################################
###                         This is the build file for                         ###
###                                                                            ###
###                              Pystatic, v 1.1                               ###
###                                                                            ###
###                            as of July 23, 2018                             ###
###                  https://github.com/Zedelghem/pystatic/                    ###
###                                                                            ###
###                                      by                                    ###
###                                                                            ###
###                              Borys Jastrzębski                             ###
###                                                                            ### 
###                          Licensed under GNU GPL 3.0                        ###
###                                                                            ###
###     Before attempting any changes in this file, please make sure you've    ###
###     read the documentation on the GitHub page of the project. I kept it    ###
###     concise and it can save you a lot of trouble.                          ###
###                                                                            ###
###     Also, take a look at the discussion on the GitHub forums before        ###
###     writing an extension to Pystatic. I might already be working on        ###
###     a similar feature.                                                     ###
###                                                                            ###
##################################################################################
##################################################################################

import glob
from dateutil import parser
import locale
from os import makedirs, listdir, path
import codecs
import markdown
import shutil
import math

locale.setlocale(locale.LC_ALL, '')

# Setting up the post class to make things clearer and easier
class Post (object):
    def __init__(self, path, filename, author='Author', extension="md"):
        self.path = path
        self.filename = filename
        self.extension = extension
        
    def build_pretty_date(self, titleseparator="_", numberseparator="-", date_format="%b %d"):
        if hasattr(self, 'timestamp'):
            self.date = parser.parse(self.timestamp.split(" ")[0].split(titleseparator)[0]).strftime(date_format).capitalize()
            self.time = self.timestamp.split(" ")[1]
        else:
            self.date = parser.parse(self.filename.split(titleseparator)[0]).strftime(date_format).capitalize()
    
    def get_content(self, headerseparator="---", obligatory=['title'], optional=['author', 'timestamp', "tags", "excerpt"]):
        
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
        
        # Extract header details and store them in a dictionary
        header = {}
        for entry in raw_header:
            if entry.split(": ")[0] in obligatory + optional:
                header[entry.split(": ")[0]] = entry.split(": ")[1]
        
        # If title was not set
        try:
            self.title = header['title']
        except:
            print("You need to set title in the header of the post", self.filename, "!")
        
        # Check for and assign optional header declarations
        if 'author' in header.keys():
            self.author = header['author']
        else:
            self.author = None

        if 'timestamp' in header.keys():
            self.timestamp = header['timestamp']

        if 'tags' in header.keys():
            self.tags = header['tags']
        else:
            self.tags = ""

        if 'excerpt' in header.keys():
            self.excerpt = markdown.markdown(header['excerpt'])
        
        # Delete header from current_post
        del(current_post[0])
        
        # Extract content
        self.content = current_post[0].rstrip()
    
    # I left an option for sentences as a unit of excerpt_len
    # Not working properly now – doesn't crash but tuned only to fullstops.
    def get_excerpt(self, len_type="chars", excerpt_len="500"):
        if not hasattr(self, "excerpt"):
            parsed_content = markdown.markdown(self.content)

            try:
                length = int(excerpt_len)
            except:
                print("Could not change the type of excerpt_len to int")

            if len_type == "chars":
                excerpt_ready = parsed_content[:length]
            elif len_type == "words":
                excerpt_ready = " ".join(parsed_content.split(" ")[:length])
            elif len_type == "sentences":
                excerpt_ready = ". ".join(parsed_content.split(". ")[:length])

            self.excerpt = excerpt_ready.rstrip() + "..."

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

def build_site_folders(outFolder):
    makedirs(outFolder, exist_ok=True)
    makedirs(outFolder + "/posts", exist_ok=True)
    makedirs(outFolder + "/assets", exist_ok=True)
    makedirs(outFolder + "/css", exist_ok=True)
    makedirs(outFolder + "/lib", exist_ok=True)

def inject_markdowned_content(post_object, paste_where, paste_where_title, wrapper_class, template, out_folder="site", post_output_file_extension=".html"):
    try:
        # Trying to use markdown library with the footnotes extension    
        content_html = markdown.markdown(post_object.content, extensions=['footnotes'])
    except:
        content_html = markdown.markdown(post_object.content)

    # Checking for Author and adding information
    if post_object.author is not None:
        post_author_par = '\n <p class="post_author">' + post_object.author + '</p>'
    else:
        post_author_par = ""

    target = template.replace(paste_where, '<h1 class="post_title">' + post_object.title + '</h1>' + post_author_par + '\n <section class="' + wrapper_class + " " + post_object.tags + '">' + content_html + '</section>').replace(paste_where_title, post_object.title)

    output_file = codecs.open(out_folder + "/posts/" + post_object.filename + post_output_file_extension, "w", encoding="utf-8", errors="xmlcharrefreplace")
    output_file.write(target)
    output_file.close()

def build_posts_folder(posts_list, template_file, out_folder_path="site", in_path="posts", ignore_empty=True, extension="md", post_output_file_extension=".html", paste_where="<!--###POST_CONTENT###-->", paste_where_title="<!--###POSTPAGE_TITLE###-->", wrapper_class="postcontent"):
    
    # Load template file
    template_f = open(template_file)
    template = template_f.read()
    template_f.close()
    
    for post in posts_list:
        
        if ignore_empty:
            if post.content != "":
                inject_markdowned_content(post, paste_where, paste_where_title, wrapper_class, template, out_folder=out_folder_path, post_output_file_extension=post_output_file_extension)
            else:
                print("Not adding", post.filename, "to the post index. It is empty! Write something first.")
        else:
            inject_markdowned_content(post, paste_where, paste_where_title, wrapper_class, template)

# Build main page of the blog
def build_index_page(posts_list, template_file, outFolder="site", paste_where="<!--###POSTS_LIST###-->", ul_class="postlist", ignore_empty=True, excerpts_on=False, posts_per_page=0, pages_in_multiple_files=False, readmore="Read more >>", output_file_extension=".html", postpage_output_file_extension=".html"):    
    # Function will look for paste_where and replace it with the generated ul_list
    # Generate <ul> with <li> for every post in the posts_sorted
    if posts_per_page == 0:
        ul_list = ['<ul class="' + ul_class + '">']
        for post in posts_list:

            if excerpts_on:
                excerpt = '<div class="excerpt">' +  post.excerpt + '<span class="readmore">' + '<a href="posts/' + post.filename + postpage_output_file_extension + '">' + readmore + '</a>' + '</span>' + '</div>'
            else:
                excerpt = ""
            if ignore_empty:
                # Ignore posts with empty content attribute
                if post.content == "":
                    print("Not adding", post.filename, "to the posts folder. It is empty! Write something before publishing. ;)")
                    continue
                else:
                    ul_list.append('<li class= "' + post.tags + '"><span class="date">' + post.date + '</span><span class="title"><a href="posts/' + post.filename + postpage_output_file_extension + '">' + post.title + '</a></span>' + excerpt + '</li>')
            else:
                ul_list.append('<li class= "' + post.tags + '"><span class="date">' + post.date + '</span><span class="title"><a href="posts/' + post.filename + postpage_output_file_extension + '">' + post.title + '</a></span>' + excerpt + '</li>')

        ul_list.append("</ul>")

        # Below: take the .html blueprint in and inject the ul_list in the space provided
        template = open(template_file)
        target = template.read().replace(paste_where, "".join(ul_list))
        template.close()
        
        output_file = open(outFolder + "/index" + output_file_extension, 'w')
        output_file.write(target)
        output_file.close()

    elif posts_per_page > 0:

        # Populate pages
        num_of_pages = math.ceil(len(posts_list) / posts_per_page)
        pages = [[] for num in range(0, num_of_pages)]
        current_page_number = 0

        for post in posts_list:

            if excerpts_on:
                excerpt = '<div class="excerpt">' +  post.excerpt + '<span class="readmore">' + '<a href="posts/' + post.filename + postpage_output_file_extension + '">' + readmore + '</a>' + '</span>' + '</div>'
            else:
                excerpt = ""

            if ignore_empty:
                # Ignore posts with empty content attribute
                if post.content == "":
                    print("Not adding", post.filename, "to the posts folder. It is empty! Write something before publishing. ;)")
                    continue
                else:
                    pages[current_page_number].append('<li class= "' + post.tags + '"><span class="date">' + post.date + '</span><span class="title"><a href="posts/' + post.filename + postpage_output_file_extension + '">' + post.title + '</a></span>' + excerpt + '</li>')
            else:
                pages[current_page_number].append('<li class= "' + post.tags + '"><span class="date">' + post.date + '</span><span class="title"><a href="posts/' + post.filename + postpage_output_file_extension + '">' + post.title + '</a></span>' + excerpt + '</li>')
            
            if len(pages[current_page_number]) == posts_per_page:
                current_page_number += 1

        pages_parsed = []
        for index, page in enumerate(pages):
            pages_parsed.append('<ul id="page' + str(index+1) + '" class="' + ul_class + '">' + "".join(page) + "</ul>")

        # Interpret pages as either multiple .html files...
        if pages_in_multiple_files:
            # Add navigation between pagefiles
            pagenav = ['<div id="page_navigation">']
            for pnum in range(num_of_pages):
                if pnum == 0:
                    index_number = ""
                else:
                    index_number = str(pnum+1)
                pagenav.append('<a href="index' + index_number + output_file_extension + '">' + str(pnum+1) + '</a>')
            pagenav.append("</div>")

            for index, pagefile in enumerate(pages_parsed):
                # Below: take the .html blueprint in and inject the list in the space provided
                template = open(template_file)
                target = template.read().replace(paste_where, " ".join(pagenav) + pagefile)
                template.close()
                
                if index == 0:
                    index_number = ""
                else:
                    index_number = str(index+1)

                output_file = open(outFolder + "/index" + index_number + output_file_extension, 'w')
                output_file.write(target)
                output_file.close()

        # ...or as multiple <ul>s within one index.html file, for example for the purpose of CSS tabs-based pagination
        else:

            # Add navigation between <ul>s with different ids
            pagenav = ['<div id="page_navigation">']
            for pnum in range(num_of_pages):
                index_number = str(pnum+1)
                pagenav.append('<a href="#page' + index_number + '">' + str(pnum+1) + '</a>')
            pagenav.append("</div>")

            template = open(template_file)
            target = template.read().replace(paste_where, " ".join(pagenav) + "".join(pages_parsed))
            template.close()

            output_file = open(outFolder + "/index.html", 'w')
            output_file.write(target)
            output_file.close() 

    else:
        print("Invalid posts_per_page value. Should be an integer >= 0")

def strRepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def parse_config(filename):
    # Load in the config file and close it
    cfg_file = open(filename, "r")
    cfg_lines = cfg_file.readlines()
    cfg_file.close()

    # Extract options, i.e. lines with "$", and drop "$"
    cfg = [line[1:] for line in cfg_lines if line[0] == "$"]

    # Create a dict of options
    options = {}
    for option in cfg:
        options[option.split(":")[0]] = option.split(":")[1].strip()

    # Extract positional arguments
    # For now it means only: in_path
    positional_args = [options["in_path"]]
    del options["in_path"]    

    # Extract arguments coming in lists
    # For now it means: obligatory_header and optional_header
    # If more list-valued arguments pop up, add them to list_args
    list_args = ["obligatory_header", "optional_header"]
    for arg in list_args:
        options[arg] = options[arg].split(", ")
    
    # Look for potential booleans and ints to convert
    for key, val in options.items():
        if val in ["True", "False"]:
            try:
                if val == "True":
                    options[key] =  True
                elif val == "False":
                    options[key] = False
            except ValueError:
                print("Trouble converting a boolean-like string to a boolean value.")
        
        if type(val) is not list and strRepresentsInt(val) == True:
            try:
                options[key] = int(val)
            except ValueError:
                print("Trouble converting an integer-like string to an integer.")

    # Combine all the arguments into the final list of options
    list_of_options = []
    list_of_options.extend(positional_args)
    list_of_options.append(options.copy())

    return list_of_options

def build_website(in_path, out_path="site", ignore_empty_posts=True, index_template="templates/index.html", post_template="templates/post.html", css_and_assets_path="templates", extension="md", index_output_file_extension=".html", postpage_output_file_extension=".html", index_paste_where="<!--###POSTS_LIST###-->", post_paste_where="<!--###POST_CONTENT###-->", title_paste_where="<!--###POSTPAGE_TITLE###-->",ul_class="postlist", post_wrapper="postcontent", headerseparator="---", obligatory_header=['title'], optional_header=['author', 'timestamp', 'tags', 'excerpt'], excerpt_type="chars", excerpt_len="500", excerpts_on=False, blurb_is_manual_excerpt=True, readmore="Read more >>", posts_per_page=0, pages_in_multiple_files=False, postlist_date_format="%d %b '%y"):
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
            post.build_pretty_date(date_format=postlist_date_format)
            post.get_excerpt(len_type=excerpt_type, excerpt_len=excerpt_len)
    except:
        print("Something went wrong with generating content and prettyfying dates. WHY?")

    # Delete target folder so it can be rebuilt without conflicts
    try:
        shutil.rmtree("site", ignore_errors=True)
    except:
        print("Could not delete previous site folder. Check file permissions for the script.")
    
    try:
        build_site_folders(out_path)
    except:
        print("Folders could not be built. Check file permissions.")
    
    try:
        build_index_page(ordered_posts, index_template, outFolder=out_path, output_file_extension=index_output_file_extension, postpage_output_file_extension=postpage_output_file_extension, ignore_empty=ignore_empty_posts, paste_where=index_paste_where, ul_class=ul_class, excerpts_on=excerpts_on, readmore=readmore, posts_per_page=posts_per_page, pages_in_multiple_files=pages_in_multiple_files)
    except:
        print("Could not build index page. Did you provide a template?")
    
    try:
        build_posts_folder(ordered_posts, post_template, out_folder_path=out_path, post_output_file_extension=postpage_output_file_extension, ignore_empty=ignore_empty_posts, in_path=in_path, extension=extension, paste_where=post_paste_where, paste_where_title=title_paste_where, wrapper_class=post_wrapper)
    except:
        print("Could not build post pages. Did you provide a template?")
    
    # Copy all css, assets and lib
    try:
        copytree(css_and_assets_path + "/css", out_path + "/css")
    except:
        print("Tried to copy contents of", css_and_assets_path, "/css folder but the folder does not exist! Make one, even empty!")
    
    try:
        copytree(css_and_assets_path + "/assets", out_path + "/assets")
    except:
        print("Tried to copy contents of", css_and_assets_path, "/assets folder but the folder does not exist! Make one, even empty!")
    
    try:
        copytree(css_and_assets_path + "/lib", out_path + "/lib")
    except:
        print("Tried to copy contents of", css_and_assets_path, "/lib folder but the folder does not exist! Make one, even empty!")