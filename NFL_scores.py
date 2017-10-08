import sopel
import requests
from bs4 import BeautifulSoup

# invoke bot with .nfl [team name]
@sopel.module.commands('nfl')

def scoreLookup(bot, trigger):
	team = trigger.group(2).lower()

	url = "http://www.nfl.com/liveupdate/scorestrip/ss.xml"
	response = requests.get(url)

	if (response.status_code == 200):
		soup = BeautifulSoup(response.content, 'html.parser')
		
		# search tags for our team name & grab the one that actually returns
		testCase1 = soup.find('g', vnn=team)
		testCase2 = soup.find('g', hnn=team)
		if (testCase1):
			tag = testCase1
		else:
			tag = testCase2
		
		# some formatting variables
		game_status = tag['q']
		home_score = tag['h'] + ' ' + tag['hs']
		visit_score = tag['vs'] + ' ' + tag['v']
		score_report = home_score + ' - ' + visit_score

		# check game status & report
		if (game_status == 'P'):
			bot.say('Pre-game ' + score_report)
			bot.say("Game time " + tag['d'] + " @ " + tag['t'] + ' Eastern')
		elif(game_status == 'H'):
			bot.say('Half-time ' + score_report)
		elif (game_status == 'F'):
			bot.say('Final ' + score_report)
		else: # game in progress!
			bot.say(score_report)
			bot.say(tag['k'] + ' remaining in Q' + tag['q'])

	else:
		bot.say("Status code " + response.status_code)