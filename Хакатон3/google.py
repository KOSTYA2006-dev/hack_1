# import smtplib

# smtpObj = smtplib.SMTP('smtp.gmail.com', 535)
# print(help(smtpObj))
# smtpObj.starttls()
# smtpObj.login('itcubeapp161@gmail.com','btmdytdxqlxgzvnc')
# smtpObj.sendmail("itcubeapp161@gmail.com","kp7145126@gmail.com", "go to bed!")
# smtpObj.quit()

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
 
# create message object instance
msg = MIMEMultipart()
 
 
message = "Привет"
 
# setup the parameters of the message
password = "btmdytdxqlxgzvnc"
msg['From'] = "itcubeapp161@gmail.com"
msg['To'] = "kp7145126@gmail.com"
msg['Subject'] = "Subscription"
 
# add in the message body
msg.attach(MIMEText(message, 'plain'))
 
#create server
server = smtplib.SMTP('smtp.gmail.com: 587')
 
server.starttls()
 
# Login Credentials for sending the mail
server.login(msg['From'], password)
 
 
# send the message via the server.
server.sendmail(msg['From'], msg['To'], msg.as_string())
 
server.quit()
 
print("successfully sent email to %s:" % (msg['To']))