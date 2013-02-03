import tweepy
import os
import time
import webbrowser
import random

# Libertas Functions Module

        
# Turns a list into a menu
def list_menu(lists):
    """Takes one parameter, a list, and prints it as a menu with index as selection."""
    for item in lists:
        selector = "(" + str(lists.index(item)) + ")"
        print selector, item

# Make sure the input entered is an integer number
def check_num(user_input):
    """Takes one parameter and returns True if it is a number of the integer type, False otherwise."""
    try:
        user_input + 1
        if isinstance(user_input, int):
            return True
        else:
            return False
    except TypeError:
        return False

# Get twitter PIN for Authorization
def get_pin(acc_key, acc_sec, con_keys, con_secret):
    """This function takes 4 file parameters. con_keys and con_secret contain the keys that are passed to Twitter.
    Twitter evaluates these keys and issues a PIN number to be entered by the user.
    The acc_key and acc_sec files are then written.
    All four of these keys are needed to authorize the program."""  
    with open(con_keys) as con_key:
        for c_key in con_key:
            CONSUMER_KEY = c_key.strip()
            
    with open(con_secret) as con_sec:
        for c_sec in con_sec:
            CONSUMER_SECRET = c_sec.strip()
            
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth_url = auth.get_authorization_url()
    webbrowser.open(auth_url)
    
    pin = raw_input("Enter the PIN: ")
    auth.get_access_token(pin)
    ACCESS_KEY = auth.access_token.key
    ACCESS_SECRET = auth.access_token.secret
    
    with open(acc_key, 'w') as key_file:
        key_file.write(ACCESS_KEY)
        
    with open(acc_sec, 'w') as sec_file:
        sec_file.write(ACCESS_SECRET)

    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    return tweepy.API(auth)

# Authorize from a file
def authorize(acc_key, acc_sec, con_keys, con_secret):
    """This function takes four file parameters containing the authorization keys.
    All four are opened, stripped of newline characters,
    and passed to Twitter for authorization."""
    with open(acc_key) as key_file:
        for key in key_file:
            ACCESS_KEY = key.strip()
            
    with open(acc_sec) as sec_file:
        for sec in sec_file:
            ACCESS_SECRET = sec.strip()
    
    with open(con_keys) as con_key:
        for c_key in con_key:
            CONSUMER_KEY = c_key.strip()
   
    with open(con_secret) as con_sec:
        for c_sec in con_sec:
            CONSUMER_SECRET = c_sec.strip()
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    return tweepy.API(auth)

# Display the program name
def logo(p_name):
    os.system("clear")
    print""
    print p_name
    print "http://godsofliberty.github.com/libertas/"
    print""

# Check if authorization is new
def new_auth(acc_key, acc_sec, con_keys, con_secret):
    """This function takes 4 file parameters containing the authorization keys.
    If the acc_key and acc_sec files exist pass them to the authorize function,
    else the get_pin function is called."""
    
    # Check to see if AccessKeys exist already, if not get PIN from twitter
    if os.path.exists(acc_key):
        if os.path.exists(acc_sec):
            api = authorize(acc_key, acc_sec, con_keys, con_secret)
            return api
        else:
            api = get_pin(acc_key, acc_sec, con_keys, con_secret )
            return api
    else:
        api = get_pin(acc_key, acc_sec, con_keys, con_secret )
        return api
    
def random_intro(i_file):
    # Load the intros from file and put them into a list.
    with open(i_file) as intro_file:
        intro_list = [selection.strip() for selection in intro_file]

    # determines the index range of the list and selects an index at random.
    list_length = (len(intro_list)) - 1
    random_intro = random.randint(0, list_length)
    selection = intro_list[random_intro] # Maps the index to the list item.
    return selection


    
def list_choice(local_list, choice):
    # Get the user's choice, checks to make sure it is acceptable and set it as the list to #FF
    last = len(local_list)
    if check_num(choice):
        if choice in range(0, last):
            fflist = local_list[choice]
            return fflist
        else:
            print "The number is out of range. Please choose a number between 0 and", last
    else:
        print "Try entering a number between 0 and", last

# Gets the twitter list of lists and ships them off to the list_menu function to be formatted
def get_lists(api):
    local_list =[]
    t_lists = tweepy.Cursor (api.lists).items()
    for i_list in t_lists:
        new_list = i_list.name
        local_list.append(new_list)
    return local_list
    
# Get the seconds and test the range.
def test_secs(wait):
    if check_num(wait):
        if wait in range(30, 3601):
            return True
        else:
            return False

# Slices up the list to tweet, formats the tweets, and sends them.
def follow_friday(api, username, fflist, libertas_intro, exit_tweet, secs, p_name):
# Get list members from the selected twitter list and add the @
    tweet_list =[]
    the_list = tweepy.Cursor(api.list_members, username, fflist).items()
    for user in the_list:
        tweeter = '@'+user.screen_name
        tweet_list.append(tweeter)
# Extract 6 users at a time from the list. Tweets only 6 names ata time to avoid going over 140
    tweet_start = 0
    tweet_stop =6
    tweet = "ok"
# Libertas Intro calls random_intro and sends the intro to twitter
    try:
        api.update_status(libertas_intro)
    except tweepy.error.TweepError:
        print "Duplicate tweet"
    time.sleep(10)
# Format the tweet making sure the bot stops when it runs out of members.
    ff = "#FF"
    while len(tweet) != 0:
        for tweet in tweet_list:
            tweet = tweet_list[tweet_start:tweet_stop]
            tweet_start = tweet_start + 6
            tweet_stop = tweet_stop + 6
            if len(tweet) !=0:
                name_string = " ".join(tweet)
                final_tweet = ff, name_string
                msg = " ".join(final_tweet)
                print msg
                try:
                    api.update_status(msg)
                except tweepy.error.TweepError:
                    print "Duplicate tweet"
                time.sleep(secs)
    logo(p_name)
    try:
        api.update_status(exit_tweet)
    except tweepy.error.TweepError:
        print "Duplicate tweet"
# list_check Function
def list_check(arg, p_name):
    logo(p_name)
    cfile = open(arg)
    count = 0
    for line in cfile:
        print len(line)
        count = count +1
        if len(line) -1 > 140:
            print "line", count, "is longer than 140 characters."
        else:
            print "ok"
    
# The ed bot
def ed(api, secs, intro, ed_file, extro):
    print intro
    try:
        api.update_status(intro)
    except tweepy.error.TweepError:
        print "Duplicate tweet"
    ed_tweets = []
    with open(ed_file) as qflist:
        for quote in qflist:
            ed_tweets.append(quote)
    for tweet in ed_tweets:
        print tweet
        try:
            api.update_status(tweet)
        except tweepy.error.TweepError:
            print "Duplicate tweet"
        time.sleep(secs)
    
    print extro
    try:
        api.update_status(extro)        
    except tweepy.error.TweepError:
        print "Duplicate tweet"
        
# Retweeter
def retweeter(api, result_list):
    count = 0
    while count != 24:
    
        search_result_object = result_list[count]
        try:
            api.retweet(search_result_object.id)
            count = count + 1
            time.sleep(60)
        except tweepy.error.TweepError:
            count = count + 1        
         
    
