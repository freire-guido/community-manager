from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time
import numpy as np
import pandas as pd
import scipy.stats

followed = pd.read_csv("C:/Users/freir/OneDrive/Documentos/Python/yuhh").set_index('username')

class InstagramBot:

	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.driver = webdriver.Chrome("C:/Users/freir/OneDrive/Documentos/Python/chromedriver.exe")

	def login(self):
		driver = self.driver
		driver.get("https://www.instagram.com/")
		time.sleep(2)
		login_username = driver.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input")
		login_username.clear()
		login_username.send_keys(self.username)
		login_password = driver.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input")
		login_password.clear()
		login_password.send_keys(self.password)
		login_enter = driver.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div[1]/div/form/div[4]/button/div")
		login_enter.click()
		time.sleep(5)

	def parsePosts(self):
		driver = self.driver
		value = 0
		for name in followed.index:
			print(name)
			print((followed.private[name]))
			if str(followed.private[name]) == 'nan':
				driver.get('https://instagram.com/' + name + '/')
				time.sleep(1)
				try:
					driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[1]/div/h2')
					value = 1
				except NoSuchElementException:
					try:
						driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[2]')
						value = 0
					except NoSuchElementException:
						value = np.nan			
				print(value)
				followed.private[name] = value

parser = InstagramBot('albefarra43', 'guidocapo911')
parser.login()
parser.parsePosts()
followed.to_csv('yuhh')