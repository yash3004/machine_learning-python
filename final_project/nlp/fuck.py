#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 16:29:20 2021

@author: yash
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
from plotly import express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from plotly import tools
import io
import base64

app = dash.Dash()
b = []

df = pd.read_csv('balanced_rev_2.csv')

for i in df['positivity']:
    if (i == '[0]'):
        i = 0
    else:
        i = 1#print(a.item())
    print(i)
    b.append(i)
def pie():    
    a = [b.count(1) , b.count(0)]
    plt.pie(a)
    plt.pie(a)
    
    plt.savefig('foo.png')
