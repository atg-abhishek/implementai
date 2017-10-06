import sys
import os
sys.path.append(os.path.join(os.getcwd(),'..'))
import watson_developer_cloud
import watson_developer_cloud.natural_language_understanding.features.v1 as Features
import pandas as pd
from pprint import pprint 

nlu = watson_developer_cloud.NaturalLanguageUnderstandingV1(version='2017-02-27',
                                                                username='username',
                                                                password='password')

def check_sentiment(text):

    response = nlu.analyze(
        text=text,
        features=[
            Features.Sentiment()
        ]
    )

    label = response['sentiment']['document']['label']
    score = response['sentiment']['document']['score']

    return score

def get_keywords(text):
    resp = nlu.analyze(
        text=text, 
        features=[
            Features.Keywords(
                emotion=True, 
                sentiment=True,
                limit=3
            )
        ]
    )

    pprint(resp)

get_keywords("Well this is complete shit, I absolutely hate this place!")
