# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 12:08:26 2022

@author: nhillman
"""
from xbbg import blp
from datetime import datetime
from datetime import date
from datetime import timedelta
import datetime
import plotly.graph_objects as go
import os.path
import plotly.io as pio
pio.renderers.default = 'browser'
import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as tls
import pandas as pd


username1 = 'nhillman_aegis'
api_key1 = 'DvCE9Fmcp7G8eusfmOKL'
chart_studio.tools.set_credentials_file(username=username1, api_key=api_key1)

# username2 = 'nhillman_aegis2'
# api_key2 = 'zGBE2dHD252tUipbC6AM'
#chart_studio.tools.set_credentials_file(username=username2, api_key=api_key2)

def candle_function_chart():
    endDate = (date.today())
    today = date.today()
    chartStartDate = date.today() - datetime.timedelta(days=90)
    candle_params = [['HRC1 COMDTY', 'Prompt-Month Hot Rolled Coil Steel'],['LMNIDS03 COMDTY', 'LME Nickel 3M Select'],['LMCADS03 COMDTY', 'LME Copper 3M Select'],['LMAHDS03 COMDTY','LME Aluminum 3M Select']]
    
    x = blp.bdh(
        tickers=['HRC1 COMDTY','LMNIDS03 COMDTY','LMCADS03 COMDTY','LMAHDS03 COMDTY'], flds=['high', 'low', 'last_price','open'],
        start_date= chartStartDate, end_date=endDate, Per='D', Fill='P', Days='T',
    )
    
    df = pd.DataFrame(x)
    df.index.name = 'Date'
 
    def build_candle_chart(ticker, chart_name):
        fig = go.Figure(go.Candlestick(
            x=df.index,
            open=df[ticker,'open'],
            high=df[ticker,'high'],
            low=df[ticker,'low'],
            close=df[ticker,'last_price']
            ))
        
        fig.update_layout(margin=go.layout.Margin(l=20, r=20, b=20, t=30),
                          plot_bgcolor='white',
                          xaxis_rangeslider_visible=False, 
                          yaxis_tickprefix = '$', 
                          yaxis_tickformat = ',.',
                          yaxis_title = y_axis_title, 
                          font=dict(family="Roboto",size=12,color="Black"),
                          legend = dict(orientation = "h", xanchor = "center", x = 0.5),
                          title =dict(text = '<b>' + (chart_name)+ '</b>',y = 1,x = 0.5, xanchor = 'center', yanchor = 'top'),
                          hovermode = "x unified",
                          xaxis_range = [chartStartDate,today])
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray', showline = True, zerolinecolor = 'rgb(0, 45, 93)', zerolinewidth = 2, linecolor = 'rgb(0, 45, 93)', linewidth = 2)
        fig.update_yaxes(showgrid=True,zeroline=True, gridwidth=1, gridcolor='LightGray', showline = True, zerolinecolor = 'rgb(0, 45, 93)', zerolinewidth = 2, linecolor = 'rgb(0, 45, 93)', linewidth = 2)
        filename = str(chart_name) + "_Metals_Price_Dashboard"
        fig.show()
        #
        fig.update_layout(height=432, width=720,
                                 font=dict(family="Roboto",size=12,color="Black"))
        py.plot(fig, filename = filename, auto_open=False)
        
    for x,y in candle_params:
        if x == 'HRC1 COMDTY':
            y_axis_title = "$/Ton"
        else:
            y_axis_title = "$/metric ton"
        
        build_candle_chart(x, y)