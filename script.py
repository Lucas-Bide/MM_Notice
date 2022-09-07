# from datetime import datetime
import requests, json, sys, os
import xml.etree.ElementTree as ET
import smtplib, ssl
from email.message import EmailMessage

# Request in browser if you ever need to see keys.
url = "https://www.megamillions.com/cmspages/utilservice.asmx/GetLatestDrawData"
record = "jackpot.txt"
record_initial_value = "10000000" # 10-000-000.

# Retrieve the lotto data for the last play.
def retrieve_json():
	data = requests.get(url)
	# Response format is <string> *json* </string>.
	xml = ET.fromstring(data.content)
	return json.loads(xml.text)

# File record stores the next playable jackpot. Once the program is run
# the morning after the lotto is played, record is updated.
def update_record(jew):
	# Initialize record with initial record value.
	if not os.path.exists(record):
		with open(record, "x") as f:
			f.write(record_initial_value)

	f = open(record, "r+")

	jold = int(f.readline())
	f.seek(0)
	f.truncate()
	f.write(str(jew))
	f.close()

	return jold

def send_sms_via_email(
	message: str,
	subject: str = "MM Alert",
	smtp_server: str = "smtp.gmail.com",
	smtp_port: int = 465,
):


	number = os.getenv("mmNumber") # 10 digit number you're emailing.
	sender_email = os.getenv("genericEmail") # Sender email.
	email_password = os.getenv("genericEmailAppPassword") # Sender email's app password. Prerequisite: enable 2FA on your Gmail account.
	provider_domain = os.getenv("mmProvider") # Carrier's email to text gateway.
	receiver_email = f'{number}@{provider_domain}'

	email = EmailMessage()
	email['From'] = sender_email
	email['To'] = receiver_email
	email['Subject'] = subject
	email.set_content(message)


	context = ssl.create_default_context()
	with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
		smtp.login(sender_email, email_password)
		smtp.sendmail(sender_email, receiver_email, email.as_string())

	


if __name__ == "__main__":
	
	# Only run on Wednesday (2) and Saturday (5) - only necessary to use a free tier host service.
	# Will run at, say, 5 am, to avoid congested servers on high jackpots plays.
	# day = datetime.now().weekday()
	# if (day != 2 and day != 5):
	#	sys.exit()
	
	jsn = retrieve_json()
	# Jackpot new.
	jew = int(jsn["Jackpot"]["NextPrizePool"])
	# Jackpot old.
	jold = update_record(jew)

	if jold < 300000000 and jew >= 300000000: # Text to alert start of buy season.
		message = "Start buying MM. The current jackpot is ${:,}".format(jew)
		send_sms_via_email(message)

	if jsn["Jackpot"]["Winners"] > 0: # Text to alert that the jackpot was won.
		message = "The MM jackpot was won. Prize: ${:,}. \nNumbers: {} {} {} {} {} {}\n Winners: {}".format(jold, jsn["Drawing"]["N1"], jsn["Drawing"]["N2"], jsn["Drawing"]["N3"], jsn["Drawing"]["N4"], jsn["Drawing"]["N5"], jsn["Drawing"]["MBall"], jsn["Jackpot"]["Winners"])
		send_sms_via_email(message)









