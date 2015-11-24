#!/usr/bin/python

import urllib
import json
import re
import operator
import sys

def find_substitutes(text):
	pieces = re.findall(r'(?P<name>[A-Z][a-z]+\s[A-Z][a-z]+)([\'\s]+[^A-Z]+|$|[\.!,])', text)
	return [piece[0] for piece in pieces]

def load_articles(offset):
	url = "http://www.dailymail.co.uk/api/latest_headlines/home/%d.json" % (offset,)
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	return data

def load_comments(article_id):
	response = urllib.urlopen('http://www.dailymail.co.uk/reader-comments/p/asset/readcomments/'+str(article_id))
	data = json.loads(response.read())
	comments = []
	for comment in data['payload']['page']:
		comments.append(comment['message'].strip())
	return comments

def get_headline_options(n):
	articles_added = 0
	offset = 0
	options = []
	while articles_added < n:
		data = load_articles(offset)
		for article in data:
			if article['channel'] != 'tvshowbiz' and article['channel'] != 'femail':
				continue
			article_id = article['articleId']
			headline = article['socialHeadline']
			pieces = find_substitutes(headline)
			if len(pieces) == 0:
				continue
			for piece in pieces:
				if len(options) < n:
					options.append((headline, headline.replace(piece,'The Hoff'), piece))
			articles_added += 1
		offset += len(data)
	return options


