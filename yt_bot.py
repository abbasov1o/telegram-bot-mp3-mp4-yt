#!/usr/bin/python

import requests, logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import token

TOKEN = token.Token().TOKEN

count = 0

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, parse_mode='Markdown', text=f"Eaeeee *{str(update.message.from_user.username)}* o/\nManda `/music` + o link do vídeo para baixar o mp3!\nManda `/video` + o link do vídeo para baixar o seu mp4!")

def message(bot, update):
	bot.send_message(chat_id=update.message.chat_id, parse_mode='Markdown', text='Digite `/music` + o link do vídeo para baixar o seu mp3!\nDigite `/video` + o link do vídeo para baixar o seu mp4!')

def music(bot, update, args):
	global count

	chatId = update.message.chat_id

	video_id = ''.join(args)

	if video_id.find('youtu.be') != -1:
		index = video_id.rfind('/') + 1
		video_id = video_id[index:][:11]

	elif video_id.find('youtube') != -1:
		index = video_id.rfind('?v=') + 3
		video_id = video_id[index:][:11]

	r = requests.get(f'https://api.pointmp3.com/dl/{video_id}?format=mp3')
	print(f'Status music code 1: {r.status_code}')

	json1_response = r.json()

	if not json1_response['error']:
		bot.send_message(chat_id=chatId, text='Consegui capturar seu vídeo, estou baixando! Um momento por favor.')

		redirect_link = json1_response['url']

		r = requests.get(redirect_link)
		print(f'Status music code 2: {r.status_code}')

		json2_response = r.json()

		if not json2_response['error']:
			payload = json2_response['payload']

			info = 'Título do vídeo: *{0}*\n✅ Quantidade de likes: *{1:,}*\n❌ Quantidade de dislikes: *{2:,}*'.format(payload['fulltitle'], payload['like_count'], payload['dislike_count'])

			try:
				bot.send_message(chat_id=chatId, parse_mode='Markdown', text=info)
				bot.send_photo(chat_id=chatId, photo=payload['thumbnail'])
				bot.send_audio(chat_id=chatId, audio=json2_response['url'])
				count += 1
				print("\033[1m\033[96m" + "Download count: " + str(count) + "\033[0m")
			except:
				bot.send_message(chat_id=chatId, text='Algo ocorreu de errado no download... Malz ae!')

def video(bot, update, args):
	global count

	chatId = update.message.chat_id

	video_id = ''.join(args)

	if video_id.find('youtu.be') != -1:
		index = video_id.rfind('/') + 1
		video_id = video_id[index:][:11]

	elif video_id.find('youtube') != -1:
		index = video_id.rfind('?v=') + 3
		video_id = video_id[index:][:11]

	r = requests.get(f'https://api.pointmp3.com/dl/{video_id}?format=mp4')
	print(f'Status video code 1: {r.status_code}')

	json1_response = r.json()

	if not json1_response['error']:
		bot.send_message(chat_id=chatId, text='Consegui capturar seu vídeo, estou baixando! Um momento por favor.')

		redirect_link = json1_response['url']

		r = requests.get(redirect_link)
		print(f'Status video code 2: {r.status_code}')

		json2_response = r.json()

		if not json2_response['error']:
			payload = json2_response['payload']

			info = 'Título do vídeo: *{0}*\n✅ Quantidade de likes: *{1:,}*\n❌ Quantidade de dislikes: *{2:,}*'.format(payload['fulltitle'], payload['like_count'], payload['dislike_count'])

			try:
				bot.send_message(chat_id=chatId, parse_mode='Markdown', text=info)
				bot.send_photo(chat_id=chatId, photo=payload['thumbnail'])
				bot.send_video(chat_id=chatId, video=json2_response['url'])
				count += 1
				print("\033[1m\033[96m" + "Download count: " + str(count) + "\033[0m")
			except:
				bot.send_message(chat_id=chatId, text='Algo ocorreu de errado no download... Malz ae!')


updater = Updater(token=TOKEN, request_kwargs={'read_timeout': 1000, 'connect_timeout': 1000})
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

music_handler = CommandHandler('music', music, pass_args=True)
dispatcher.add_handler(music_handler)

video_handler = CommandHandler('video', video, pass_args=True)
dispatcher.add_handler(video_handler)

message_handler = MessageHandler(Filters.text, message)
dispatcher.add_handler(message_handler)

updater.start_polling()
print('The bot has been started...')

updater.idle()
