from bs4 import BeautifulSoup
import requests

import json
import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


email = "EMAIL"
password = "PASSWORD"


session_requests = requests.session()

""" LOGIN AND GET SESSION """
login_url = "https://www.edgeprop.my/user/login"
# Get login csrf token
login_page = session_requests.get(login_url)
soup = BeautifulSoup(login_page.text, 'html.parser')
authenticity_token = soup.find("input", { "name": "form_build_id" } )["value"]
payload = { "name": email, "pass": password, "form_build_id": authenticity_token, "form_id": "user_login" }
# Perform login
result = session_requests.post(login_url, data = payload, headers = dict(referer = login_url))
""" END LOGIN AND GET SESSION """

def scrap(url_k):
	page = session_requests.get(url_k, headers = dict(referer = 'https://www.edgeprop.my/transaction/selangor?start=2012-01-01&end=2018-06-31&price=0'))
	soup = BeautifulSoup(page.text, 'html.parser')

	# Extract result
	date_list = soup.find_all("div", class_="transaction-item transaction-date")
	price_list = soup.find_all("div", class_="transaction-item transaction-price")
	type_list = soup.find_all("div", class_="transaction-item transaction-type2")
	sf_list = soup.find_all("div", class_="transaction-item transaction-sqft")
	addr_list = soup.find_all("div", class_="transaction-item transaction-address")

	d = {
		'date': [date.get_text() for date in date_list],
		'price': [locale.atoi(price.get_text()) for price in price_list],
		'house_type': [hse.get_text() for hse in type_list],
		'area_sf': [locale.atoi(area.get_text()) for area in sf_list],
		'addr': [addr.get_text() for addr in addr_list]
	}

	return pd.DataFrame(data=d)

# load links from json
with open('selangor_name.json') as f:
    data = json.load(f)

# spliting area using the url given
url_list = {
    'area': [d['url'].split('/')[5] for d in data],
    'url': [d['url'] for d in data],
	'neighbourhood': [d['neighbourhood'] for d in data]
}
df_url = pd.DataFrame(data=url_list)

# remove places not in klang valley
not_in_klang_valley = ['tanjong-sepat', 'tanjong-karang', 'batang-berjuntai', 'jenjarom'
					, 'kerling', 'sepang', 'semenyih', 'batang-kali', 'banting'
					, 'pulau-indah-(pulau-lumut)', 'sungai-besar', 'telok-panglima-garang'	
					, 'serendah', 'rasa', 'kuala-selangor', 'sabak-bernam', 'batu-arang'
					, 'beranang', 'jeram', 'kuala-kubu-baru', 'kuala-selangor', 'kuang'
					, 'sekinchan', 'sungai-pelek']
df_url = df_url[~df_url['area'].isin(not_in_klang_valley)]

df = pd.DataFrame(data=[])

# scraping for each url
for index, row in df_url.iterrows():
	df2=scrap(row['url'])
	df2['area'] = row['area']
	df2['neighbourhood'] = row['neighbourhood']
	print(row['area'], ": ", len(df2.index))
	df = df.append(df2)

print('============================================')
print(df.head())
print('total length: ', len(df.index))

# output
df.to_csv('output/selangor.csv', sep=';', index=False )
