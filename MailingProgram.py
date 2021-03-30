import smtplib
#Does the same as the previous function, but sends a message to me specifically
def message(message):
	auth = ('senderstonk@gmail.com', 'stonkSender2021')
	server = smtplib.SMTP( "smtp.gmail.com", 587 )
	server.starttls()
	server.login(auth[0], auth[1])
	server.sendmail( auth[0], ['vmod2005@gmail.com'], message)
