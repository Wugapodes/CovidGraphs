import pandas as pd
import pycountry
import subprocess

# Set data URLs
confirmedURL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
deathsURL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'

# Update local files
pd.read_csv(confirmedURL).to_csv('/home/cj/Desktop/Projects/Wikipedia/CovidGraphs/data/csse_time_series_19-covid-Confirmed.csv', index=False)
pd.read_csv(deathsURL).to_csv('/home/cj/Desktop/Projects/Wikipedia/CovidGraphs/data/csse_time_series_19-covid-Deaths.csv', index=False)

# Run r script to clean it up
subprocess.call('./dataIngest.R')

# Confirmed
confirmedRaw = pd.read_csv('data/csse_Confirmed_by_country.csv')
dateArray = []
for key in confirmedRaw.columns:
	if key == 'Country':
		dateArray.append(key)
		continue
	dateFormatted = '/'.join([x.zfill(2) for x in key.split('/')])
	dateArray.append(dateFormatted)

confirmedRaw.columns = dateArray

countryCodes = {}
for country in set(confirmedRaw["Country"]):
	try:
		result = pycountry.countries.search_fuzzy(country)
	except LookupError as e:
		if country == 'Korea, South':
			countryCodes[country] = 'KOR'
		elif country == 'Taiwan*':
			countryCodes[country] = 'TWN'
		elif country == 'Gambia, The':
			countryCodes[country] = 'GMB'
		else:
			countryCodes[country] = 'XXX'
		continue
	countryCodes[country]=result[0].alpha_3

idArray = [countryCodes[x] for x in confirmedRaw["Country"]]
confirmedRaw['id'] = idArray

confirmedRaw.to_csv('data/csse_Confirmed_by_country_zero_padded.csv',index=False)

# New cases per day
cols = [x for x in confirmedRaw.columns if x not in ['Country', 'id'] ]
confirmedDaily = pd.DataFrame({'Country': confirmedRaw['Country'], 'id': confirmedRaw['id']})
for i in range(1,len(cols)):
	newDay = cols[i]
	oldDay = cols[i-1]
	confirmedDaily[newDay] = confirmedRaw[newDay] - confirmedRaw[oldDay]

confirmedDaily.to_csv('data/csse_Daily_New_Confirmed_by_country_zero_padded.csv',index=False)

# Global totals by date

globalConfirmedRaw = pd.read_csv('data/csse_global_confirmed_cases_by_date.csv')
dateArray = []
for date in globalConfirmedRaw["date"]:
	dateFormatted = '/'.join([x.zfill(2) for x in date.split('/')])
	dateArray.append(dateFormatted)

globalConfirmedRaw["date"] = dateArray

globalConfirmedRaw.to_csv('data/csse_global_Confirmed_by_country_zero_padded.csv',index=False)

# Deaths
deathsRaw = pd.read_csv('data/csse_deaths_by_country.csv')
dateArray = []
for key in deathsRaw.columns:
	if key == 'Country':
		dateArray.append(key)
		continue
	dateFormatted = '/'.join([x.zfill(2) for x in key.split('/')])
	dateArray.append(dateFormatted)

deathsRaw.columns = dateArray

countryCodes = {}
for country in set(deathsRaw["Country"]):
	try:
		result = pycountry.countries.search_fuzzy(country)
	except LookupError as e:
		if country == 'Korea, South':
			countryCodes[country] = 'KOR'
		elif country == 'Taiwan*':
			countryCodes[country] = 'TWN'
		elif country == 'Gambia, The':
			countryCodes[country] = 'GMB'
		else:
			countryCodes[country] = 'XXX'
		continue
	countryCodes[country]=result[0].alpha_3

idArray = [countryCodes[x] for x in deathsRaw["Country"]]
deathsRaw['id'] = idArray

deathsRaw.to_csv('data/csse_deaths_by_country_zero_padded.csv',index=False)

globaldeathsRaw = pd.read_csv('data/csse_global_deaths_by_date.csv')
dateArray = []
for date in globaldeathsRaw["date"]:
	dateFormatted = '/'.join([x.zfill(2) for x in date.split('/')])
	dateArray.append(dateFormatted)

globaldeathsRaw["date"] = dateArray

globaldeathsRaw.to_csv('data/csse_global_deaths_by_date_zero_padded.csv',index=False)

# New deaths per day
cols = [x for x in deathsRaw.columns if x not in ['Country', 'id'] ]
deathsDaily = pd.DataFrame({'Country': deathsRaw['Country'], 'id': deathsRaw['id']})
for i in range(1,len(cols)):
	newDay = cols[i]
	oldDay = cols[i-1]
	deathsDaily[newDay] = deathsRaw[newDay] - deathsRaw[oldDay]

deathsDaily.to_csv('data/csse_Daily_New_deaths_by_country_zero_padded.csv',index=False)

dateArray = []
for date in globaldeathsRaw["date"]:
	dateFormatted = '/'.join([x.zfill(2) for x in date.split('/')])
	dateArray.append(dateFormatted)

globaldeathsRaw["date"] = dateArray

globaldeathsRaw.to_csv('data/csse_global_deaths_by_date_zero_padded.csv',index=False)
