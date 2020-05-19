# Wrote by Jacky Yuan @2016
# To run this, you can install BeautifulSoup
# https://pypi.python.org/pypi/beautifulsoup4
import urllib.request, urllib.parse, urllib.error
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re
import numpy
import os.path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#fname = input('Enter File:')

fname = "GP1-website.txt"
f=open(fname,'r')
fout = open('GP1-autofusion-website-meta-data.txt','w')
#print(f)
for url in f:
        url = url.rstrip()
        html = urlopen(url, context=ctx).read()
        soup = BeautifulSoup(html, "html.parser")
        fout.write("Client Website:"+(url)+"\n")
        metas = soup.find_all('meta')
        try:
            fout.write("1st H1 Tag:"+str(soup.find_all('h1')[0].text.strip())+"\n")
            fout.write("2nd H1 Tag:"+str(soup.find_all('h1')[1].text.strip())+"\n")
            fout.write("3rd H1 Tag:"+str(soup.find_all('h1')[2].text.strip())+"\n")
        except:
            fout.write("H1 Tag:"+str("Attention:None H1 Exist!")+"\n")
        fout.write("Meta Title:"+str(soup.title)+"\n")
        metastring= str([ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ])+"\n\n"
        fout.write("Meta Description:"+metastring)
f.close()
        #print (fout)
        #print (soup.h1)
        #print (soup.title)
        #print ([ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ])
        #print (url)
fout.close()

email_user = 'test@gmail.com' # Your Email Address
email_password = 'password!' #email_password
email_send = ['test@gmail.com'] # email address you want to send


subject = 'GP1 Daily Meta Data Result'

msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = ", ".join(email_send)
msg['Subject'] = subject


message = 'Hi there,\r\r\nSending this email from analytics team <H1 & Meta Data> Report for GP1 Client!\r\r\nOpen the txt file and Search(cmd+F) "Attention" to find out any missing H1 Tag.\r\r\nThank you! - Jacky Yuan\r\r\nSee the attached.'
msg.attach(MIMEText(message,'plain'))

filename='GP1-autofusion-website-meta-data.txt'
attachment  =open(filename,'rb')

part = MIMEBase('application','octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition',"attachment; filename= "+filename)

msg.attach(part)
text = msg.as_string()
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(email_user,email_password)


server.sendmail(email_user,email_send,text)
server.quit()
print("Success: Email sent!")
