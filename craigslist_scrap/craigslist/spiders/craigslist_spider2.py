#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#importing files for scraping of Data.
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from craigslist.items import CraigslistItem
from bs4 import BeautifulSoup
import urllib
from collections import defaultdict

#importing files for editing and sending mail.
import smtplib, os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

items = []
Dictionary = defaultdict(list)
class MySpider(BaseSpider):
    name = "craig"
    allowed_domains = ["craigslist.org"]
    scrap_site = raw_input("**Enter the full url to a craiglist page you want to scrap, otherwise press Enter for default url**\n")
    if scrap_site == "":
    	start_urls = ["http://sfbay.craigslist.org/sof/"]
    else:
	start_urls = scrap_site 
    def parse(self, response):
	username = raw_input("*******Enter your gmail email-id or press enter to use default:********\n")
    	password = raw_input("*******Enter your gmail password or press enter to use default:*******\n")
    	hxs = HtmlXPathSelector(response)
	titles = hxs.select("//span[@class='pl']")
	for titles in titles:
		item = CraigslistItem()
		item["title"] = titles.select("a/text()").extract()
		link_scraped = str(titles.select("a/@href").extract())
		link_replaced = link_scraped.translate(None, "[]'")
		link_replaced = link_replaced[1:]
		link = "http://sfbay.craigslist.org"+link_replaced
		item["link"] = link
		items.append(item)
	count = 0
	for item in items:
		link =  item["link"]
		sock = urllib.urlopen(link)
		htmlSource = sock.read()
		sock.close()
		soupy = BeautifulSoup(htmlSource)
		content_divs = soupy.findAll( attrs={'id':'postingbody'} )
		try:
			reply_link = soupy.find('a',{'class':'replylink'}).text
		except:
			continue
		if len(reply_link) > 3:
			if len(content_divs) > 0:
				count += 1
				print reply_link
    				Dictionary[count].append(content_divs[0].text)
				content = soupy.find('a',{'class':'replylink'}).text
				Dictionary[count].append(content)
				Dictionary[count].append(item["title"])
				Dictionary[count].append(link)
				
	def getwords(sentence):

        	#this method returns important words from a sentence as list
        	w= sentence.lower().split()

        	#get rid of all stop words
  	        #w= [x for x in w if not x in stopwords]

       		#remove all things that are 1 or 2 characters long (punctuation)
        	#w= [x for x in w if len(x)>2]

        	#get rid of duplicates by converting to set and back to list
        	#this works because sets dont contain duplicates
        	#w= list(set(w))
          	return w
    	
	for key in Dictionary.keys():
            	w = getwords(Dictionary[key][0])
		technical_glossary = ['java','c','c++','c#','sql','databases','programming','cloud computing','sharepoint','cloud','javaScript', 'linux','oracle','swing','ubuntu', 'linux','unix','geneva', 'document refining', 'requirement gathering', 'testing', 'unit testing', 'user manuals', 'induction pack','data migration','macros' ]

		for words in w:
			if words in technical_glossary:
				edit_1 = "I would like to reinforce the fact, that as mentioned in the advertisement in craigslist, I have experience in "+words+", which can be clearly seen in my resume, attached along."
				ind = w.index(words)
				new_line =[]
				for i in range (ind - 6, ind + 6):
     					try:
    						new_line.append(w[i])
						keyword = w[ind]
     		 		        except:
     		 		    		break
				new_edited_line = " ".join(new_line)
		try:
			edit_1
			new_edited_line
			newest_edited_line = "As mentioned in your advertisement and I quote '"+str(new_edited_line)+"', I have worked with "+str(keyword)+" and you can see more of my work related to "+str(keyword)+" in my resume"
			
		except:
			edit_1 = ""
			newest_edited_line = ""
			keyword = ""
		
		#sending mail from gmail script
		
		msg = MIMEMultipart() 	     
		if username == "" :             
			gmail_user = "noobjobbot@gmail.com"
			FROM = "noobjobbot@gmail.com"
			msg['From'] = "noobjobbot@gmail.com"
		else:
			gmail_user = username
			FROM = username
			msg['From'] = username
		if password == "":
			gmail_pwd = "1234567890asdfghjkl"
		else:
			gmail_pwd = password
		TO = str(Dictionary[key][1]) #must be a list
		#msg = MIMEMultipart()
		#msg['From'] = "noobjobbot@gmail.com"
		msg['To'] = str(Dictionary[key][1])
		msg['Date'] = formatdate(localtime=True)
		title_replaced = str(Dictionary[key][2]).translate(None, "[]'")
                title_replaced = title_replaced[1:]
		msg['Subject'] = "Application to craig. job ad - " + str(title_replaced) 

		body =  "230, Sandpiper Drive Davis 95616\nDate: "+formatdate(localtime=True)+"\nTo whomsoever it may concern\n\n\nEmail: rkaul5@yahoo.com\nRoma Kaul\n\n"+"				Subject: "+str(title_replaced)+"\n\nI am writing in connection with the ad you recently posted in craiglist at "+ str(Dictionary[key][3])+". I am writing to you to request you to consider me for the position of fulltime/intern/part-time/freelance work. This fulltime/internship/part-time/freelancing will help me build a strong foundation in the career I wish to pursue.\n\nI have a professional experience of 1.5 years at Genpact Headstrong Capital Markets, details of which are present in the attached resume. The projects that I have worked on in my undergrad include digital image processing that allowed to modify an image quality and a fully functional e-shopping website. I’m  currently working on a project for pfizer which involves developement of two site collections for their internal portal to be created on sharepoint technology 2010. My last project involved creation of UML for Bank of America.  Both the projects are being implemented in c#/.net.\n\n"+str(edit_1)+str(newest_edited_line)+". I believe that my expertise combined with my motivation and enthusiasm will make me a good fit for your job description. I thank you in advance for reviewing my application and would welcome the opportunity to speak to you further about this job position.\n\nThank you for your time and consideration.\n\nSincerely,\nRoma Kaul"
		
		print body
        #next section commented for testing
		
		msg.attach(MIMEText(body))
		part = MIMEBase('application', "octet-stream")
		part.set_payload( open("resume.pdf","rb").read() )
		Encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="Roma - Resume"')
		msg.attach(part)	
		server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
		server.ehlo()
		server.starttls()
		server.login(gmail_user, gmail_pwd)
		text = msg.as_string()
		server.sendmail(FROM, TO, text)
		#server.quit()
		server.close()
		print 'successfully sent the mail'
			
