#!/usr/bin/env python
import tweepy
import os
import time
import lib_func
import argparse
from argparse import RawTextHelpFormatter

# Program name and version 
version = "2.5"  
p_name = "Libertas"

# API Keys
path_keys = "data/keys/"
AK = path_keys + "AK.txt"
AS = path_keys + "AS.txt"
CK = path_keys + "CK.txt"
CS = path_keys + "CS.txt"

# Intros
path_intros = "data/intros/"

# Exits
path_exits = "data/exits/"
ff_exit = path_exits + "ff_exits.txt"
ed_exit = path_exits + "ed_exits.txt"

# Ed files
path_ed ="data/ed/"

# Command line options parser     
parser = argparse.ArgumentParser(prog=p_name, formatter_class=RawTextHelpFormatter, description="""Libertas is a set of command line interface (cli) tools for twitter with activism in mind. It includes a cli tweet, #FF bot and more.

    Copyright (C) 2010-2012  godsofliberty
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    Contact: godsofliberty@lavabit.com""")

# Verion option
parser.add_argument("-v", "--version", action="version", version="%s %s" % (p_name, version))

# Creation of subparsers
subparsers = parser.add_subparsers(help="commands", dest="sub_name")

# The tweet command options
tweet_parser = subparsers.add_parser("tweet", help="Send a tweet to twitter.")
tweet_parser.add_argument("string", action="store", help="The tweet to send to twitter.")
     
# The ed command options
ed_parser = subparsers.add_parser("ed", help="An education? twitter bot.")

# The List_check command options
list_check_parser = subparsers.add_parser("list_check", help="Checks a list for character counts and reports a line over 140 characters.")
list_check_parser.add_argument("file", action="store", help="Check a file to assure every tweet is less than 140 characters. If not, the line is printed." )

# The #FFBot command options
ffbot_parser = subparsers.add_parser("ffbot", help="Sends #ff tweets made from a specified list.")


# Assign options given to the variable 'args' 
args = parser.parse_args()

# The tweet command code
if args.sub_name == "tweet":
    api = lib_func.new_auth(AK, AS, CK, CS)
    try:
        api.update_status(str(args.string))
    except tweepy.error.TweepError:
        print "Duplicate tweet"
    exit()

# The ed Command code
elif args.sub_name == "ed":
    
    api = lib_func.new_auth(AK, AS, CK, CS)
    lib_func.logo(p_name)
    
    print "Welcome to the Ed Interactive Menu"
    print "====================================="
    print p_name, """Copyright (C) 2010-2012  GodsOfLiberty
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions."""
    print ""
    print ""
    
    # Get a list of files and display a menu
    intro_list =[]
    
    for filename in os.listdir(path_intros):
        intro_list.append(filename)
    lib_func.list_menu(intro_list)
    print ""
    
    choice = raw_input("Pick an ed intro file: ")
    intro_file = path_intros + lib_func.list_choice(intro_list, choice)
    intro = lib_func.random_intro(intro_file)
    print choice
    print ""
    
    time_choice = int(raw_input("Enter the Number of Seconds between tweets: "))
    wait = time_choice
    results = lib_func.test_secs(wait)
    if results == True:
        print wait
        print ""
        
        ed_list =[]
        for filename in os.listdir(path_ed):
            ed_list.append(filename)
        lib_func.list_menu(ed_list)
        print ""
        
        ed_choice = raw_input("Pick an ed file: ")
        ed_file = path_ed + lib_func.list_choice(ed_list, ed_choice)
        print ed_choice
        print ""
        
        ed_exit_tweet = lib_func.random_intro(ed_exit)                                  
        lib_func.ed(api, wait, intro, ed_file, ed_exit_tweet)
        print""
        print "%s is finished." % p_name
        exit()
    else:
        print "Time out of range."
        exit()
    
# The list_check command code
elif args.sub_name == "list_check":
    if args.file:
        arg = str(args.file)
        lib_func.list_check(arg, p_name)
    else:
        print "Can't find file."
        exit()
    exit() 
        
# The ffbot command code
elif args.sub_name == "ffbot":
    
    api = lib_func.new_auth(AK, AS, CK, CS)
    username = api.me().screen_name
    lib_func.logo(p_name)
    
    print "Welcome to the ffbot Interactive Menu"
    print "====================================="
    print p_name, """Copyright (C) 2010-2012  godsofliberty
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions."""
    print""
    
    twitter_lists = lib_func.get_lists(api)
    lib_func.list_menu(twitter_lists)
    user_choice = int(raw_input("Enter the number corresponding to the list you want to tweet: "))
    ff_list_choice = lib_func.list_choice(twitter_lists, user_choice)
    print user_choice
    print""
    
    time_choice = int(raw_input("Enter the Number of Seconds between tweets: "))
    wait = time_choice
    results = lib_func.test_secs(wait)
    if results == True:
        print wait
        print""
        
        ff_intro_list =[]
        for filename in os.listdir(path_intros):
            ff_intro_list.append(filename)
        lib_func.list_menu(ff_intro_list)
        print ""
        
        choice = raw_input("Pick an #FF intro file: ")
        intro_file = path_intros + lib_func.list_choice(ff_intro_list, choice)
        intro = lib_func.random_intro(intro_file)
        print choice
        print ""

        ff_exit_tweet = lib_func.random_intro(ff_exit)
        
        print "%s is working..." % p_name
        print ""
        
        print intro
        print ""
        lib_func.follow_friday(api, username, ff_list_choice, intro, ff_exit_tweet, wait, p_name)
        print ff_exit_tweet
        print""
        print "%s is finished." % p_name
    else:
        print "Can't find file."
        exit()
    exit()
        
