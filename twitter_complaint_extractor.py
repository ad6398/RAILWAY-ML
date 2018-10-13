#Importing libraries
import sys
import os
import jsonpickle
import tweepy
#Pass our consumer key and consumer secret to Tweepy's user authentication handler
auth = tweepy.OAuthHandler('####', '####')

#Pass our access token and access secret to Tweepy's user authentication handler
auth.set_access_token('##****', '##****')

#Creating a twitter API wrapper using tweepy
#Details here http://docs.tweepy.org/en/v3.5.0/api.html
api = tweepy.API(auth)

#Error handling
if (not api):
    print ("Problem connecting to API")
#Getting Geo ID for USA
places = api.geo_search(query="India", granularity="country")

#Copy USA id
place_id = places[0].id
print('India id is: ',place_id)

#Switching to application authentication
auth = tweepy.AppAuthHandler('###***', '###****')

#Setting up new api wrapper, using authentication only
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
 
#Error handling
if (not api):
    print ("Problem Connecting to API")

searchQuery = 'place:b850c1bfd38f30e0 @RailMinIndia OR #IndianRailway OR @PiyushGoyal OR #PiyushGoyal'

#Maximum number of tweets we want to collect 
maxTweets = 3200

#The twitter Search API allows up to 100 tweets per query
tweetsPerQry = 100

tweetCount = 0
d= open("guru99.txt","w+")

#Open a text file to save the tweets to
with open('complaints_railway.json', 'w') as f:

    #Tell the Cursor method that we want to use the Search API (api.search)
    #Also tell Cursor our query, and the maximum number of tweets to return
    for tweet in tweepy.Cursor(api.search,q=searchQuery,tweet_mode="extended").items(maxTweets) :         

        #Verify the tweet has place info before writing (It should, if it got past our place filter)
        if tweet.place is not None and tweet.lang=="en":
            
            #Write the JSON format to the text file, and add one to the number of tweets we've collected
            print(tweet.created_at)
            d.write("%s\n\n" % (tweet.full_text.encode('utf-8')))
            f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
            tweetCount += 1

    #Display how many tweets we have collected
    print("Downloaded {0} tweets".format(tweetCount))
d.close()





 



