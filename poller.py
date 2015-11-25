# -*- coding: utf-8 -*-

import tweepy
import datetime
import sys
import os
import random
from subprocess import call
from game_secrets import *

from settings import DB_PATH, STRINGS, DEBUG, HASH_HOME
from sqlalchemy import create_engine, desc
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

if session.query(Question).count() == 0:
	sys.exit(0)

game_over = False
curr_question = session.query(Question).order_by(desc(Question.datestamp))[0]
if curr_question.solver:
	game_over = True

end_time = datetime.datetime.combine(datetime.date.today(), datetime.time(18,00))
if datetime.datetime.now() > end_time and not game_over:
	no_winners = random.choice(STRINGS['no_winners'])
	no_winners = no_winners.replace('{{ ANSWER }}', curr_question.answer)
	if not DEBUG:
		api.update_status(no_winners)
	else:
		print no_winners
	curr_question.solver = 'davidhashelhoff'
	session.commit()

mentions = api.mentions_timeline(count=50, since_id=curr_question.status)

for mention in reversed(mentions):
	text = mention.text.lower()
	text = text.replace('@davidhashelhoff', '').strip()
	username = mention.user.screen_name

	if username != 'davidhashelhoff':
		if game_over:
			already_over = random.choice(STRINGS['already_over'])
			if not DEBUG:
				api.update_status("@"+username+" "+already_over)
			else:
				print "@"+username+" "+already_over
		else:
			if curr_question.answer.lower() == text:
				right_answer = random.choice(STRINGS['right_answer'])
				right_answer = right_answer.replace('{{ WINNER }}', "@"+username)
				if not DEBUG:
					api.update_status(right_answer)
					call(["sudo",HASH_HOME+"/servo.py"])
				else:
					print right_answer
				curr_question.solver = username
				curr_question.solvetime = datetime.datetime.now()
				session.commit()
			else:
				wrong_answer = random.choice(STRINGS['wrong_answer'])
				wrong_answer = wrong_answer.replace('{{ PLAYER }}', "@"+username)
				if not DEBUG:
					api.update_status(wrong_answer)
				else:
					print wrong_answer
	curr_question.status = mention.id

session.commit()
	
