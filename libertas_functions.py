import tweepy
import os
import time
import webbrowser
import random

# Check to see if is an integer
def is_integer(x):
    try:
        int(x)
        return True
    except ValueError:
        return False

# Reutrns False if not a number
def is_number(x):
    try:
        x + 1
        return True
    except TypeError:
        return False
        
# Turns a list into a menu
def list_menu(lists):
    count = len(lists)
    num = 0
    for item in lists:
        tac = str(num)
        num = num + 1
        print '('+tac+')', item

# Make sure the input entered is number
def check_num(uinput):
    if is_integer(uinput):
        num = int(uinput)
        if is_number(num):
            return True
        else:
            return False
    else:
        return False

# Get twitter PIN for Authorization
def get_pin(acc_key, acc_sec, con_keys, con_secret):
    # Get the pin
    auth = tweepy.OAuthHandler(con_keys, con_secret)
    auth_url = auth.get_authorization_url()
    webbrowser.open(auth_url)
    pin = raw_input("Enter the PIN: ")
    auth.get_access_token(pin)
    ACCESS_KEY = auth.access_token.key
    ACCESS_SECRET = auth.access_token.secret
    key_file = open(acc_key, 'w')
    key_file.write(ACCESS_KEY)
    key_file.close()
    sec_file = open(acc_sec, 'w')
    sec_file.write(ACCESS_SECRET)
    sec_file.close()
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    return tweepy.API(auth)

# Authorize from a file
def authorize(acc_key, acc_sec, con_keys, con_secret):
    key_file = open(acc_key)
    for key in key_file:
        ACCESS_KEY = key
    key_file.close()
    sec_file = open(acc_sec)
    for sec in sec_file:
        ACCESS_SECRET = sec
    sec_file.close()
    con_key = open(con_keys)
    for c_key in con_key:
        CONSUMER_KEY = c_key.strip()
    con_key.close()
    con_sec = open(con_secret)
    for c_sec in con_sec:
        CONSUMER_SECRET = c_sec.strip()
    con_sec.close()
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    return tweepy.API(auth)
    print [CONSUMER_SECRET, CONSUMER_KEY]
# Display the program name
def logo(p_name):
    os.system("clear")
    print""
    print p_name
    print""

#Check if authorization is new or already in a file
#ASSIGN TO api CALL THIS FUNCTION TO AUTHORIZE
def new_auth(acc_key, acc_sec, con_keys, con_secret):
    # Check to see if AccessKeys exist already, if not get PIN from twitter
    if os.path.exists(acc_key):
        if os.path.exists(acc_sec):
            api = authorize(acc_key, acc_sec, con_keys, con_secret)
            return api
        else:
            api = get_pin(acc_key, acc_sec, con_keys, con_secret)
            return api
    else:
        api = get_pin(acc_key, acc_sec, con_keys, con_secret)
        return api
    

def random_intro(i_file):
    # Load the intros from file and put them into a list.
    intro_list =[]
    intro_file = open(i_file)
    for selection in intro_file:
        intro_list.append(selection)
    intro_file.close()
    # Randomize the intro_list.
    list_length = (len(intro_list)) - 1
    random_intro = random.randint(0, list_length)
    selection = intro_list[random_intro]
    return selection


    
def list_choice(local_list, choice):
    # Get the user's choice, checks to make sure it is acceptable and set it as the list to #FF
    last = len(local_list)
    if check_num(choice):
        pick = int(choice)
        if pick in range(0, last):
            fflist = local_list[pick]
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
    if check_num(wait) == True:
        if int(wait) in range(30, 3601):
            secs = int(wait)
            return True
        else:
            return False

# Slices up the list to tweet, formats the tweets, and sends them.
def execute(api, fflist, p_name, libertas_intro, exit_tweet, secs, username):
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
    api.update_status(libertas_intro)
    time.sleep(10)
# Format the tweet making sure the bot stops when it runs out of members.
    ff = "#FF"
    while len(tweet) != 0:
        for tweet in tweet_list:
            tweet = tweet_list[tweet_start:tweet_stop]
            tweet_start = tweet_start + 6
            tweet_stop = tweet_stop + 6
            if len(tweet) !=0:
                almost_last_tweet = " ".join(tweet)
                final_tweet = ff, almost_last_tweet
                msg = " ".join(final_tweet)
                print msg
                api.update_status(msg)
                time.sleep(secs)
    logo(p_name)
    api.update_status(exit_tweet)

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
    
        


        
         
    
