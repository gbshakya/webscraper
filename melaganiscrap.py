from bs4 import BeautifulSoup
import requests
import csv

##arrays for types
fieldNames = ["Symbol","Sector","SharessOutstanding","MarketPrice","PercentChange","LastTradeON","52LowHigh","180Ave","120Ave","OneYearYield","EPS","P/E","BookValue","Pbv"]
sector = []
sharesOutstanding = []
marketPrice = []
percentChange = []
lastTradedOn = []
fiftyTwoLowHigh = []
OneTwentyAve = []
OneEightAve = []
OneYearYield = []
eps = []
ProfToEarning = []
BookValue = []
pbv=[]
perDivid = []
bonus = []
rightShare = []
thirtydayavevole = []
marketCapt = []



url = "https://merolagani.com/CompanyDetail.aspx?symbol=bokl"
page = requests.get(url)
soup = BeautifulSoup(page.content,'html5lib')
tbody = soup.findAll("tbody")
#print(len(tbody))

#print(tbody[9].text)
#print("NEXT LINE")

with open('info.csv' ,'w') as file:
    thewriter = csv.writer(file)
    thewriter.writerow(fieldNames)
    length=len(fieldNames)
    dat = ["bokl"]  
    for i in range(0,length):
        word = str(tbody[i].td.text)
    
        new = word.replace('\n','')
        striped = new.strip()
        dat.append(striped)

    print(dat)
    thewriter.writerow(dat)
