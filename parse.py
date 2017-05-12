#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Thu May 11 17:29:32 2017

@author: n_venkata
"""

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError



import pandas as pd
from flask import Flask
from flask import request
import json
app = Flask(__name__)

@app.route('/jobotService2')
def parse_data():
    
    unspc = pd.read_excel("UNSPSC Reference.xlsx")
    tandt = pd.read_excel("Tools and Technology.xlsx")
    inputtitle = 'Chief Executives'#request.args.get('title')
    inputskill = 'Word processing software'#request.args.get('skill')
    
    comodity_code = tandt['Commodity Code'][(tandt['Title'] == inputtitle) & (tandt['Hot Technology'] == "Y")]
    comodity_code_n= tandt['Commodity Code'][(tandt['Title'] == inputtitle)&(tandt['Commodity Title'] == inputskill) & (tandt['Hot Technology'] == "N")]
    results_classcode = unspc[unspc['Commodity Code'].isin(list(comodity_code))]
    results_classcode_n = unspc[unspc['Commodity Code'].isin(list(comodity_code_n))]
    final_results = results_classcode[results_classcode['Class Code'].isin(list(results_classcode_n['Class Code']))]
    
    if len(final_results) == 0:
        final_results = results_classcode[results_classcode['Family Code'].isin(list(results_classcode_n['Family Code']))]
    
    if len(final_results) == 0:
        final_results = unspc[unspc['Commodity Code'].isin(list(comodity_code))]
    #unique(final_results['Commodity Title'])
    jsondata = []
    l = 0
    for val in final_results['Commodity Title']:
        print(val)
        data = {}
        data[l] = val
        jsondata.append(data)
        l = l+1
    jsonreturn = json.dumps(jsondata)
    print(jsonreturn)
    return jsonreturn
    #return str(final_results['Class Title']), str(final_results['Family Title'])

if __name__ == '__main__':
  app.run()



#tandt = pd.read_excel("Tools and Technology.xlsx")


