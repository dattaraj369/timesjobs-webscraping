import requests
from bs4 import BeautifulSoup
import pandas as pd

print("Type a skill you don't have")
unfamiliar_skill = input('>')
print(f"Filtering out {unfamiliar_skill}")

html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text
soup = BeautifulSoup(html_text, 'lxml')

column_headers = ['Company','Skills','Posted on','More Info']
dataframe = pd.DataFrame(columns = column_headers)

jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

for index, job in enumerate(jobs):
    i=0
    skills = job.find('span', class_='srp-skills').text.replace(' ', '')
    
    if unfamiliar_skill not in skills:
        for i in (1,5):
            date = job.find('span', class_='sim-posted').span.text
            company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ', '')
            skills = job.find('span', class_='srp-skills').text.replace(' ', '')
            more_info = job.header.h2.a['href']
    if (company_name!=''):
        dataframe = dataframe._append(
            pd.Series([
                company_name,
                skills,
                date,
                more_info
            ],
            index = column_headers),
            ignore_index = True)

dataframe.to_excel('Jobs.xlsx')
print('DataFrame is written to Excel File successfully.')
