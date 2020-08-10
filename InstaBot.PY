from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import os
import requests
import shutil

class InstaBot:
	def __init__(self, username, password):
		self.username=username
		self.password=password
		self.main_url = 'https://www.instagram.com'
		self.driver=webdriver.Chrome()
		self.driver.get("https://instagram.com")
		sleep(2)
		self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(self.username)
		self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(self.password)
		self.driver.find_element_by_xpath("//button[@type=\"submit\"]").click()
		sleep(2)		
		self.driver.find_element_by_xpath("//button[contains(text(),'Not Now')]").click()
		sleep(2)
		self.driver.find_element_by_xpath("//button[contains(text(),'Not Now')]").click()
		sleep(2)

	def scrape_account(self, target_account):
		self.target_account=target_account
		target_profile_url  = self.main_url + '/' + self.target_account
		self.driver.get(target_profile_url) 
		num_posts=str(self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span').text).replace(',', '') 
		print("Number of posts: "+str(num_posts))
		num_followers=str(self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').text).replace(',', '')
		print("Followers: "+ str(num_followers))
		num_following=str(self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text).replace(',', '')
		print("Following: "+str(num_following))
		self.num_posts=12
		image_list = []
		soup = BeautifulSoup(self.driver.page_source, 'lxml')
		all_images = soup.find_all('img', attrs = {'class': 'FFVAD'}) 
		for img in all_images:
			if img not in image_list:
				image_list.append(img)
		if self.num_posts > 12:
			no_of_scrolls = round(self.num_posts/12) + 6
			print('Loading all the posts...')
			for __ in range(no_of_scrolls):
				self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
				sleep(2)
				soup = BeautifulSoup(self.driver.page_source, 'lxml')
				all_images = soup.find_all('img')
				for img in all_images:
					if img not in image_list:
						image_list.append(img)
		parent_dir = "scraped_data"
		self.path = os.path.join(parent_dir, self.target_account)
		os.mkdir(self.path) 
		no_of_images = len(image_list)
		for index, img in enumerate(image_list, start = 1):
			filename = 'image_' + str(index) + '.jpg'
			image_path = os.path.join(self.path, filename)
			link = img.get('src')
			response = requests.get(link, stream = True)
			print('Downloading image: {0}/{1}'.format(index, no_of_images))
			try:
				with open(image_path, 'wb') as file:
					shutil.copyfileobj(response.raw, file)
			except Exception as e:
				print(e)
				print('Couldn\'t download image {0}.'.format(index))
				print('Link for image {0} ---> {1}'.format(index, link))
		print('Done!')

	def scrape_hashtag(self,target_hashtag):
		self.target_hashtag=target_hashtag
		target_profile_url  = self.main_url + '/explore/tags/' + self.target_hashtag
		self.driver.get(target_profile_url)	
		self.num_posts=12
		image_list = []
		soup = BeautifulSoup(self.driver.page_source, 'lxml')
		all_images = soup.find_all('img', attrs = {'class': 'FFVAD'}) 
		for img in all_images:
			if img not in image_list:
				image_list.append(img)
		if self.num_posts > 12:
			no_of_scrolls = round(self.num_posts/12) + 6
			print('Loading all the posts...')
			for __ in range(no_of_scrolls):
				self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
				sleep(2)
				soup = BeautifulSoup(self.driver.page_source, 'lxml')
				all_images = soup.find_all('img')
				for img in all_images:
					if img not in image_list:
						image_list.append(img)
		parent_dir = "scraped_data"
		self.path = os.path.join(parent_dir, self.target_hashtag)
		os.mkdir(self.path) 
		no_of_images = len(image_list)
		for index, img in enumerate(image_list, start = 1):
			filename = 'image_' + str(index) + '.jpg'
			image_path = os.path.join(self.path, filename)
			link = img.get('src')
			response = requests.get(link, stream = True)
			print('Downloading image: {0}/{1}'.format(index, no_of_images))
			try:
				with open(image_path, 'wb') as file:
					shutil.copyfileobj(response.raw, file)
			except Exception as e:
				print(e)
				print('Couldn\'t download image {0}.'.format(index))
				print('Link for image {0} ---> {1}'.format(index, link))
		print('Done!')	
