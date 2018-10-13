# RAILWAY_ML
CLASSIFICATION OF RAILWAY COMPLAINTS LETTER INTO THEIR RESPECTIVE DEPARTMENTS AND ZONES

Main problem with this project was that it doesn't has any standard data set. First step was to prepare data set, classify them manually. Then clean them so ML model can be trained and extract relevant things like place, date, time etc mentioned in them and than classify them.

Tweets were extracted using TWEEPY from handle of @RailMinindia and indian railway and piyush goyal. All complaint was saved in json format. Beautifulsoup was used for web scrapping. it was used to extract complaint from indian railway complaint board. It was also used to extract train schedule from a Travelkhana's website. We also extracted zone list using this.


After extraction, we distributed them along some of my friends and told them to classify it manually into different department like
1. Commercial
2.safety and  Maintenance 
3.Lost and found
4. Health
5.Financial
6. Unclassified
And we also told them to prepare 'hotwords' due to which they think that this should belong to this department.

#data cleaning
This was toughest work after preparing data set. Indian complaint are neither in English nor in Hindi, they are mixture of these. Extracted complaint was in raw format so a lot of cleaning was required, we used NLTK and regular expression to clean data.
A much object standardization was required like to convert plz into please.


#model training
We used tfid vectorizer to convert text into words so that ML models could be trained on them. We also used hotword as prepared as our feature in ML model. This way we found department of complaint.

To find region of complaint, we extracted pnr number to track location of train at time of complaint or place mentioned in complaint to decide it's region.
