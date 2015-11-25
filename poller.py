# -*- coding: utf-8 -*-

import tweepy
import datetime
import sys
import os

from game_secrets import *
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from headlines import get_headline_options
from models import Base, Question, QuestionOption

HASH_HOME = os.path.dirname(os.path.realpath(__file__))
DB_PATH = 'sqlite:///'+HASH_HOME+'/hoff.db'

engine = create_engine(DB_PATH)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

if session.query(Question).count() == 0:
	sys.exit(0)

curr_question = session.query(Question).order_by(desc(Question.datestamp))[0]
if curr_question.solver:
	# Already solved.
	sys.exit(0)

end_time = datetime.datetime.combine(datetime.date.today(), datetime.time(18,00))
if datetime.datetime.now() > end_time:
	api.update_status("No-one rang my bell :( I was looking for: "+curr_question.answer)
	curr_question.solver = 'davidhashelhoff'
	session.commit()

mentions = api.mentions_timeline(count=50, since_id=curr_question.status)

for mention in reversed(mentions):
	text = mention.text.lower()
	text = text.replace('@davidhashelhoff', '').strip()
	username = mention.user.screen_name
	if curr_question.answer.lower() == text:
		api.update_status("@"+username+" You rang my bell!")
		curr_question.solver = username
		curr_question.solvetime = datetime.datetime.now()
		session.commit()
	else:
		api.update_status("@"+username+" Not this time, buddy!")
	curr_question.status = mention.id

session.commit()
	
