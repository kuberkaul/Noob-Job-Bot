NoobJobBot
==========
This project is an attempt to create a smart program that recurses through scraped data from the jobs(fulltime/internship) section of craiglist : http://newyork.craigslist.org/sof/. Craiglist is scrapped using the open source project http://scrapy.org/ which is a rapid web crawler built in python. Once we scrap data using scrappy our program goes through the data noting down the email address, keywords from each job oppurtunity using urllib and thus 'smartly' editing the cover letter and resume as per the requirement through the keywords using our own strategy . It then automates the process of applying to the jobs by sending emails to the respective email id's with that cover letter, resume through a mailing service. The program is written in Python

Purpose : The main purpose of this project is to automate the process of job application with highly personalized job application thus making sure it is not perceived to be a bot/spam mail. Our project is thus aptly called NoobJobBot.

Evaluation : We are done with version 1 on the software.In time we would be putting up our user evaluation for this product, rating how well it works in its category.

Instruction for use : Follow the steps to run the project -

1. Download the project on your local file system .
2. Install scrapy for your OS using the site. 
3. Install beautiful soup on your system. 
4. plug in your email address and password at line 104 and 105. Similarly change the other details as per your wish.
5. Once done, open the path to the project in console and type- scrapy crawl craig

- We will soon be releasing version 2 with updated project.


In Brief : We automate the process of applying for jobs(Fulltime/internships), while still keeping each application individual. 
