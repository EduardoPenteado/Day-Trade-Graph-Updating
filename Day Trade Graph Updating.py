#!/usr/bin/env python
# coding: utf-8

# In[6]:


import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from time import sleep
from IPython import display

class Day_Trade:
    
    def __init__(self):
        self.stock = input('Stock: ').upper()
        self.bond = yf.download(self.stock+'.SA', period='1d')
        self.bond['Date'] = datetime.today().strftime("%H:%M:%S")
        # The time the stock price will be updated
        self.time = int(input('Time analysis in seconds: '))
        self.clean()
        
    def clean(self):
        return display.clear_output(wait=True)
    
    def fig_update(self, fig):
        fig.update_layout(showlegend=False)
        fig.update_layout(hovermode='x')
        
    def graph(self):
        try:
            fig = go.Figure(go.Indicator(
                            align = 'left',
                            mode = "number+delta",
                            value = self.bond['Close'][-1],
                            number = {'prefix': "R$ ", 'font':{'size':20}},
                            delta = {'position': "top", 'reference': self.bond['Close'][-2]},
                            domain ={'x':[0, 1], 'y':[0.9, 1]}
                            ))
        except Exception:
            fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.bond['Date'], y=self.bond['Close'],line=dict(color='blue')))
        self.fig_update(fig)
        return display.display(fig)
            
    def update(self):
        # to interrupt, just interrupt the kernel.
        check = True
        while check == True:
            try:
                self.graph()
                sleep(self.time)
                bond_update = yf.download(self.stock+'.SA',period='1d')
                bond_update['Date'] = datetime.today().strftime("%H:%M:%S")
                self.bond = pd.concat([self.bond, bond_update])
                self.clean()
            except KeyboardInterrupt:
                check = False
                self.clean()
                print('Stopped')
                self.save_to_excel()

    def save_to_excel(self):
        resp = str(input('Do you want to save the prices in excel? [Y/N]: ')).upper()
        if resp == 'Y' or resp == 'YES':
            name = input(str('Insert the filename: '))
            self.bond.to_excel(name+'.xlsx')
            print('File Saved!')
        print('Closed!')
        
x = Day_Trade()
x.update()

