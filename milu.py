#!/usr/bin/env python
#
# [milu_bot] to reply Telegram messages
# Query on urbandict and wolframalpha
# Change yout telegramToken and wolframalphaAppId when you used code
# Copyright (C) 2015 khoai <dungcoivb@gmail.com>

import logging
import telegram
import wolframalpha
import urbandict

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

listGoQuery = [queryUrbandict, queryWolf]

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

		# implement [go] command
		if msg.startswith('/go'):
			question = msg[3:].strip()
			print 'question:', question
			try:
				for query in listGoQuery:
					answer = query(question)
					print 'answer:', answer
					if answer:
						break
			except:
				pass

		# implement [xinh] command
		if msg.startswith('/xinh'):
			answer = 'implement at here'

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

	while True:
		milu(bot)

if __name__ == '__main__':
	main()
