# sopel-modules
Some modules for use with the Sopel IRC bot (https://sopel.chat)

# Modules

## Package Tracking (track.py)

This module adds a couple commands that allow users to track packages. 

### .track
The .track command tells the bot to look up tracking info for a package when you give a number with it, e.g.:

	<@user> .track 999999999999999

	<Sopel> Package status: FAILURE

	<Sopel> Status details: Shipment exception

	<Sopel> Location: Keasbey, NJ 08832

	<Sopel> Last updated: 2017-01-26 at 02:05:34

It works by first guessing the carrier using [tracking_url](https://pypi.python.org/pypi/tracking-url/0.0.2), and then using [Shippo](https://github.com/goshippo/shippo-python-client) to look up the tracking data. **You will need a shippo API key to use this module.**

### .mypkg
Allows users to maintain a personal list of packages, using Sopel's "memory" function. Has three commands: add, del, and list. List will look up tracking info for all packages in a user's list. Memory is stored by user nick.

	<@user> .mypkg add 999999999999999
	<Sopel> user: package added.


	<@user> .mypkg list
	<Sopel> user: you have 1 packages.
	<Sopel> Package status: FAILURE
	<Sopel> Status details: Shipment exception
	<Sopel> Location: Keasbey, NJ 08832
	<Sopel> Last updated: 2017-01-26 at 02:05:34


	<@user> .mypkg del 999999999999999
	<Sopel> user: package deleted.
