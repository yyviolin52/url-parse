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
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#fname = input('Enter File:')
def first_check_url():
    #print("test")
    fname = "GP1-website.txt"
    f=open(fname,'r')
    fout = open('meta-data-comparison.txt','w')
    #print(f)
    for url in f:
        url = url.rstrip()
        print(url)
        html = urlopen(url, context=ctx).read()
        soup = BeautifulSoup(html, "html.parser")
        metas = soup.find_all('meta')
        metastring= str([ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ])+"\n\n"
        firsth1 = str("H1 Tag:"+str(soup.h1)+"\n")
        fout.write(firsth1)
        fout.write(str(soup.title)+"\n")
        fout.write(metastring)
        seo_data=[firsth1,str(soup.title),metastring]
        meta_dict={}
        meta_dict[url]=seo_data
        numpy.save('data',meta_dict)
    f.close()

        #print (fout)
        #print (soup.h1)
        #print (soup.title)
        #print ([ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ])
        #print (url)
    fout.close()

def second_check_url():
    fname = "GP1-website.txt"
    f = open(fname,'r')
    fout1 = open('meta-data-comparison.txt','w')
    meta_dict = numpy.load('data.npy').item()
    fout = open('result.txt','w')
    #print(f)
    for url in f:
        url = url.rstrip()
        print('Second Check: '+url)
        html = urlopen(url, context=ctx).read()
        soup = BeautifulSoup(html, "html.parser")
        metas = soup.find_all('meta')
        metastring= str([ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ])+"\n\n"
        firsth1 = str("H1 Tag:"+str(soup.h1)+"\n")
        fout1.write(firsth1)
        fout1.write(str(soup.title)+"\n")
        fout1.write(metastring)
        seo_data=[firsth1,str(soup.title),metastring]
        if url in meta_dict.keys():
            if meta_dict[url]!=seo_data:
                meta_dict[url]=seo_data
                fout.write(url+", Meta has changed!\n")
            else:
                pass
                #fout.write(url+", Meta does not changed!\n")
             #meta_dict[url]=seo_data
        else:
            fout.write(url+", New Url has been added!\n")
            meta_dict[url]=seo_data
        numpy.save('data.npy',meta_dict)
    fout.close()
    fout1.close()
    f.close()

def send_email(subject,msg):
    try:
        email_user = 'test@gmail.com'
        email_password = 'password'
        email_send = ['test@gmail.com']

        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = ", ".join(email_send)
        msg['Subject'] = subject
        msg.attach(MIMEText(message,'plain'))
        text = msg.as_string()

        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email_user,email_password)
        server.sendmail(email_user,email_send,text)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")

if(os.path.exists("data.npy")):
    second_check_url()
    print("second check!")
    #msg = "Hello there, second check!"
    fname = "result.txt"
    f=open(fname,'r')
    result=f.read()
    f.close()
    if not result:
        subject = "No Changes for Meta Data"
        message = "Nothing Changed!"

    else:
        subject = "[Alerts]: Meta Data Changed!"
        message = result

    send_email(subject, message)

else:
    first_check_url()
    print("first check!")
