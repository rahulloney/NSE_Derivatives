from nsepy import get_history
from datetime import date
import arrow
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import datetime


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
