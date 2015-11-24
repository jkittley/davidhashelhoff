# -*- coding: utf-8 -*-

import tweepy
from game_secrets import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from headlines import get_headline_options
from models import Base, Question, QuestionOption
import datetime
import sys

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Read all the DMs for today
dms = api.direct_messages()
today = datetime.datetime.combine(datetime.date.today(), datetime.time(9))
print today
option = 0
for dm in reversed(dms):
	if dm.created_at > today:
		option = int(dm.text)

if option == 0:
	print "No option chosen."
	sys.exit(0)

engine = create_engine('sqlite:///hoff.db')
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

question_options = session.query(QuestionOption).filter_by(number=option)

if question_options.count() == 0:
	print "Invalid option selected."
	sys.exit(0)

question_option = question_options[0]

status = api.update_status(question_option.question)

question = Question(datestamp=today, 
	headline=question_option.headline, 
	question=question_option.question, 
	answer=question_option.answer,
	status=status.id)

session.add(question)
session.commit()
