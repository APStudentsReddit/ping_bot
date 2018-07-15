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
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	createornah = input("Do you have an existing account for APStudents - Ping Bot? (y/n)")
	if (createornah[0].lower() != 'y'):
		print("WARNING: Remember the details below for future use.")
		user_name = input("Email: ")
		pass_word = getpass.getpass("Password: ")
		auth.create_user_with_email_and_password(user_name, pass_word)
	else:
		print("Alright, proceed as usual:")
		user_name = input("Email: ")
		pass_word = getpass.getpass("Password: ")
	print("You're set! Type !pinggroup name to ping a group named 'name'.")

@client.event
async def on_message(message):
	if message.content.startswith('!pinggroup'):
		print("New message!")
		print(db.child("users").child(message.author.id).get().val());
		if (db.child("users").child(message.author.id).get().val() != None):
			if(time.time()-(list(db.child("users").child(message.author.id).get().val().items())[0][1]) > 3600):
					group = message.content.split('!pinggroup ')[1]
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
				await client.send_message(message.channel, "<@%s>, you've already done this in the past hour."%message.author.id)
		else:
				group = message.content.split('!pinggroup ')[1]
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

	

client.run(config.DISCORD_token)