# -*- coding: utf-8 -*-

import tweepy
import datetime
import sys
import os
import random
from game_secrets import *
from settings import DB_PATH, DEBUG, STRINGS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from headlines import get_headline_options
from models import Base, Question, QuestionOption

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Read all the DMs for today
dms = api.direct_messages()
today = datetime.datetime.combine(datetime.date.today(), datetime.time(9))
option = 0
for dm in reversed(dms):
	if dm.created_at > today:
		option = int(dm.text)

if option == 0:
	print "No option chosen."
	sys.exit(0)

engine = create_engine(DB_PATH)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

question_options = session.query(QuestionOption).filter_by(number=option)

if question_options.count() == 0:
	print "Invalid option selected."
	sys.exit(0)

question_option = question_options[0]

game_start = random.choice(STRINGS['game_start']) 
if not DEBUG:
	api.update_status(game_start)
	status_id = api.update_status(question_option.question).id
else:
	print game_start
	print question_option.question
	# Hardcoded ID for now
	status_id = 669476778105249792

question = Question(datestamp=today, 
	headline=question_option.headline, 
	question=question_option.question, 
	answer=question_option.answer,
	status=status_id)

session.add(question)
session.commit()
