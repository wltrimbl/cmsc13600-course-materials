'''keyword_search.py shows the basic structure of indexing using python dictionaries.
'''

#Some imports
import time, logging, sys
import pandas as pd

'''This code sets up logging and display for class
'''
root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(open('out.log', 'w'))
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)
pd.set_option('display.max_colwidth', 500)


def load_tweets(file):
    '''load_tweets loads data from the Tweets.csv file into a pandas dataframe
    '''
    start = time.perf_counter()
    
    #loading the file
    df = pd.read_csv(file)

    end = time.perf_counter()
    logging.info('Load_Tweets took ' + str(end-start) + ' seconds')
    logging.info('Load_Tweets found ' + str(len(df)) + ' Tweets')

    #clean up the text strip all punctuation
    df['text'] = df['text'].str.replace('[^\w\s]',' ')

    return df


def naive_find_tweets_1word(data, keyword):
    '''Searches through the data to find all tweets that contain a single word. We'll make this interesting
    and make it case insensitive.
    '''
    start = time.perf_counter()

    logging.info('naive_find_tweets_1word searching for ' + keyword)

    result = []

    for i, row in data.iterrows():

        #why???
        if keyword.lower() in row['text'].lower().split():

            result.append(i)


    end = time.perf_counter()
    logging.info('naive_find_tweets_1word took ' + str(end-start) + ' seconds')
    logging.info('naive_find_tweets_1word found ' + str(len(result)) + ' tweets')

    return df.iloc[result,:]

def build_index_tweets_1word(data):
    '''build index builds a dictionary data structure that we can re-use across the tweets 
    '''
    start = time.perf_counter()

    index = {}

    for i, row in data.iterrows():

        for word in row['text'].lower().split():

            if not word in index:
                index[word] = []

            index[word].append(i)

    end = time.perf_counter()
    logging.info('build_index_tweets_1word took ' + str(end-start) + ' seconds')
    logging.info('build_index_tweets_1word found ' + str(len(index)) + ' distinct words')

    return index


def index_find_tweets_1word(data, index, keyword):
    '''Searches through the data to find all tweets that contain a single word. We'll make this interesting
    and make it case insensitive.
    '''
    start = time.perf_counter()

    logging.info('index_find_tweets_1word searching for ' + keyword)

    result = index[keyword]

    end = time.perf_counter()
    logging.info('index_find_tweets_1word took ' + str(end-start) + ' seconds')
    logging.info('index_find_tweets_1word found ' + str(len(result)) + ' tweets')

    return df.iloc[result,:]


def naive_find_tweets_phrase(data, phrase):
    '''Searches through the data to find all tweets that contain a phrase (which can be multiple words!)
    '''
    start = time.perf_counter()

    logging.info('naive_find_tweets_phrase searching for ' + phrase)

    result = []

    for i, row in data.iterrows():

        #Changed!! Why?
        if phrase.lower() in row['text'].lower():
            result.append(i)


    end = time.perf_counter()
    logging.info('naive_find_tweets_phrase took ' + str(end-start) + ' seconds')
    logging.info('naive_find_tweets_phrase found ' + str(len(result)) + ' tweets')

    return df.iloc[result,:]


def index_find_tweets_phrase_v1(data, index, phrase):
    '''first version looks at all tweets that contain any of the words
    '''
    start = time.perf_counter()

    logging.info('index_find_tweets_phrase_v1 searching for ' + phrase)

    result = []

    #build a list of candidate tweets
    candidates = set()
    for word in phrase.lower().split():
        candidates = candidates.union(set(index[word]))

    logging.info('index_find_tweets_phrase_v1 considering ' + str(len(candidates)) + ' candidates')

    #filter the list of candidate tweets
    for candidate in candidates:
        if phrase.lower() in df.iloc[candidate,10].lower():
            result.append(candidate)

    end = time.perf_counter()
    logging.info('index_find_tweets_phrase_v1 took ' + str(end-start) + ' seconds')
    logging.info('index_find_tweets_phrase_v1 found ' + str(len(result)) + ' tweets')

    return df.iloc[result,:]


def index_find_tweets_phrase_v2(data, index, phrase):
    '''first version looks at all tweets that contain any of the words
    '''
    start = time.perf_counter()

    logging.info('index_find_tweets_phrase_v2 searching for ' + phrase)

    result = []

    #build a list of candidate tweets
    candidates = set()
    for word in phrase.lower().split():

        if len(candidates) == 0:
            candidates = set(index[word])
        else:
            candidates = candidates.intersection(set(index[word]))

    logging.info('index_find_tweets_phrase_v2 considering ' + str(len(candidates)) + ' candidates')

    #filter the list of candidate tweets
    for candidate in candidates:
        if phrase.lower() in df.iloc[candidate,10].lower():
            result.append(candidate)

    end = time.perf_counter()
    logging.info('index_find_tweets_phrase_v2 took ' + str(end-start) + ' seconds')
    logging.info('index_find_tweets_phrase_v2 found ' + str(len(result)) + ' tweets')

    return df.iloc[result,:]


'''keywords
'''
"""
#naive
df = load_tweets('Tweets.csv')
print(naive_find_tweets_1word(df, 'landing')['text'])
print(naive_find_tweets_1word(df, 'lax')['text'])
print(naive_find_tweets_1word(df, 'pilot')['text'])

#with index
df = load_tweets('Tweets.csv')
index = build_index_tweets_1word(df)
print(index_find_tweets_1word(df, index, 'landing')['text'])
print(index_find_tweets_1word(df, index,'lax')['text'])
print(index_find_tweets_1word(df, index, 'pilot')['text'])
"""


'''phrases
'''
#naive
df = load_tweets('Tweets.csv')
print(naive_find_tweets_phrase(df, 'bad weather')['text'])
print(naive_find_tweets_phrase(df, 'landing gear failure')['text'])

print('----')

#v1
df = load_tweets('Tweets.csv')
index = build_index_tweets_1word(df)
print(index_find_tweets_phrase_v1(df, index, 'bad weather')['text'])
print(index_find_tweets_phrase_v1(df, index, 'landing gear failure')['text'])


#v2
df = load_tweets('Tweets.csv')
index = build_index_tweets_1word(df)
print(index_find_tweets_phrase_v2(df, index, 'bad weather')['text'])
print(index_find_tweets_phrase_v2(df, index, 'landing gear failure')['text'])
