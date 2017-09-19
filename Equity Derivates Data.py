from nsepy import get_history
from datetime import date
import arrow
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import datetime


s=str(arrow.now().format("YYYY-MM-DD"))
def get_date(s):
    dt = []
    for t in s.split("-"):
        dt.append(int(t))
    return dt 
def get_CMP(sy):    
    underlying = get_history(symbol=sy,
                            start=date(get_date(start)[0],get_date(start)[1],get_date(start)[2]), 
                            end=date(get_date(s)[0],get_date(s)[1],get_date(s)[2]),
                            futures=True,
                            expiry_date=date(get_date(d)[0],get_date(d)[1],get_date(d)[2]))
    CMP = int(underlying["Underlying"][0])

    return (CMP)

#List of top stock futures
stks= ["SBIN","INFY","VEDL","APOLLOTYRE","RELCAPITAL",
       "BHARATFIN","MARUTI","ICICIBANK","TATAMOTORS","YESBANK",
       "HINDALCO","AXISBANK","HDFCBANK","TCS","RELIANCE",
       "ITC","ULTRACEMCO","POWERGRID","HDFC","LT",
       "BAJAJ-AUTO","KOTAKBANK","ASHOKLEY","GRASIM",
      "TATASTEEL","INDUSINDBK","HEROMOTOCO","HINDUNILVR"]

#Creating Dataframe for Stock Futures for Current Month Time Series
fut = get_history(symbol=stks[0], 
                      start=date(2017,1,1),
                      end=date(2017,12,31),
                      index=False,
                      futures=True,
                      expiry_date=date(2017,1,25))
month=1
for i in [23,30,27,25,29,27,31]:
    month+=1
    numb = get_history(symbol=stks[0], 
                      start=date(2017,month,1),
                      end=date(2017,12,31),
                      index=False,
                      futures=True,
                      expiry_date=date(2017,month,i))
    fut = fut.append(numb)
for j in stks[1:len(stks)+1]:
    month=1
    fut = fut.append(get_history(symbol=j, 
                                 start=date(2017,1,1),
                                 end=date(2017,12,31),
                                 index=False,
                                 futures=True,
                                 expiry_date=date(2017,1,25)))
    for k in [23,30,27,25,29,27,31]:
        month+=1
        numb_ent1 = get_history(symbol=j, 
                                start=date(2017,month,1),
                                end=date(2017,12,31),
                                index=False,
                                futures=True,
                                expiry_date=date(2017,month,k))
        fut = fut.append(numb_ent1)
fut
fut['Premium']=fut['Settle Price']-fut['Underlying']


#Creating New Dataframe for Monthly Trend Analysis
f=pd.DataFrame(fut[(fut['Symbol']=='SBIN')].ix[datetime.date(2017,1,2)])
f=f.T
month=1
for i in [1,1,3,2,1,3]:
    month+=1
    g=(pd.DataFrame(fut[(fut['Symbol']=='SBIN')].ix[datetime.date(2017,month,i)])).T
    f=f.append(g)

for i in range(1,28):
    month=1
    f=f.append((pd.DataFrame(fut[(fut['Symbol']==stks[i])].ix[datetime.date(2017,month,2)])).T)
    for j in [1,1,3,2,1,3]:
        month+=1
        g=(pd.DataFrame(fut[(fut['Symbol']==stks[i])].ix[datetime.date(2017,month,j)])).T
        f=f.append(g)

start = input('Start date(YYYY-MM-DD):')
d = input('Expiry date(YYYY-MM-DD):')
typ = input('CE or PE:')
    
putopt = get_history(symbol=stks[0], 
                           start=date(get_date(start)[0],get_date(start)[1],get_date(start)[2]),
                           end=date(get_date(s)[0],get_date(s)[1],get_date(s)[2]),
                           option_type=typ,
                           strike_price=get_CMP(stks[0])-0.1*(get_CMP)(stks[0]),
                           index=False,
                           expiry_date=date(get_date(d)[0],get_date(d)[1],get_date(d)[2]))

