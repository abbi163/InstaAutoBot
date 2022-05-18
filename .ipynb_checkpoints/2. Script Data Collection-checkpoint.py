## Data Collection using Instaloader API !!

# ! pip install instaloader

import threading
from instaloader import Instaloader, Profile
from itertools import dropwhile, takewhile
from datetime import date, datetime
from datetime import timedelta
from instaloader.exceptions import BadResponseException
import time
import pandas as pd


# Necessary function !

def login(USER, PASSWORD):
    """ 
        Returns loaders 
    
        PARAMETER:
            USER : Instagram Username
            PASSWORD : Instagram Password
    """
    loader = Instaloader()
    loader.login(USER, PASSWORD)  
    return loader
    
def get_users(hashtag=None, loader=None):
    """
    
    Parameters :
        hashtag - Input hashtag in string format without '#'
                  eg. get_users(hashtag="Photography", loader=loader)
    
    Return :
        user : list
            unique set of username
    
    """
    # get posts object 
    posts = loader.get_hashtag_posts(hashtag)

    # Get today, yesterday and day_before_yesterday dates !
    today = datetime.now()
    yesterday = today - timedelta(days = 1)
    day_before_yesterday = today - timedelta(days = 2)

    # Deciding dates for which posts need to be extracted !
    SINCE = today
    UNTIL = day_before_yesterday

    # Max user count !
    count_break = 50
    count = 0
    exception_count = 0
    # get users !
    users = []
    for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
        time.sleep(2)
        try:
            profile = post.owner_profile
            users.append(profile.username)
            count+=1
            if count>count_break:
                break;
        except BadResponseException:
            exception_count +=1
    print("total count : ", count)
    print("total exception count: ", exception_count)
    return list(set(users))

def get_followers(user_id=None, loader=None):
    """
    get followers of user_id
    
    """
    profile = Profile.from_username(loader.context, user_id)
    followers = list(set(profile.get_followers()))
    return [f.username for f in followers]

def collect_user_id(mode = 1, hashtag="", user_id = "", loader = None):
    """
    Parameters : 
        mode : INPUT (INTEGER) , mode in [1, 2, 3]
               
               if mode = 1 -> Collect only those users who have posted relevant hashtag 
               
               if mode = 2 -> Collect only those users who have posted relevant hashtag and there followers, 
               
               if mode = 3 -> Collect the followers of a given user id
    
    """
    
        

    if (mode == 1):
        if len(hashtag)==0:
            print("enter a valid hashtag in string format for mode 1 \n")
            print("eg : collect_user_id(mode=1, hashtag='photgraphy', loader=loader)")
        else:
            users = get_users(hashtag=hashtag, loader=loader)
            return users
        
    elif (mode == 2):
        if len(hashtag)==0:
            print("enter a valid hashtag in string format for mode 2 \n")
            print("eg : collect_user_id(mode=2, hashtag='photgraphy', loader=loader)")
        else:
            followers=[]
            users = get_users(hashtag=hashtag, loader=loader)
            for user in users:
                follower_list = get_followers(user_id = user, loader=loader)
                for f in follower_list:
                    followers.append(f)

                if len(followers) > 2000 :
                    break;

            # merging users and there followers into the same list and filtering out the duplicate entry !!
            users = list(set(users+followers))
            return users

    elif (mode == 3):
        if (len(user_id) == 0):
            print("enter a valid user_id in string format for mode 3 \n")
            print("eg : collect_user_id(mode=3, user_id ='instagram', loader=loader)")
        users = get_followers(user_id = user_id, loader=loader)
        if (len(users) == 0):
            print( "Note: No output had been recorded, Please check if user_id is public or private. Data extraction of only public account will happen.")
        return users

    else: 
        print ( "mode can only be 1, 2, or 3. Please check your input again or check the documentation of this function")
    
    

# Login and get loader 

USER = "abbi13011995"
PASSWORD = "3.141592653589"


loader=login(USER, PASSWORD)

# Existing users
df_userlist = pd.read_csv("data/UserList.csv")
existing_users = df_userlist.iloc[:,0].values.tolist()

# New users
users = collect_user_id(mode = 3, user_id="julian.starlights", loader=loader)

# Checking if new user is in existing users
existing_users = set(existing_users)
users = set(users)
new_users = users.difference(existing_users)

# Saving the data into DATA folder !!
df = pd.DataFrame(data=new_users, columns=["users"])
df["pic_like_status"] = "False"
df["userid_collection_date"] = date.today()
df["pic_like_date"] = ""
# if flag = 0, no interation had been done yet, if flag=1, interaction had been done, 
# we will ignore the account where flag=1
df["interaction_status"] = 0

# appending the dataframes together and saving the list
df_userlist = df_userlist.append(df)
df_userlist.to_csv("data/UserList.csv", index=None)

