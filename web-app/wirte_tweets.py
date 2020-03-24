import tweepy

def writeTweet(question, response, at=None):
    # keys
    api_key = 'xxxxxxxx'
    api_secret = 'xxxxxxxx'

    access_token = 'xxxxxxxx'
    access_secret = 'xxxxxxxx'

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)

    # Create API object
    api = tweepy.API(auth)

    # text generation
    # @adomaslingevici
    if at == None:
        at = '#answerthis'
    else:
        at = '@' + at + ' ' + '#answerthis'
    responseLen = len(response)
    lenIt = 220
    responseCount = round(responseLen/lenIt)   

    # Create a tweet
    a = api.update_status(str(at+' '+question))
    current_id = a.id
    for i in range(responseCount+1):
        start = i*lenIt
        end = (i+1)*lenIt
        usableResponse = response[start:end]
        b = api.update_status('['+ str(i+1)+ '] '+usableResponse ,in_reply_to_status_id = current_id)
        current_id = b.id
    api.update_status('get your answer at www.answerthis.xyz' ,in_reply_to_status_id = current_id)