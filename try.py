from bs4 import BeautifulSoup
import requests
import csv

CompanyNameUrl = "http://www.nepalstock.com/company/index/"

nepstockPage = 17

data = []

for i in range(1,nepstockPage + 1):
    url = "http://www.nepalstock.com/company/index/" + str(i)
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    table = soup.find("table")
    rows = table.findAll("tr")
    #print(len(rows))
    #print(rows[22])
    for j in range(2,22):
        try:
            #print(rows[j].findAll("td")[3].text)
            data.append(rows[j].findAll("td")[3].text)
        except:
            print("scraping finished")
            break
    

print(data)



##Scraping values
fieldNames = ["Symbol","Sector","SharessOutstanding","MarketPrice","PercentChange","LastTradeON","52LowHigh","180Ave","120Ave","OneYearYield","EPS","P/E","BookValue","Pbv","Dividend","random","Bonus","Rand"]
with open('info.csv','w') as file:
    thewriter = csv.writer(file)
    thewriter.writerow(fieldNames)

    for i in range(0,len(data) + 1):
        dat = []
        dat.append(data[i])
        print(len(data))
        print(data[i])
        merLaganiUrl = "https://merolagani.com/CompanyDetail.aspx?symbol=" + data[i]
        lagpage = requests.get(merLaganiUrl)
        soup = BeautifulSoup(lagpage.content,'html5lib')
        tbody = soup.findAll("tbody")
        length=len(fieldNames) 
        for j in range(0,length):


            try:
                word = str(tbody[j].td.text)
                new = word.replace('\n','')
                striped = new.strip()
                dat.append(striped)
            except:
                dat.append("0")
        thewriter.writerow(dat)

