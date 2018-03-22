# -*- coding: utf-8 -*-
import telegrand, Settings, re

bot = telegrand.Bot(Settings.TELEGRAM_TOKEN)

def isAdmin(message):
	isAdmin = False
	adminsList = bot.req(
		"getChatAdministrators",
		data={
			"chat_id": message.chat.id
		}
	)
	for admin in adminsList:
		if message.from_user.id == admin.user.id:
			isAdmin = True
	return isAdmin

@bot.handle()
def do(message):

	try:
		message.new_chat_member
	except:
		pass
	else:
		try:
			ln = " " + message.new_chat_member.last_name
		except:
			ln = ""

		bot.req(
			"sendMessage",
			data={
				"text": Settings.WELCOME_MESSAGE % "%s%s" % (message.new_chat_member.first_name, ln),
				"chat_id": message.chat.id,
				"reply_to_message_id": message.message_id,
				"parse_mode": "HTML"
			}
		)

	try:
		message.text
	except:
		pass
	else:
		if not isAdmin(message) and re.match(r"((http)(s)?:\/\/)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-z]{1,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)", message.text, re.IGNORECASE):
			bot.req(
				"deleteMessage",
				data={
					"chat_id":  message.chat.id,
					"message_id": message.message_id
				}
			)

bot.polling()
