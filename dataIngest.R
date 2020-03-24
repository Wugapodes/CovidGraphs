#!/data/project/wugbot/local/bin/Rscript
library(dplyr)
library(tidyr)

getwd()
confirmed.raw = read.csv('/data/project/wugbot/CovidGraphs/data/csse_time_series_19-covid-Confirmed.csv')

confirmed.consolidated = confirmed.raw %>%
  select(-Lat,-Long,-`Province.State`)%>%
  rename(Country=`Country.Region`)%>%
  group_by(`Country`)%>%
  summarise_all(sum)

confirmed.dates = gather(confirmed.consolidated,"date","cases",-Country)
dates = unique(confirmed.dates$date)
confirmed.global = confirmed.dates %>%
  select(-Country)%>%
  group_by(date)%>%
  summarize_all(sum)

write.csv(confirmed.global, '/data/project/wugbot/CovidGraphs/data/csse_global_confirmed_cases_by_date.csv')
write.csv(confirmed.consolidated,'/data/project/wugbot/CovidGraphs/data/csse_Confirmed_by_country.csv')

deaths.raw = read.csv('/data/project/wugbot/CovidGraphs/data/csse_time_series_19-covid-Deaths.csv')

deaths.consolidated = deaths.raw %>%
  select(-Lat,-Long,-`Province.State`)%>%
  rename(Country=`Country.Region`)%>%
  group_by(`Country`)%>%
  summarise_all(sum)

deaths.dates = gather(deaths.consolidated,"date","cases",-Country)
dates = unique(deaths.dates$date)
deaths.global = deaths.dates %>%
  select(-Country)%>%
  group_by(date)%>%
  summarize_all(sum)

write.csv(deaths.global, '/data/project/wugbot/CovidGraphs/data/csse_global_deaths_by_date.csv')
write.csv(deaths.consolidated,'/data/project/wugbot/CovidGraphs/data/csse_deaths_by_country.csv')
