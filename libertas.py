#!/usr/bin/env python
import tweepy
import os
import time
from libertas_functions import *
import argparse
from argparse import RawTextHelpFormatter

# variables   
p_name = "Libertas 2.0 http://godsofliberty.github.com/libertas/"
# API Keys
acc_key = "data/keys/acc_key.txt"
acc_sec = "data/keys/acc_sec.txt"
con_keys = "data/keys/con_key.txt"
con_secret = "data/keys/con_sec.txt"
default_ff_intro = "data/access/ff_intros/ff_lib_intros.txt"
default_ed_intro = "data/access/ed_intros/ed_intros.txt"
ff_exit_file="data/access/ff_exits/ff_exits.txt"
ed_exit_file="data/access/ed_exits/ed_exits.txt"
     
parser = argparse.ArgumentParser(prog="libertas", formatter_class=RawTextHelpFormatter, description="""Libertas is a set of cli tools for twitter with activism in mind. It includes a cli tweet, #FF bot and more.

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

parser.add_argument("-v", "--version", action="version", version="%(prog)s 2.0")
subparsers = parser.add_subparsers(help="commands", dest="sub_name")

# The tweet command
tweet_parser = subparsers.add_parser("tweet", help="Send a tweet to twitter.")
tweet_parser.add_argument("string", action="store", help="The tweet to send to twitter.")
     


# The ed command.
ed_parser = subparsers.add_parser("ed", help="A libertarian quote tweeter bot.")
ed_parser.add_argument("ed_files", action="store", help="File of quotes to send.")
ed_parser.add_argument("-s", "--seconds", action="store", dest="secs", help="Wait between tweets: 30-3600. Default=300", type=int)
ed_parser.add_argument("-i", "--intro", help="The ed intro file. Default=data/acsess/ed_intros/ed_intros.txt")
ed_parser. add_argument("-e", "--exits", help="The ed exit file. Default=data/acsess/ed_exits/ed_exits.txt")

# The List_check command
list_check_parser =subparsers.add_parser("list_check", help="Checks a list for character counts and reports a line over 140 characters.")
list_check_parser.add_argument("file", action="store", help="Check a file to assure every tweet is less than 140 characters. If not, the line is printed." )

# The #FFBot command
ffbot_parser = subparsers.add_parser("ffbot", help="Sends #ff tweets made from a specified list.")
ffbot_parser.add_argument("-l", "--list", action="store", dest="tlist", help="Number corresponding to the twitter list. You can get this value by first running ffbot with no options. Default=0 (the top list)", type=int)
ffbot_parser.add_argument("-s", "--seconds", action="store", dest="secs", help="Seconds to wait between tweets: 30-3600. Default=300", type=int)
ffbot_parser.add_argument("-f", "--file", help="File with intros, separated by line breaks. This list will be randomized, and one line will be selected. Default=data/access/ff_intros/ff_lib_intros.txt")
 
args = parser.parse_args()


 
# The tweet command code
if args.sub_name == "tweet":
    api = new_auth(acc_key, acc_sec, con_keys, con_secret)
    try:
        api.update_status(str(args.string))
    except tweepy.error.TweepError:
        print "Duplicate tweet. Wait a while before you tweet that again."
    exit()

# The ed Command code
elif args.sub_name == "ed":
    print "Libertas ed initialized..."
    api = new_auth(acc_key, acc_sec, con_keys, con_secret)
    
    if args.ed_files:
        quote_list = str(args.ed_files)
        
    else:
        print "No such file"
    if args.secs == None:
        wait = 300
    else:
        wait = args.secs
        results = test_secs(wait)
        if results == True:
            pass
        else:
            print wait, "is out of range."    
    ed_intro_file=args.intro
    if ed_intro_file == None:
        ed_intro_file = default_ed_intro
    ed_intro = random_intro(ed_intro_file)
    if args.exits:
        ed_exit_file = args.exits
    else:
        ed_exit = random_intro(ed_exit_file)
    ed(api, wait, ed_intro, quote_list, ed_exit)
    exit()
# The list_check command code
elif args.sub_name == "list_check":
    if args.file:
        arg = str(args.file)
        list_check(arg, p_name)
    else:
        print "Can't find file."
    exit() 
        
# The ffbot command code
# Setting Defaults     
elif args.sub_name == "ffbot":
    api = new_auth(acc_key, acc_sec, con_keys, con_secret)
    username = api.me().screen_name
    if args.tlist==None and args.secs==None and args.file==None:
        logo(p_name)
        print "Welcome to the ffbot Interactive Menu"
        print "====================================="
        print p_name, """Copyright (C) 2010-2012  godsofliberty
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions."""
        twitter_lists = get_lists(api)
        list_menu(twitter_lists)
        user_choice = int(raw_input("Enter the number corresponding to the list you want to tweet: "))
        choice = list_choice(twitter_lists, user_choice)
        print choice                                  
        time_choice = int(raw_input("Enter the Number of Seconds between tweets: "))
        wait = time_choice
        results = test_secs(wait)
        if results == True:
            print wait
            user_file = str(raw_input("Enter full path to file to be scanned for an intro: "))
            if user_file == "":
                user_file = default_ff_intro
            intro_file = random_intro(user_file)
            exit_tweet = random_intro(ff_exit_file)
            print p_name + " is working..."
            print intro_file
            follow_friday(api, username, choice, intro_file, exit_tweet, wait, p_name)
            print exit_tweet
            print p_name + "is finished."
        else:
            exit()
            
        exit()
    elif args.tlist == None and args.secs == None:
        args.tlist = 0
        args.secs = 300
    elif args.tlist == None and args.file == None:
        args.tlist = 0
        args.file = default_ff_intro
    elif args.secs == None and args.file == None:
        args.secs = 300
        args.file = default_ff_intro
    elif args.tlist == None:
        args.tlist = 0
    elif args.secs == None:
        args.secs = 300
    elif args.file == None:
        args.file = default_ff_intro
# Get the list to follow from twitter choose one.
    twitter_lists = get_lists(api)
    print twitter_lists
    choice = list_choice(twitter_lists, args.tlist)
# Set the seconds between tweets.
    wait = args.secs
    results = test_secs(wait)
    if results == True:
        pass
    else:
        print "seconds must be between 30 and 3600"
# Get the intro from the file
    intro = random_intro(args.file)
    exit_tweet = random_intro(ff_exit_file)
    print intro
# Set it in motion
    follow_friday(api, choice, p_name, intro, exit_tweet, wait, username)



