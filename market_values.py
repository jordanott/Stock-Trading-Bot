from yahoo_finance import Share
from datetime import datetime
from pandas.tseries.offsets import BDay
import sqlite3
from pprint import pprint

conn = sqlite3.connect('stock_data.db')
cur = conn.cursor()

def get_share_value(company_name,date):
	start_date = datetime(int(date[0:4]),int(date[4:6]),int(date[6:]))
	end_date = start_date + BDay(5)

	start_date = start_date.strftime('%Y-%m-%d')
	end_date = end_date.strftime('%Y-%m-%d')

	company = Share(company_name)
	company_data = company.get_historical(start_date,end_date)
	#pprint(company_data)
	company_data = company_data[:-1]
	return_data = []
	for day in reversed(company_data):
		return_data.append(day['Close'])
	return return_data

def insert_to_db(file_name,table):
	data_file = open(file_name,'r')
	for line in data_file:
		data = line.split(',')
		
		statement1 = "insert into {table}(date,company,price,dollar_change,percent_change" 
		statement2 = ") values(\'{date}\',\'{company}\',\'{price}\',\'{dollar_change}\',\'{percent_change}\'"
		statement1 = statement1.format(table=table)
		statement2 = statement2.format(date=data[0],company=data[1],price=data[2],dollar_change=data[3],percent_change=data[4])
		
		statement = create_statement(statement1,statement2,get_share_value(data[1],data[0]))
		print(statement)
		cur.execute(statement)
		conn.commit()

def create_statement(statement1,statement2,days_data):
	if len(days_data) == 5:
		statement = statement1 + "day1,day2,day3,day4,day5" + statement2
		days = ",\'{day1}\',\'{day2}\',\'{day3}\',\'{day4}\',\'{day5}\');".format(day1=days_data[0],day2=days_data[1],day3=days_data[2],day4=days_data[3],day5=days_data[4])
	elif len(days_data) == 4:
		statement = statement1 + "day1,day2,day3,day4" + statement2
		days = ",\'{day1}\',\'{day2}\',\'{day3}\',\'{day4}\');".format(day1=days_data[0],day2=days_data[1],day3=days_data[2],day4=days_data[3],day5=days_data[4])
	elif len(days_data) == 3:
		statement = statement1 + "day1,day2,day3" + statement2
		days = ",\'{day1}\',\'{day2}\',\'{day3}\');".format(day1=days_data[0],day2=days_data[1],day3=days_data[2])
	elif len(days_data) == 2:
		statement = statement1 + "day1,day2" + statement2
		days = ",\'{day1}\',\'{day2}\');".format(day1=days_data[0],day2=days_data[1])
	elif len(days_data) == 1:
		statement = statement1 + "day1" + statement2
		days = ",\'{day1}\');".format(day1=days_data[0])
	elif len(days_data) == 0:
		statement = statement1 + statement2
		days = ");"
	return_statement = statement + days

	return return_statement.replace('\n','')

def update():
	pass

insert_to_db('decliners.csv',"decliners")

conn.close()