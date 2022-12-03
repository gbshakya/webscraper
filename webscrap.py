from bs4 import BeautifulSoup
import requests
import csv


dat = ["BOKL"]
merLaganiUrl = "https://merolagani.com/CompanyDetail.aspx?symbol=bokl" 



    
##Scraping values
fieldNames = ["Symbol","Sector","SharessOutstanding","MarketPrice","PercentChange","LastTradeON","52LowHigh","180Ave","120Ave","OneYearYield","EPS","P/E","BookValue","Pbv"]
with open('infotest.csv','w') as file:
    thewriter = csv.writer(file)
    thewriter.writerow(fieldNames)
    lagpage = requests.get(merLaganiUrl)
    soup = BeautifulSoup(lagpage.content,'html5lib')
    tbody = soup.findAll("tbody")
    length=len(fieldNames)
    for j in range(0,length + 4):


        try:
            word = str(tbody[j].td.text)
            new = word.replace('\n','')
            striped = new.strip()
            dat.append(striped)
            print(striped)
        except:
            dat.append(0)
    thewriter.writerow(dat)



    