for i in range (len(stks)):    
    if i == 0:
        a,b = (get_CMP(stks[i])-0.1*(get_CMP)(stks[i]))+10,get_CMP(stks[i])+0.1*(get_CMP)(stks[i])
        y=get_CMP(stks[i])-0.1*(get_CMP)(stks[i])+5
    elif i!=0:
        a,b = (get_CMP(stks[i])-0.1*(get_CMP)(stks[i]))+10,get_CMP(stks[i])+0.1*(get_CMP)(stks[i])
        y=get_CMP(stks[i])-0.1*(get_CMP)(stks[i])
    putopt = putopt.append(get_history(symbol=stks[i], 
                           start=date(get_date(start)[0],get_date(start)[1],get_date(start)[2]),
                           end=date(get_date(s)[0],get_date(s)[1],get_date(s)[2]),
                           option_type=typ,
                           strike_price=y,
                           index=False,
                           expiry_date=date(get_date(d)[0],get_date(d)[1],get_date(d)[2])))
    for x in range(int(a),int(b)):
        puttopt = get_history(symbol=stks[i], 
                              start=date(get_date(start)[0],get_date(start)[1],get_date(start)[2]),
                              end=date(get_date(s)[0],get_date(s)[1],get_date(s)[2]),
                              option_type=typ,
                              strike_price=x,
                              index=False,
                              expiry_date=date(get_date(d)[0],get_date(d)[1],get_date(d)[2]))
        putopt =putopt.append(puttopt)
putopt=putopt.set_index('Strike Price')

typ = input('CE or PE:')
    
calopt = get_history(symbol=stks[0], 
                           start=date(get_date(start)[0],get_date(start)[1],get_date(start)[2]),
                           end=date(get_date(s)[0],get_date(s)[1],get_date(s)[2]),
                           option_type=typ,
                           strike_price=get_CMP(stks[0])-0.1*(get_CMP)(stks[0]),
                           index=False,
                           expiry_date=date(get_date(d)[0],get_date(d)[1],get_date(d)[2]))

for i in range (len(stks)):    
    if i == 0:
        a,b = (get_CMP(stks[i])-0.1*(get_CMP)(stks[i]))+10,get_CMP(stks[i])+0.1*(get_CMP)(stks[i])
        y=get_CMP(stks[i])-0.1*(get_CMP)(stks[i])+5
    elif i!=0:
        a,b = (get_CMP(stks[i])-0.1*(get_CMP)(stks[i]))+10,get_CMP(stks[i])+0.1*(get_CMP)(stks[i])
        y=get_CMP(stks[i])-0.1*(get_CMP)(stks[i])
    calopt = calopt.append(get_history(symbol=stks[i], 
                           start=date(get_date(start)[0],get_date(start)[1],get_date(start)[2]),
                           end=date(get_date(s)[0],get_date(s)[1],get_date(s)[2]),
                           option_type=typ,
                           strike_price=y,
                           index=False,
                           expiry_date=date(get_date(d)[0],get_date(d)[1],get_date(d)[2])))
    for x in range(int(a),int(b)):
        callopt = get_history(symbol=stks[i], 
                              start=date(get_date(start)[0],get_date(start)[1],get_date(start)[2]),
                              end=date(get_date(s)[0],get_date(s)[1],get_date(s)[2]),
                              option_type=typ,
                              strike_price=x,
                              index=False,
                              expiry_date=date(get_date(d)[0],get_date(d)[1],get_date(d)[2]))
        calopt =calopt.append(callopt)
calopt=calopt.set_index('Strike Price')


#Graphing Stock Option data
pp1 = PdfPages('Stock Options.pdf')
for i in range (0,28):
    fig2, ax2 = plt.subplots(nrows=1, ncols=2)
    fig2.set_size_inches(20, 8)
    plt.subplots_adjust(wspace=0.5)
    calopt.loc[(calopt['Symbol']==stks[i])].plot(y="Open Interest",kind="bar", ax=ax2[0])
    plt.tight_layout()
    ax2[0].set_title(stks[i]+' - '+'Call'+'   '+'CMP:'+str(get_CMP(stks[i])), size=20)
    ax2[0].set_xlabel('Strike Price',fontsize=16)
    ax2[0].set_ylabel('Open Interest',fontsize=16)
    ax2[0].tick_params(labelsize=15)
    a=ax2[0].get_ylim()
    putopt.loc[(putopt['Symbol']==stks[i])].plot(y="Open Interest",kind="bar",color=['r'],sharey=True,ax=ax2[1])
    plt.tight_layout()
    ax2[1].set_title(stks[i]+' - '+'Put'+'   '+'CMP:'+str(get_CMP(stks[i])), size=20)
    ax2[1].set_xlabel('Strike Price',fontsize=16)
    ax2[1].tick_params(labelsize=15)
    ax2[1].set_ylim(a[0],a[1])
    pp1.savefig()
pp1.close()

