from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from selenium import webdriver
import pandas as pd
import configparser
import numpy as np
import time

total_liked = 0
total_followed = 0
reset_count = 1

class InstagramBot:

	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.driver = webdriver.Chrome("chromedriver.exe")

	def closeBrowser(self):
		self.driver.close()

	def login(self):
		driver = self.driver
		driver.get("https://www.instagram.com/")
		time.sleep(2)
		login_username = driver.find_element_by_xpath("//*[@id='loginForm']/div/div[1]/div/label/input")
		login_username.clear()
		login_username.send_keys(self.username)
		login_password = driver.find_element_by_xpath("//*[@id='loginForm']/div/div[2]/div/label/input")
		login_password.clear()
		login_password.send_keys(self.password)
		login_enter = driver.find_element_by_xpath("//*[@id='loginForm']/div/div[3]/button")
		login_enter.click()
		with open('data/followed' + self.username.replace('.', '+'), 'r+') as file:
			if not file.read(1):
				file.write('username,following,followers,posts,private')
		with open('data/followers' + rollocriollo.username.replace('.', '+'), 'a+') as file:
			pass
		time.sleep(5)

	def suggestFollower(self):
		driver = self.driver
		global reset_count

		driver.get("https://www.instagram.com/explore/people/suggested/")
		time.sleep(4)
		self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[2]/div/div/div[{}]/div[2]/div[1]/div/span/a'.format(reset_count)).click()
		time.sleep(3)

	def evaluateFollower(self):
		driver = self.driver
		global prediction
		global following
		global followers
		global user
		global posts
		global private
		try:
			following = int(driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/span/span').text.replace(".", "").replace(",", "").replace("mm", "00000").replace('k', ''))
		except NoSuchElementException:
			try:
				following =  int(driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text.replace(".", "").replace(",", "").replace("mm", "00000").replace('k', ''))
			except:
				following = np.nan
		try:
			followers = int(driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').text.replace(".", "").replace(",", "").replace("mm", "00000").replace('k', ''))
		except NoSuchElementException:
			try:
				followers =  int(driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/span/span').text.replace(".", "").replace(",", "").replace("mm", "00000").replace('k', ''))
			except:
				followers = np.nan
		try:
			posts = int(driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span').text.replace(".", "").replace(",", "").replace("mm", "00000").replace('k', ''))
		except ValueError:
			posts = np.nan
		try:
			user = str(driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/h2').text)
		except NoSuchElementException:
			user = str(driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/h1').text)
		try:
			driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[1]/div/h2')
			private = 1
		except NoSuchElementException:
			try:
				driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[2]')
				private = 0
			except NoSuchElementException:
				private = np.nan			
		#REMOVE prediction = pipeline.predict([[following, followers, posts, private]])

	def patFollower(self):
		driver = self.driver
		global total_liked
		global total_followed
		try:
			driver.find_element_by_xpath("//*[text()='Seguir']").click()
		except NoSuchElementException:
			driver.find_element_by_xpath("//*[text()='Seguir también']").click()
		print('Followed')
		total_followed += 1
		element = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[2]')
		driver.execute_script("arguments[0].scrollIntoView();", element)
		driver.find_element_by_xpath('//div[@class="eLAPa"]').click()
		time.sleep(4)
		for i in range(posts):
			driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button').click()
			try:
				driver.find_element_by_xpath('//*[text()="Siguiente"]').click()
			except NoSuchElementException:
				pass
			print('Liked {} post(s)'.format(i + 1))
			total_liked += 1
			time.sleep(2)
			if i > 4:
				break

	def updateModel(self):
		global pipeline
		global rude
		followed = pd.read_csv('data/followed' + self.username.replace('.', '+')).set_index('username')
		fw = []
		with open('data/followers' + rollocriollo.username.replace('.', '+'), 'r') as file:
			for line in file:
				fw.append(line.strip())
		#Update "followers" if someone follows or unfollows me
		self.driver.get('https://instagram.com/' + self.username + '/')
		time.sleep(1)
		try:
			followers_mine = int(self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').text.replace(".", "").replace(",", "").replace("mm", "00000").replace('k', ''))
		except NoSuchElementException:
			followers_mine =  int(self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/span/span').text.replace(".", "").replace(",", "").replace("mm", "00000").replace('k', ''))
		print('Loaded', len(fw), 'followers from last session')
		print('Found', followers_mine, 'followers')
		if len(fw) != followers_mine:
			print('Updating followers...')
			self.driver.find_element_by_xpath('//*[text()=" seguidores"]').click()
			time.sleep(2)
			scroll_box = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
			last_ht, ht = 0, 1
			while last_ht != ht:
				last_ht = ht
				ht = self.driver.execute_script("""
				                                arguments[0].scrollTo(0, arguments[0].scrollHeight);
				                                return arguments[0].scrollHeight;""", scroll_box)
				time.sleep(1)
			fw = [name.text for name in scroll_box.find_elements_by_xpath('//a[@class="FPmhX notranslate  _0imsa "]')]
			#FOR DYNAMIC FOLLOWER LOADING, CHANGE LAST LINE TO FW_COUNT AND UNCOMMENT:
			#with open('followers' + rollocriollo.username.replace('.', '+'), 'a+') as file:
			#	for name in fw_count:
			#		if str(name) not in fw:
			#			file.write(name + '\n')
			#			fw.append(name)
			#		else:
			#			continue
			with open('data/followers' + rollocriollo.username.replace('.', '+'), 'w') as file:
				for name in fw:
					file.write(name + '\n')
		print(len(fw), 'followers found')
		#Create the "Random Forest Classifier" model
		print('Updating regression model...')
		followed['followed_back'] = [0 if name not in fw else 1 for name in followed.index]
		rude = [name for name in followed.index if followed.loc[name, 'followed_back'] == 0]
		pipeline = Pipeline(steps=[('preprocessor', followed.dropna(inplace=True)), ('model', RandomForestClassifier())])
		if len(followed.index) > 5:
			X = followed[['following', 'followers', 'posts', 'private']]
			y = followed.followed_back
			pipeline.fit(X, y)

	def unfollow(self, username):
		driver = self.driver
		driver.get('https://instagram.com/' + username + '/')
		time.sleep(2)
		try:
			driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div[2]/span/span[1]/button').click()
			time.sleep(1)
			driver.find_element_by_xpath('//*[text()="Dejar de seguir"]').click()
			print(username, 'unfollowed')
		except NoSuchElementException:
			print(username, 'not following')

if __name__ == "__main__":
	config_type = 'run'
	config = configparser.ConfigParser()
	config.read('config.ini')
	userName = config.get(config_type, 'user')
	passWord = config.get(config_type, 'pass')
rollocriollo = InstagramBot(userName, passWord)
rollocriollo.login()
rollocriollo.updateModel()
for username in rude:
	print('Looking for rude people...')
	rollocriollo.unfollow(username)
print('Looking for potential followers...')
while total_liked + total_followed < 360:
	rollocriollo.suggestFollower()
	rollocriollo.evaluateFollower()
	reset_count += 1
	print(user, 'has\n', 'following:', following, 'followers:', followers, 'posts:', posts, '\nreset_count:', reset_count)
	if (following / followers) > 0.6 and posts > 2 and private == 0:
		rollocriollo.patFollower()
		with open('data/followed' + rollocriollo.username.replace('.', '+'), 'a') as file:
						file.write(user + ',' + str(following) + ',' + str(followers) + ',' + str(posts) + ',' + str(private) + '\n')
		reset_count -= 1
	if reset_count > 10:
		reset_count = 1
else:
	print('Session finished with', total_followed,'followed and', total_liked, 'liked')