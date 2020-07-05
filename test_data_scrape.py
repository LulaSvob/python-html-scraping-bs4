import requests
from bs4 import BeautifulSoup
import csv

r = requests.get('https://www.usclimatedata.com/climate/united-states/us')
# print(len(r.text))

soup = BeautifulSoup(r.text, features="lxml")

# print(soup.title)
# print(soup.title.string)
# print(soup.p)
# print(soup.p.text)
# print(soup.a)
# print(soup.a['title'])
# print()
# print(soup.p.parent)
# print(soup.p.parent.prettify())

# for link in soup.find_all('a'):
#     print(link.get('href'))


base_url = 'https://www.usclimatedata.com'
state_links = []
for link in soup.find_all('a'):
    url = link.get('href')
    if url and '/climate/' in url and '/climate/united-states/us' not in url:
        state_links.append(url)
# print(state_links)


r = requests.get(base_url + state_links[5])
soup = BeautifulSoup(r.text, features="lxml")
# print(soup)

rows = soup.find_all('tr')
# print(rows)

rows = [row for row in rows if 'Average high' in str(row)]
# print(len(rows))
# print(rows)

high_temps = []
for row in rows:
    tds = row.find_all('td')
    for i in range(1, len(tds)):
        high_temps.append(tds[i].text)
# print(high_temps)


state = soup.title.string.split()[1]
# print(state)
s = soup.title.string
state = s[s.find(' '):s.find('-')].strip()
# print(state)


data = {}
data[state] = high_temps
# print(data)


data = {}
for state_link in state_links:
    url = base_url + state_link
    r = requests.get(base_url + state_link)
    soup = BeautifulSoup(r.text, features="lxml")
    rows = soup.find_all('tr')
    rows = [row for row in rows if 'Average high' in str(row)]
    high_temps = []
    for row in rows:
        tds = row.find_all('td')
        for i in range(1, len(tds)):
            high_temps.append(tds[i].text)
    s = soup.title.string
    state = s[s.find(' '):s.find('-')].strip()
    data[state] = high_temps
# print(data)


with open('high_temps.csv', 'w') as f:
    w = csv.writer(f, quoting=csv.QUOTE_NONE, lineterminator='\n', delimiter=':', escapechar='')
    w.writerows(data.items())
