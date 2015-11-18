#!/usr/bin/python

import urllib
import json
import re
import operator
url = "http://www.dailymail.co.uk/api/latest_headlines/home/0.json"
response = urllib.urlopen(url)
data = json.loads(response.read())
common_words = []
common = open('common_words.txt', 'r')
for word in common:
	common_words.append(word.rstrip())

all_words = {}
hints = {}

for article in data:
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
		
		all_words[word] += 1
		sentences = original.split(". ")
		sentences.append(article['socialHeadline'])
		for sentence in sentences:
			sentence = sentence.replace(word,"???").strip()
			if len(sentence) < 120 and len(sentence) > 20 and not sentence in hints[word]:
				hints[word].append(sentence)

sorted_x = sorted(all_words.items(), key=operator.itemgetter(1))

for w,a in sorted_x:
	print "Count:",a
	print "Hints:"
	for hint in hints[w]:
		print "->",hint
	print "Answer:",w
	print ""
