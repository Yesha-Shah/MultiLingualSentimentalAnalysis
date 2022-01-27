import tweepy
import re
import classifier

access_key = "103589925-PYiNRi6sAoSAFCau7Q5zDAqF7Kt8WwsK5EunWL3I"
access_secret = "u8N1nS93eN5npmtBOAxCwJgZE0W4wPCNe1CEuCB9lEIys"
consumer_key = "IIFBxSZv8YnhRJuvvDJVkR4ht"
consumer_secret = "zou3XOVMDXp9esingDNEowUeEPmTKkY4daZGYdmalovyd9JCxr"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)

def fetch(query):
    pos = 0
    neg = 0
    cnt = 0
    newTweets=api.search(q=query, lang="hi",count=100)
    for tweet in newTweets:
        try:
            current = tweet.text
            if('RT' not in current):
                #Remove www.* or https?://* 
                current = re.sub('((www\.[\s]+)|(https?://[^\s]+))','',current)

                #Remove @username
                current = re.sub('@[^\s]+','',current)

                #Remove additional white spaces
                current = re.sub('[\s]+', ' ', current)

                #Replace #word with word Handling hashtags
                current = re.sub(r'#([^\s]+)', r'\1', current)

                #trim
                current = current.strip('\'"')

                res=classifier.fn1(current)
                print("##########", current)
                if res == "negative":
                    neg=neg+1
                elif res == "positive":
                    pos=pos+1
                cnt=cnt+1
                
        except UnicodeEncodeError:
            continue
        except Exception as e:
            break

    per1=((float(pos)/cnt)*100)
    per2=((float(neg)/cnt)*100)
    print("POSITIVE {0}%".format(per1))
    print("NEGATIVE {0}%".format(per2))

    return per1,per2

def main(keyword):
    
    print("\nFetching'{0}':\n".format(keyword))
    
    per1,per2=fetch(keyword)
    return per1,per2

if __name__ == "__main__":
    main()
