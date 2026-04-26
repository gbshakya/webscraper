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

[<tbody class="panel panel-default" style="border: none;">
                        <tr>
                            <th style="width: 200px;">Sector
                            </th>
                            <td class="text-primary">
                                Commercial Banks
                            </td>
                        </tr>
                    </tbody>, <tbody class="panel panel-default" style="border: none;">
                        <tr>
                            <th style="width: 200px;">Shares Outstanding
                            </th>
                            <td class="">
                                270,569,970.00
                            </td>
                        </tr>
                    </tbody>, <tbody class="panel panel-default" style="border: none;">
                        <tr>
                            <th style="width: 200px;">Market Price
                            </th>
                            <td class="">
                                <strong><span class="text-increase" id="ctl00_ContentPlaceHolder1_CompanyDetail1_lblMarketPrice">529.00</span></strong>
                            </td>
                        </tr>
                    </tbody>, <tbody class="panel panel-default" style="border: none;">
                        <tr>
                            <th style="width: 200px;">% Change
                            </th>
                            <td class="">
                                <span class="text-increase" id="ctl00_ContentPlaceHolder1_CompanyDetail1_lblChange">0.38 %</span>
                            </td>
                        </tr>
                    </tbody>, <tbody class="panel panel-default" style="border: none;">
                        <tr>
                            <th style="width: 200px;">Last Traded On
                            </th>
                            <td class="">
                                2026/03/12 02:59:56
                            </td>
                        </tr>
                    </tbody>, <tbody class="panel panel-default" style="border: none;">
                        <tr>
                            <th style="width: 200px;">52 Weeks High - Low
                            </th>
                            <td class="">
                                562.00-471.00
                            </td>
                        </tr>
                    </tbody>, <tbody class="panel panel-default" style="border: none;display: none;">
                        <tr>
                            <th style="width: 200px;">180 Day Average
                            </th>
                            <td class="">
                                503.55
                            </td>
                        </tr>
                    </tbody>, <tbody class="panel panel-default" style="border: none;">
                        <tr>
                            <th style="width: 200px;">120 Day Average
                            </th>
                            <td class="">
                                500.70
                            </td>
                        </tr>
                    </tbody>, <tbody class="panel panel-default" style="border: none;">
                        <tr>
                            <th style="width: 200px;">1 Year Yield
                            </th>
                            <td class="">
                                <span class="text-increase" id="ctl00_ContentPlaceHolder1_CompanyDetail1_lblYearYeild">7.74%</span>
                            </td>
                        </tr>
                    </tbody>, <tbody class="panel panel-default" style="border: none;">
                        <tr>
                            <th style="width: 200px;">EPS
                            </th>
                            <td class="">
                                35.18
                                <span class="text-primary">
                                    (FY:082-083, Q:2)</span>
                            </td>
                        </tr>
                    </tbody>, <tbody class="panel panel-default" style="border: none;">
                        <tr>
                            <th style="width: 200px;">P/E Ratio
                            </th>
                            <td class="">
                                15.04
                            </td>
                        </tr>
                    </tbody>, <tbody class="panel panel-default" style="border: none;">
                        <tr>
                            <th style="width: 200px;">Book Value
                            </th>
                            <td class="">
                                235.64
                            </td>
                        </tr>
                    </tbody>, <tbody class="panel panel-default" style="border: none;">
                        <tr>
                            <th style="width: 200px;">PBV
                            </th>
                            <td class="">
                                2.24
                            </td>
                        </tr>
                    </tbody>, <tbody class="panel panel-default" style="border: none;">
                        <tr>
                            <th style="width: 200px;">
                                <a aria-expanded="true" class="collapsed" data-parent="#accordion" data-toggle="collapse" href="#dividend-panel" title="Show All - Cash Dividend">% Dividend
                                </a>
                            </th>
                            <td class="">
                                12.50
                                <span class="text-primary">
                                    (FY:081-082)</span>
                            </td>
                        </tr>
                        <tr aria-expanded="true" class="panel-collapse collapse" id="dividend-panel">
                            <td colspan="2">
                                <table class="table table-striped table-hover table-zeromargin" style="border: solid 1px #ccc; margin-bottom: 0px">

                                    <tbody>

                                                <tr>
                                                    <th class="td-icon">
                                                        <span>#</span></th>
                                                    <th class="text-center" style="white-space: nowrap">
                                                        <span title="Fiscal Year">Fiscal Year</span></th>

                                                    <th class="text-center">
                                                        <span title="Date">Value</span></th>


                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">1.</td>
                                                    <td class="text-center">
                                                        12.50%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 081-082)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">2.</td>
                                                    <td class="text-center">
                                                        10.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 080-081)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">3.</td>
                                                    <td class="text-center">
                                                        11.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 079-080)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">4.</td>
                                                    <td class="text-center">
                                                        0.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 079-080)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">5.</td>
                                                    <td class="text-center">
                                                        11.50%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 078-079)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">6.</td>
                                                    <td class="text-center">
                                                        0.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 078-079)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">7.</td>
                                                    <td class="text-center">
                                                        4.40%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 077-078)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">8.</td>
                                                    <td class="text-center">
                                                        1.76%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 076-077)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">9.</td>
                                                    <td class="text-center">
                                                        0.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 075-076)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">10.</td>
                                                    <td class="text-center">
                                                        0.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 074-075)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">11.</td>
                                                    <td class="text-center">
                                                        18.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 073-074)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">12.</td>
                                                    <td class="text-center">
                                                        15.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 072-073)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">13.</td>
                                                    <td class="text-center">
                                                        6.84%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 071-072)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">14.</td>
                                                    <td class="text-center">
                                                        0.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 070-071)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">15.</td>
                                                    <td class="text-center">
                                                        40.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 069-070)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">16.</td>
                                                    <td class="text-center">
                                                        40.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 068-069)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">17.</td>
                                                    <td class="text-center">
                                                        30.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 067-068)</td>
                                                </tr>

                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    </tbody>, <tbody>

                                                <tr>
                                                    <th class="td-icon">
                                                        <span>#</span></th>
                                                    <th class="text-center" style="white-space: nowrap">
                                                        <span title="Fiscal Year">Fiscal Year</span></th>

                                                    <th class="text-center">
                                                        <span title="Date">Value</span></th>


                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">1.</td>
                                                    <td class="text-center">
                                                        12.50%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 081-082)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">2.</td>
                                                    <td class="text-center">
                                                        10.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 080-081)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">3.</td>
                                                    <td class="text-center">
                                                        11.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 079-080)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">4.</td>
                                                    <td class="text-center">
                                                        0.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 079-080)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">5.</td>
                                                    <td class="text-center">
                                                        11.50%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 078-079)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">6.</td>
                                                    <td class="text-center">
                                                        0.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 078-079)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">7.</td>
                                                    <td class="text-center">
                                                        4.40%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 077-078)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">8.</td>
                                                    <td class="text-center">
                                                        1.76%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 076-077)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">9.</td>
                                                    <td class="text-center">
                                                        0.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 075-076)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">10.</td>
                                                    <td class="text-center">
                                                        0.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 074-075)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">11.</td>
                                                    <td class="text-center">
                                                        18.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 073-074)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">12.</td>
                                                    <td class="text-center">
                                                        15.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 072-073)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">13.</td>
                                                    <td class="text-center">
                                                        6.84%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 071-072)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">14.</td>
                                                    <td class="text-center">
                                                        0.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 070-071)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">15.</td>
                                                    <td class="text-center">
                                                        40.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 069-070)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">16.</td>
                                                    <td class="text-center">
                                                        40.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 068-069)</td>
                                                </tr>

                                                <tr>
                                                    <td class="text-center td-icon">17.</td>
                                                    <td class="text-center">
                                                        30.00%
                                                    </td>
                                                    <td class="text-center text-primary">(FY: 067-068)</td>
                                                </tr>

                                    </tbody>, <tbody class="panel panel-default" style="border: none;">
                        <tr>

                            <th style="width: 200px;">
                                <a aria-expanded="true" class="collapsed" data-parent="#accordion" data-toggle="collapse" href="#bonus-panel" title="Show All - Cash Dividend">% Bonus
                                </a>
                            </th>
                            <td class="">

                                <span class="text-primary">
                                    </span>
                            </td>
                        </tr>
                        <tr aria-expanded="true" class="panel-collapse collapse" id="bonus-panel">
                            <td colspan="2">
                                <table class="table table-striped table-hover table-zeromargin" style="border: solid 1px #ccc; margin-bottom: 0px">

                                    <tbody>

                                                <tr>
                                                    <th class="td-icon">
                                                        <span>#</span></th>
                                                    <th class="text-center">
                                                        <span title="Date">Value</span></th>
                                                    <th class="text-center" style="white-space: nowrap">
                                                        <span title="Fiscal Year">Fiscal Year</span></th>
                                                </tr>

                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    </tbody>, <tbody>

                                                <tr>
                                                    <th class="td-icon">
                                                        <span>#</span></th>
                                                    <th class="text-center">
                                                        <span title="Date">Value</span></th>
                                                    <th class="text-center" style="white-space: nowrap">
                                                        <span title="Fiscal Year">Fiscal Year</span></th>
                                                </tr>

                                    </tbody>, <tbody class="panel panel-default" style="border: none;">
                        <tr>
                            <th style="width: 200px;">
                                <a aria-expanded="true" class="collapsed" data-parent="#accordion" data-toggle="collapse" href="#right-panel" title="Show All - Cash Dividend">Right Share
                                </a>
                            </th>
                            <td class="">

                                <span class="text-primary">
                                    </span>
                            </td>
                        </tr>
                        <tr aria-expanded="true" class="panel-collapse collapse" id="right-panel">
                            <td colspan="2">
                                <table class="table table-striped table-hover table-zeromargin" style="border: solid 1px #ccc; margin-bottom: 0px">

                                    <tbody>

                                                <tr>
                                                    <th class="td-icon">
                                                        <span>#</span></th>

                                                    <th class="text-center">
                                                        <span title="Date">Value</span></th>
                                                    <th class="text-center" style="white-space: nowrap">
                                                        <span title="Fiscal Year">Fiscal Year</span></th>

                                                </tr>

                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    </tbody>, <tbody>

                                                <tr>
                                                    <th class="td-icon">
                                                        <span>#</span></th>

                                                    <th class="text-center">
                                                        <span title="Date">Value</span></th>
                                                    <th class="text-center" style="white-space: nowrap">
                                                        <span title="Fiscal Year">Fiscal Year</span></th>

                                                </tr>

                                    </tbody>, <tbody class="panel panel-default" style="border: none;">
                        <tr>
                            <th style="width: 200px;">30-Day Avg Volume
                            </th>
                            <td class="">
                                69,271.00
                            </td>
                        </tr>
                    </tbody>, <tbody class="panel panel-default" style="border: none;">
                        <tr>
                            <th style="width: 200px;">Market Capitalization
                            </th>
                            <td class="">
                                143,131,514,130.00
                            </td>
                        </tr>
                    </tbody>, <tbody><tr>
                                            <th style="width: 200px;">
                                                <span title="Stock Symbol">Symbol</span></th>

                                            <td>NABIL</td>
                                        </tr>
                                        <tr>
                                            <th>
                                                <span title="Company Name">Company Name</span></th>

                                            <td>Nabil Bank Limited</td>
                                        </tr>
                                        <tr>
                                            <th>
                                                <span title="Sector Name">Sector</span></th>

                                            <td>Commercial Banks</td>
                                        </tr>
                                        <tr>
                                            <th>
                                                <span title="Listed Shares">Listed Shares</span></th>

                                            <td>270,569,970.00</td>
                                        </tr>
                                        <tr>
                                            <th>
                                                <span title="Paidup Value">Paidup Value</span></th>

                                            <td>100.00</td>
                                        </tr>
                                        <tr>
                                            <th>
                                                <span title="Total Paidup Value">Total Paidup Value</span></th>

                                            <td>27,056,997,000.00</td>
                                        </tr>

                            </tbody>]



    


