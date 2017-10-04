import sopel.module
import tracking_url
import shippo
import json
 
shippo.api_key = "" # Insert your Shippo API key here.

@sopel.module.commands('track', 'mypkg')
def main(bot, trigger):
	command = trigger.group(1)

	def trackPackage(number):
		# guess carrier using tracking_url, then use Shippo to look up number + carrier
		carrier = tracking_url.guess_carrier(number).carrier
		tracking = shippo.Track.get_status(carrier, number)

		# make it an object and then pull the relevant info: 
		#   package status, details, last updated, location
		tracking = json.loads(str(tracking))

		status = tracking["tracking_history"][0]["status"]
		details = tracking["tracking_history"][0]["status_details"]
		last_updated = tracking["tracking_history"][0]["status_date"]
		
		# location parsing 
		city = tracking["tracking_history"][0]["location"]["city"]
		state = tracking["tracking_history"][0]["location"]["state"]
		postal = tracking["tracking_history"][0]["location"]["zip"]
		location = city + ", " + state + " " + postal

		# date/time parsing
		last_updated = last_updated.split('T')
		date = last_updated[0]
		time = last_updated[1].split('Z')[0]

		# report on all of this
		bot.say("Package status: " + status)
		bot.say("Status details: " + details) 
		bot.say("Location: " + location)
		bot.say("Last updated: " + date + " at " + time)

	if command == 'track':
			trackPackage(trigger.group(2))

	elif command == 'mypkg':
		# Get the user's list of packages and save it to pkg
		try:
			pkg = bot.memory[trigger.nick]["packages"]
		except:
			bot.memory[trigger.nick] = {}
			bot.memory[trigger.nick]["packages"] = []
			pkg = bot.memory[trigger.nick]["packages"]

		args = trigger.group(2).split(' ')
		if (args[0] == 'add'):
			bot.memory[trigger.nick]["packages"].append(args[1])
			bot.reply("package added.")

		elif (args[0] == 'del'):
			bot.memory[trigger.nick]["packages"].remove(args[1])
			bot.reply("package deleted.")

		elif (args[0] == 'list'):
			if (len(pkg) > 0): 
				bot.reply("you have " + str(len(pkg)) + " packages.")
				for number in pkg:
					trackPackage(number)
			else:
				bot.reply("you have no packages.")