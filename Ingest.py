import pandas as pd
import pycountry
import subprocess
import pywikibot

live = 1
site = pywikibot.Site()
dataToPageCorrespondence = {
	'data/csse_Confirmed_by_country_zero_padded.csv': 'Template:Interactive COVID-19 maps/data/Confirmed covid cases-csv',
	'data/csse_Daily_New_Confirmed_by_country_zero_padded.csv': 'Template:Interactive COVID-19 maps/data/Daily confirmed covid cases-csv',
	'data/csse_deaths_by_country_zero_padded.csv': 'Template:Interactive COVID-19 maps/data/Deaths by country-csv',
	'data/csse_Daily_New_deaths_by_country_zero_padded.csv': 'Template:Interactive COVID-19 maps/data/Daily deaths by country-csv',
	'data/csse_global_Confirmed_by_country_zero_padded.csv': 'Template:Interactive COVID-19 maps/data/global Confirmed covid cases by date-csv',
	'data/csse_global_deaths_by_date_zero_padded.csv': 'Template:Interactive COVID-19 maps/data/Cumulative deaths by date-csv'
}

def writeDataPage( site, dataFileName, pageName ):
	prefix = '/data/project/wugbot/CovidGraphs/'
	with open(prefix+dataFileName,'r') as f:
		data = f.read()
	page = pywikibot.Page(site, pageName)
	page.text = data
	page.save('Updating COVID-19 data from CSSEGISandData/COVID-19 repository.')

def formatDates( columns ):
	dateArray = []
	for key in columns:
		if key == 'Country':
			dateArray.append(key)
			continue
		dateFormatted = zeroPad( key )
		dateArray.append(dateFormatted)
	return dateArray

def formatShortDates( columns ):
	dateArray = []
	for date in columns:
		dateFormatted = zeroPad( date )
		dateArray.append(dateFormatted)
	return dateArray

def zeroPad( date ):
	return '/'.join([x.lstrip('X').zfill(2) for x in date.split('.')])

def getCountryCodes(data):
	countryCodes = {}
	for country in set(data["Country"]):
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
	idArray = [countryCodes[x] for x in data["Country"]]
	return idArray

def perDiem( rawData ):
	cols = [x for x in rawData.columns if x not in ['Country', 'id'] ]
	daily = pd.DataFrame({'Country': rawData['Country'], 'id': rawData['id']})
	for i in range(1,len(cols)):
		newDay = cols[i]
		oldDay = cols[i-1]
		daily[newDay] = rawData[newDay] - rawData[oldDay]
	return daily

# Set data URLs
confirmedURL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
deathsURL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'

# Update local files
pd.read_csv(confirmedURL).to_csv('/data/project/wugbot/CovidGraphs/data/csse_time_series_19-covid-Confirmed.csv', index=False)
pd.read_csv(deathsURL).to_csv('/data/project/wugbot/CovidGraphs/data/csse_time_series_19-covid-Deaths.csv', index=False)

# Run r script to clean it up
subprocess.call('/data/project/wugbot/CovidGraphs/dataIngest.R')

# Confirmed
confirmedRaw = pd.read_csv('/data/project/wugbot/CovidGraphs/data/csse_Confirmed_by_country.csv')

confirmedRaw.columns = formatDates(confirmedRaw.columns)

confirmedRaw['id'] = getCountryCodes(confirmedRaw)

confirmedRaw.to_csv('/data/project/wugbot/CovidGraphs/data/csse_Confirmed_by_country_zero_padded.csv',index=False)

# New cases per day
confirmedDaily = perDiem(confirmedRaw)

confirmedDaily.to_csv('/data/project/wugbot/CovidGraphs/data/csse_Daily_New_Confirmed_by_country_zero_padded.csv',index=False)

# Global totals by date

globalConfirmedRaw = pd.read_csv('/data/project/wugbot/CovidGraphs/data/csse_global_confirmed_cases_by_date.csv')

globalConfirmedRaw["date"] = formatShortDates( globalConfirmedRaw["date"] )

globalConfirmedRaw.to_csv('/data/project/wugbot/CovidGraphs/data/csse_global_Confirmed_by_country_zero_padded.csv',index=False)

# Deaths
deathsRaw = pd.read_csv('/data/project/wugbot/CovidGraphs/data/csse_deaths_by_country.csv')

deathsRaw.columns = formatDates(deathsRaw.columns)

deathsRaw['id'] = getCountryCodes(deathsRaw)

deathsRaw.to_csv('/data/project/wugbot/CovidGraphs/data/csse_deaths_by_country_zero_padded.csv',index=False)

globaldeathsRaw = pd.read_csv('/data/project/wugbot/CovidGraphs/data/csse_global_deaths_by_date.csv')


globaldeathsRaw["date"] = formatShortDates( globaldeathsRaw["date"] )

globaldeathsRaw.to_csv('/data/project/wugbot/CovidGraphs/data/csse_global_deaths_by_date_zero_padded.csv',index=False)

# New deaths per day
deathsDaily = perDiem( deathsRaw )

deathsDaily.to_csv('/data/project/wugbot/CovidGraphs/data/csse_Daily_New_deaths_by_country_zero_padded.csv',index=False)

if live == 1:
	for k,v in dataToPageCorrespondence.items():
		writeDataPage( site, k, v )
else:
	print('Not writing to wiki')
