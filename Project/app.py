import pyodbc
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import Flask, render_template

connection = pyodbc.connect("DSN=BDAT_1000", autocommit=True)
# connection=pyodbc.connect('DRIVER={ODBC DRIVER 17 for SQL Server};'
# 'Server=LAPTOP-NCE4R91B;'
# 'Database=BDAT_1000;'
# 'Trusted_Connection=Yes;')
query= 'select count(1) as Count, [Geo Summary] from dbo.Airport_Stats group by [Geo Summary]'
TM = pd.read_sql(query, connection)

# Extracting Query from SSMS for Chart #1
cursor =connection.cursor()
cursor.execute('select [GEO Region] as Region,sum(Passenger_Count) as Count  from dbo.Airport_Stats where year=2006 group by [GEO Region]')

tuples=cursor.fetchall()
cursor.close()

# Convert Function - List of Tuples to Dictionary
def Convert(tup, di): 
    di = dict(tup) 
    return di 

# Prepare Dictionary using Convert Function
print(tuples)
dictionary = {} 
dic1=Convert(tuples, dictionary)
print (Convert(tuples, dictionary)) 
#Add Key Value Pair Title
dic2={'Region':'Count'}
dic2.update(dic1)
print(dic2)

# Extracting Query from SSMS for Chart #3
cursor2 =connection.cursor()
cursor2.execute('select [Activity Type Code],count(1) as Flight_Status from dbo.Airport_Stats group by [Activity Type Code]')
tuples2=cursor2.fetchall()
cursor2.close()

# Prepare Dictionary using Convert Function
print(tuples2)
dictionary3 = {} 
dic3=Convert(tuples2, dictionary3)
print (Convert(tuples2, dictionary3)) 
#Add Key Value Pair Title
dic4={'Activity Code':'Flight Status'}
dic4.update(dic3)
print(dic3)

# Extracting Query from SSMS for Chart #2
cursor1 =connection.cursor()
cursor1.execute('select Year, Sum(Passenger_Count) as Count from dbo.Airport_Stats group by Year order by Year')

#Store data into JSON
C2=[]
G2=[]
for row in cursor1:
	print(row)
	C2.append(row.Year)
	G2.append(row.Count)


app = Flask(__name__)

@app.route('/')
# @app.route('/index3.html')
# def index3(chartID = 'chart_ID', chart_type = 'bar', chart_height = 350):
# 	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
# 	for i in range(0,5):
# 		series = [{"name": 'Regions', "data": C1}]
# 	title = {"text": 'My Title'}
# 	for i in range(0,5):
# 		xAxis = {"categories": G1}
# 	yAxis = {"title": {"text": 'Passenger Count'}}
	
# 	return render_template('index3.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)


# Line Chart Function
@app.route('/#LineChart')
def index(chartID = 'chart_ID', chart_type = 'line', chart_height = 400):
	
	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
	for i in range(0,5):
		series = [{"name": 'Passenger Count', "data": G2}]
	title= {"text": 'Trend of Passenger traveling to SF'}
	for i in range(0,5):
		xAxis= {"title":{"text":'Year'},"categories": C2}
	yAxis = {"title": {"text": 'Passenger Count (in Millions)'}}
	return render_template('index.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)

#Pie Chart Function
@app.route('/index2.html')
def google_pie_chart():
	dic4={'Activity Code':'Flight Status'}
	dic4.update(dic3)
	# dic3={ 'Region': 'Passenger Count','Asia': 1955732.0, 'Australia / Oceania': 164991.0, 'Canada': 589467.0, 'Central America': 61994.0, 'Europe': 1147195.0, 'Mexico': 305087.0, 'US': 12997567.0}
	return render_template('index2.html', data=dic4)

# Bar Chart Function
@app.route('/index3.html')
def google_bar_chart():

	# dic1={ 'Region': 'Passenger Count','Asia': 1955732.0, 'Australia / Oceania': 164991.0, 'Canada': 589467.0, 'Central America': 61994.0, 'Europe': 1147195.0, 'Mexico': 305087.0, 'US': 12997567.0}
	dic2={'Region':'Count'}
	dic2.update(dic1)
	return render_template('index3.html', data=dic2)

if __name__ == "__main__":
	app.run(debug=True)