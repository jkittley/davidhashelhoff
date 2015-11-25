# -*- coding: utf-8 -*-

import os
import tweepy
from settings import DB_PATH, DEBUG
from game_secrets import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from headlines import get_headline_options
from models import Base, Question, QuestionOption

engine = create_engine(DB_PATH)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

headlines = get_headline_options(5)

session.query(QuestionOption).delete()
text = ""
for i,headline in enumerate(headlines):
	(original,question,answer) = headline
	question_option = QuestionOption(number=i+1, headline=original, question=question, answer=answer)
	session.add(question_option)
	option = "(%d) %s [%s]" % (i+1, question, answer)
	text += option+"\n"
session.commit()

if not DEBUG:
	api.send_direct_message(screen_name='mikejewell', text=text)
	api.send_direct_message(screen_name='jkittley', text=text)
else:
	print text