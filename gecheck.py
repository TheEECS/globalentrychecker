import time
import datetime
from selenium import webdriver
import logging
import smtplib

#Set up logging
logging.basicConfig(filename='path/to/globalentry.log',level=logging.INFO)
logging.info('Kicking off run at:'+ str(datetime.datetime.now()))
loginurl= 'https://goes-app.cbp.dhs.gov/goes/jsp/login.jsp'
day = ''
#Do not schedule dates
#Example
#blacklistdates = [datetime.datetime(2017,2,14)]
blacklistdates = []

#Path to your webdriver, I used Chrome
driver = webdriver.Chrome("/path/to/chromedriver")
driver.get(loginurl);
username = driver.find_element_by_name('j_username')
#Replace with your username
username.send_keys('username')
password = driver.find_element_by_name('j_password')
#Replace with your password
password.send_keys('password')
time.sleep(1)
logging.info('Logging in')
driver.find_element_by_id("SignIn").click()
time.sleep(2)
#Hit the human checkbox
logging.info('Checking that I am a person')
driver.find_element_by_id("checkMe").click()
time.sleep(1)
#Enter the Manage Appointment
driver.find_element_by_name("manageAptm").click()
#Figure out current interview date
elem = driver.find_elements_by_xpath('.//p')
for e in elem:
	if (e.text.find('Interview Date:') > -1):
		day = e.text
day = day.split(':')[1].strip()
day = day.replace(',','')
interviewday = datetime.datetime.strptime(day, '%b %d %Y')

logging.info('Current Interview Date:'+ str(interviewday))

driver.find_element_by_name("reschedule").click()
#Set your preferred interview location by finding the "value" of the radio button
#Example is set to SFO: driver.find_elements_by_css_selector("input[type='radio'][value='5446']")[0].click()
driver.find_elements_by_css_selector("input[type='radio'][value='Enter yours here']")[0].click()
driver.find_element_by_name("next").click()
elem = driver.find_elements_by_xpath("//*[contains(@id, 'scheduleForm:schedule1_header_')]")
currentday = elem[0].get_attribute("id")
currentday = currentday.split('_')[2].strip()
currentday = datetime.datetime.strptime(currentday, '%Y%m%d')

#If day is worse or same day as current
if (currentday >= interviewday):
	logging.info('Current best day is no better: ' + str(currentday))
#If day is in blacklist
elif (currentday in blacklistdates):
	logging.info('Blacklist time, skipping: ' + str(currentday))
#We got a hit!
elif (currentday < interviewday):
	logging.info('Better time available: ' + str(currentday))
	elem = driver.find_elements_by_css_selector("a.entry")[0].click()
	comments = driver.find_element_by_name('comments')
	#You need to enter some comments as to why you changed your appointment
	comments.send_keys('Comments')
	driver.find_element_by_name("Confirm").click()

	#Optional: Set up gmail to let you know
	fromaddr = 'fromuser@example.com'
	toaddrs  = 'touser@example.com'
	password = 'password'
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(fromaddr,password)
	msg = "\r\n".join([
	  "From: fromEmail",
	  "To: toEmail",
	  "Subject: New Global Entry Time!",
	  "",
	  'Better time available:' + str(currentday)
	  ])
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()
#Ok dunno what happened
else:
	logging.info('Unknown state, current best day is ' + str(currentday))
driver.quit()
