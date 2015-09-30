#!/usr/bin/env python
#
# [milu_bot] to reply Telegram messages
# Query on:
#  - urbandict
#  - wolframalpha
#  - xkcd
# Change your telegramToken and wolframalphaAppId when you used code
# Copyright (C) 2015 khoai <dungcoivb@gmail.com>

import logging
import telegram
import wolframalpha
import urbandict
import os, random
import xkcd

dirXinh = 'xkcn'
listXinhUrl = 'xinh_urls.txt'
teleToken = '128856974:AAE2yeS_CLucntiQbwF4DCtnsL1ROPQNA4M'
wolfAppId = 'G3YRP3-G9L2GGJJVJ'
wCli = wolframalpha.Client(wolfAppId)

LAST_UPDATE_ID = None

def pod2text(wres):
	for pod in wres.pods:
		print ' - ', pod.title
		if not pod.title.startswith('Input'):
			if pod.text and pod.text.strip():
				aws = pod.text.strip()
				return aws.replace('|', ':')
	return ''

def queryUrbandict(query):
	uRes = urbandict.define(query)
	if len(uRes) > 0:
		for word in uRes:
			if 'def' in word:
				return word['def']

def queryWolf(query):
	#WolframAlpha query
	wRes = wCli.query(query)
	return pod2text(wRes)

def randXinh():
	while True:
		file = random.choice(os.listdir(dirXinh))
		if file[-3:] == 'jpg':
			return dirXinh + '/' + file

xinhUrls = open(listXinhUrl).read().splitlines()
def randXinhUrl():
	url = random.choice(xinhUrls)
	return url

listGoQuery = [queryUrbandict, queryWolf]

def randXkcd():
	comic = xkcd.getRandomComic()
	url = comic.getImageLink()
	return url

def milu(bot):
	global LAST_UPDATE_ID

	# Request updates after the last updated_id
	for update in bot.getUpdates(offset=LAST_UPDATE_ID, timeout=10):
		# chat_id is required to reply any message
		chat_id = update.message.chat_id
		msg = update.message.text.encode('utf-8')
		answer = ''
		if not msg:
			LAST_UPDATE_ID = update.update_id + 1
			continue

		print ' - chat_id=' + str(chat_id) +', msg=' + msg
		# implement [go] command
		if msg.startswith('/go'):
			try:
				question = msg[3:].strip()
				for query in listGoQuery:
					answer = query(question)
					if answer:
						break
			except:
				pass

		# implement [xinh] command
		if msg.startswith('/xinh'):
			try:
				answer = ''
				bot.sendPhoto(chat_id=chat_id, photo=randXinhUrl())
			except:
				pass

		# implement [xinh] command
		if msg.startswith('/xkcd'):
			try:
				answer = ''
				bot.sendPhoto(chat_id=chat_id, photo=randXkcd())
			except:
				pass

		if answer:
			print ' -> ', answer
			bot.sendMessage(chat_id=chat_id,
							text=answer)
		LAST_UPDATE_ID = update.update_id + 1

def main():
	global LAST_UPDATE_ID
	logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	bot = telegram.Bot(teleToken)
	try:
		LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
	except IndexError:
		LAST_UPDATE_ID = None

	print '[+] Milu start'
	while True:
		try:
			milu(bot)
		except ValueError:
			pass
	print '[+] Milu stop'

if __name__ == '__main__':
	main()
