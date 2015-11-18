#!/usr/bin/python

import urllib
import json
import re
import operator

common_words = []
common = open('common_words.txt', 'r')
for word in common:
	common_words.append(word.rstrip())

all_words = {}
hints = {}
word_comments = {}

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

articles_added = 0
offset = 0
while articles_added < 200:
	data = load_articles(offset)
	for article in data:
		if article['channel'] != 'tvshowbiz' and article['channel'] != 'femail':
			continue
		article_id = article['articleId']
		print article_id, article['socialHeadline']
		comments = []
		if int(article['readerCommentsCount']) > 0:
			comments = load_comments(article_id)
		large_text = article['largePreviewText']
		original = large_text
		large_text = re.sub(r"'", ' ', large_text)
		result = re.sub(r'[^a-zA-Z\s]', '', large_text)
		for word in re.split('\s+', result):
			if len(word) < 5:
				continue
			if word.lower() == word:
				continue
			if word.lower() in common_words:
				continue
			found = False
			for common_word in common_words:
				if len(common_word) > 3 and word.startswith(common_word):
					found = True
			if found:
				continue
			if not word in all_words:
				all_words[word] = 0
				hints[word] = []
				word_comments[word] = []
			
			all_words[word] += 1
			for comment in comments:
				comment = comment.replace(word,"???").strip()
				if len(sentence) < 120 and len(comment) > 20 and not comment in word_comments[word]:
					word_comments[word].append(comment)
			sentences = re.split('\.\s+', original)
			sentences.append(article['socialHeadline'])
			for sentence in sentences:
				sentence = sentence.replace(word,"???").strip()
				if len(sentence) < 120 and len(sentence) > 20 and not sentence in hints[word]:
					hints[word].append(sentence)
		articles_added += 1
	offset += len(data)

sorted_x = sorted(all_words.items(), key=operator.itemgetter(1))

for w,a in sorted_x:
	if len(word_comments[w]) > 0:
		print "Count:",a
		print "Hints:"
		for hint in hints[w]:
			print "Article ->",hint
		for comment in word_comments[w]:
			print "Comment ->",comment
		print "Answer:",w
		print ""
