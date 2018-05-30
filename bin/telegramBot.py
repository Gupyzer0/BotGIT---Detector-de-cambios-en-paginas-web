import telegram, logging

token_auth = ""
chat_id = ""

class TelegramBot():
	def __init__(self):
		try:
			self.bot = telegram.Bot(token=token_auth)
		except:
			logging.error("No se pudo iniciar el bot de telegram")
		else:
			self.id_chat = chat_id

	def enviarMensaje(self, texto):
		try:
			self.bot.send_message(chat_id=self.id_chat, text=texto)
			logging.info("Mensaje enviado por telegram")
		except:
			logging.error("No se pudo enviar el mensaje por Telegram")
