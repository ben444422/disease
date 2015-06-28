"""
Given a list of icdcodes in a text file (piped in via stdin), extracts both the 
name of the disease and the associated symptoms from the diseasedatabase website

Usage: python crawler.py < icdcodes.txt
"""

from bs4 import BeautifulSoup
import requests
import sys
import time 

count = 0
for line in sys.stdin:
	code = line.strip()

	url = "http://www.diseasesdatabase.com/code_translate.asp"
	url2 = "http://www.diseasesdatabase.com/"

	headers = {'user-agent': 'diseasecrawler2/0.0.1'}
	params = {"strSAB": "ICD10", "strCODE": code}

	try:
		r = requests.get(url, params=params, headers=headers)

		soup = BeautifulSoup(r.content)

		diseaselink = None
		for link in soup.find_all('a', href=True):
			if "htm" in link['href']:
				diseaselink = link['href']
				break

		if diseaselink is None:
			continue

		r = requests.get(url2 + diseaselink,headers=headers)
		soup = BeautifulSoup(r.content)

		diseasename = soup.title.text
		diseaselink = None
		for link in soup.find_all('a', href=True):
			if "UserChoice" in link['href']:
				diseaselink = link['href']
				break

		if diseaselink is None:
			continue


		r = requests.get(url2 + diseaselink, headers=headers)
		soup = BeautifulSoup(r.content)

		head = None
		for dt in soup.find_all('dt'):
			if "Symptoms" in dt.contents[0]:
				head = dt
				break

		if head is None:
			continue	

		symptoms = []


		for i in range(11):
			if head is not None:
				text = head.find('strong')
				if text is not None:
					if type(text) is not int:
						symptoms.append(text.text)

			head = head.nextSibling


		head.nextSibling
		if head is not None:
			text = head.find('strong')
			if text is not None:
				if type(text) is not int:
					symptoms.append(text.text)

		print "==== Processing Disease " + count + " ====="
		print diseasename
		print "Symptoms: "
		print symptoms
		count += 1
	except:
		print "Error processing disease: " + code
		pass
	# add a delay of 7 seconds between disease crawl jobs
	time.sleep(7)




