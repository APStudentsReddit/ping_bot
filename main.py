import pyrebase
import discord
import asyncio
import time
import getpass
import config

client = discord.Client()
configkey = config.config_k

firebase = pyrebase.initialize_app(configkey)
storage = firebase.storage()
db = firebase.database()
auth = firebase.auth()
usernamel = ""
passwordl = ""
commands = ["*!pinggroup role*: Pings all members with role 'role'. If a user has executed this command in the past hour, it will return the time remaining until the user may ping a group again.", "*!pinggroup help*: Lists all commands."]

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	createornah = input("Do you have an existing account for APStudents - Ping Bot? (y/n)")
	if (createornah[0].lower() != 'y'):
		print("WARNING: Remember the details below for future use.")
		usernamel = input("Email: ")
		passwordl = getpass.getpass("Password: ")
		auth.create_user_with_email_and_password(usernamel, passwordl)
		user = auth.sign_in_with_email_and_password(usernamel, passwordl)
		user = auth.refresh(user['refreshToken'])
	else:
		print("Alright, proceed as usual:")
		usernamel = input("Email: ")
		passwordl= getpass.getpass("Password: ")
		user = auth.sign_in_with_email_and_password(usernamel, passwordl)
		user = auth.refresh(user['refreshToken'])
	print("You're set! Type !pinggroup name to ping a group named 'name'.")

@client.event
async def on_message(message):
	if message.content.startswith('!pinggroup'):
		#print("Logged in as %s"%usernamel)
		
		print("New message!")
		group = message.content.split('!pinggroup ')[1]
		if (group.lower() != "help"):
			print(db.child("users").child(message.author.id).get().val());
			if (db.child("users").child(message.author.id).get().val() != None):
				if(time.time()-(list(db.child("users").child(message.author.id).get().val().items())[0][1]) > 3600):
						members = message.server.members
						msg = ""
						await client.send_message(message.channel, "Pinging %s...." % group)
						for y in members:
							if group.lower() in [y.name.lower() for y in y.roles]:
								msg+="<@%s>, "%y.id
						await client.send_message(message.channel, "%s" % msg)
						user = auth.sign_in_with_email_and_password(user_name, pass_word)
						user = auth.refresh(user['refreshToken'])
						db.child("users").child(message.author.id).set(
							{
								"lastpinged": time.time()
							
							})
				else:
					timeleft = 60 - (time.time()-(list(db.child("users").child(message.author.id).get().val().items())[0][1]))/60
					await client.send_message(message.channel, "<@%s>, you've already done this in the past hour. There are %s minutes remaining until you can ping a group."%(message.author.id, timeleft))
			else:
					group = message.content.split('!pinggroup ')[1]
					members = message.server.members
					msg = ""
					await client.send_message(message.channel, "Pinging %s...." % group)
					for y in members:
						if group.lower() in [y.name.lower() for y in y.roles]:
								msg+="<@%s>, "%y.id
					await client.send_message(message.channel, "%s" % msg)
					
					db.child("users").child(message.author.id).set(
						{
							"lastpinged": time.time()
						
						})
		else:
			embed = discord.Embed(title="List of commands:", description='Here you go:', color=0x00ff00)
			for command in commands:
				embed.add_field(name="x", value=command+"\n", inline=False)

			await client.send_message(message.channel, embed=embed)

	

client.run(config.DISCORD_token)