'''
Author: Jordan Ott
Date: February 20th, 2017
Description: This module scrapes the top gainers and losers from the New York stock market over the past
150 business days and outputs the data to csv files.
Requirements: 
	pandas
	selenium
	firefox
'''
import time
import pandas as pd
# BDay is business day, not birthday...
from pandas.tseries.offsets import BDay
from selenium import webdriver

# URLs for gainers and decliners using the wall street journal
gainers   = ["http://online.wsj.com/mdc/public/page/2_3021-gainnyse-gainer-",".html?mod=mdc_pastcalendar"]
decliners = ["http://online.wsj.com/mdc/public/page/2_3021-losenyse-loser-",".html?mod=mdc_pastcalendar"]

def build_past_url(days_since_current,stock_movement):
	today = pd.datetime.today()
	past_date = today - BDay(days_since_current)
	date = past_date.strftime('%Y%m%d')
	url = stock_movement[0] + date + stock_movement[1]
	return url,date

def scrape_table(data_file,url,date):
	driver.get(url)
	tbody = driver.find_elements_by_css_selector('tbody')
	table_body = tbody[5]
	if len(tbody) == 10:
		table_body = tbody[6]
	table_rows = table_body.find_elements_by_css_selector("tr")
	for index in range(1,len(table_rows)):
		individual_row = table_rows[index].find_elements_by_css_selector("td")
		company_name = individual_row[1].find_elements_by_css_selector('a')[0].text
		company_name = company_name[company_name.find("(")+1:company_name.find(")")]
		price = individual_row[2].text
		dollar_change = individual_row[3].text
		percent_change = individual_row[4].text
		line = date +','+ company_name +','+ price +','+ dollar_change +','+ percent_change +'\n'
		
		data_file.write(line)
	
# 150 for last 150 business days
'''
for num in range(1,150):
	gainers_url,date = build_past_url(num,gainers)
	decliners_url,date = build_past_url(num,decliners)
	scrape_table(gainers_file,gainers_url,date)
	scrape_table(decliners_file,decliners_url,date)
	print(num)
'''
def get_daily():
	driver = webdriver.Firefox()

	gainers_file = open("gainers.csv",'w')
	decliners_file = open("decliners.csv",'w')
	
	gainers_url = "http://online.wsj.com/mdc/public/page/2_3021-gainnyse-gainer.html"
	decliners_url = "http://online.wsj.com/mdc/public/page/2_3021-losenyse-loser.html"
	date = pd.datetime.today().strftime('%Y%m%d')

	scrape_table(gainers_file,gainers_url,date)
	scrape_table(decliners_file,decliners_url,date)

	gainers_file.close()
	decliners_file.close()
	driver.quit()