#Graphing Current month time series for Open Interest and Price
pp2 = PdfPages('Stock Futures.pdf')
for i in range (0,20):
    stk=fut[(fut['Symbol']==stks[i])]
    chunk=stk[(stk['Expiry']==date(get_date(d)[0],get_date(d)[1],get_date(d)[2]))]
    fig = plt.figure()        # Create matplotlib figure
    ax = fig.add_subplot(111) # Create matplotlib axes
    ax2 = ax.twinx()          # Create another axes that shares the same x-axis as ax.
    chunk.plot(y='Open Interest',kind='line', color='red', ax=ax,title=stks[i]+' - '+'Futures'+'    '+'Time series of Current month')
    chunk.Close.plot(kind='line', color='blue', ax=ax2)
    ax.set_ylabel('Open Interest')
    ax2.set_ylabel('Close')
    fig.autofmt_xdate()
    plt.tight_layout()
    pp2.savefig()
for j in range (20,28):
    stk=fut[(fut['Symbol']==stks[j])]
    chunk=stk[(stk['Expiry']==date(get_date(d)[0],get_date(d)[1],get_date(d)[2]))]
    fig = plt.figure()        # Create matplotlib figure
    ax = fig.add_subplot(111) # Create matplotlib axes
    ax2 = ax.twinx()           # Create another axes that shares the same x-axis as ax.
    chunk.plot(y='Open Interest',kind='line', color='red', ax=ax,title=stks[j]+' - '+'Futures'+'    '+'Time series of Current month')
    chunk.Close.plot(kind='line', color='blue', ax=ax2)
    ax.set_ylabel('Open Interest')
    ax2.set_ylabel('Close')
    fig.autofmt_xdate()
    plt.tight_layout()
    pp2.savefig()
pp2.close()


#Graphing Current month time series for Futures Premium
pp3=PdfPages('Futures Premium.pdf')
for i in range(0,20):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    prem=fut[(fut['Symbol']==stks[i])]
    prem_chunk=prem[(prem['Expiry']==date(get_date(d)[0],get_date(d)[1],get_date(d)[2]))]
    prem_chunk.plot(y='Premium',kind='line',color='g',ax=ax,title=stks[i]+' - '+'Futures Premium Time Series(Current Month)')
    fig.autofmt_xdate()
    pp3.savefig()
for i in range(20,28):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    prem=fut[(fut['Symbol']==stks[i])]
    prem_chunk=prem[(prem['Expiry']==date(get_date(d)[0],get_date(d)[1],get_date(d)[2]))]
    prem_chunk.plot(y='Premium',kind='line',color='g',ax=ax,title=stks[i]+' - '+'Futures Premium Time Series(Current Month)')
    fig.autofmt_xdate()
    pp3.savefig()
pp3.close()


#Graphing Monthly time series for Open Interest and Price
pp4 = PdfPages('Stock Futures Monthly Series.pdf')
for i in range (0,20):
    fig = plt.figure()        # Create matplotlib figure
    ax = fig.add_subplot(111) # Create matplotlib axes
    ax2 = ax.twinx()          # Create another axes that shares the same x-axis as ax.
    f[f['Symbol']==stks[i]].plot(y='Open Interest',kind='line', color='red', ax=ax,title=stks[i]+' - '+'Futures'+'     '+'Open Interest by Month')
    f[f['Symbol']==stks[i]].Close.plot(kind='line', color='blue', ax=ax2)
    ax.set_ylabel('Open Interest')
    ax2.set_ylabel('Close')
    fig.autofmt_xdate()
    plt.tight_layout()
    pp4.savefig()
for j in range (20,28):
    stk=fut[(fut['Symbol']==stks[j])]
    chunk=stk[(stk['Expiry']==date(get_date(d)[0],get_date(d)[1],get_date(d)[2]))]
    fig = plt.figure()        # Create matplotlib figure
    ax = fig.add_subplot(111) # Create matplotlib axes
    ax2 = ax.twinx()          # Create another axes that shares the same x-axis as ax.
    f[f['Symbol']==stks[i]].plot(y='Open Interest',kind='line', color='red', ax=ax,title=stks[j]+' - '+'Futures'+'     '+'Open Interest by Month')
    f[f['Symbol']==stks[i]].Close.plot(kind='line', color='blue', ax=ax2)
    ax.set_ylabel('Open Interest')
    ax2.set_ylabel('Close')
    fig.autofmt_xdate()
    plt.tight_layout()
    pp4.savefig()
pp4.close()
