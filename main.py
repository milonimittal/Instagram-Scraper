from InstaBot import InstaBot
from getpass import getpass

username=input("Enter your username: ")
password=getpass("Enter your password: ")
choice_str=input("Input 1 for account scraping, 2 for hashtag scraping: ")
choice=int(choice_str)

if choice==1:
	target_account=input("Enter name of the account you want to scrape: ")
	myBot=InstaBot(username, password)
	myBot.scrape_account(target_account)
elif choice==2:
	target_hashtag=input("Enter the hashtag you want to scrape: ")
	myBot=InstaBot(username, password)
	myBot.scrape_hashtag(target_hashtag)