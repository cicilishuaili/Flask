from flask import Flask, render_template, request, redirect
import pandas as pd
import requests
import json
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.palettes import brewer
import os
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

app = Flask(__name__)

app.vars={}

@app.route('/')
def home():
    return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        app.vars['name']=request.form['ticker']
        app.vars['features']=request.form.getlist('features')
        app.vars['dates']=request.form.getlist('dates')

#        f = open('%s.txt'%(app.vars['name']),'w')
#        for feat in app.vars['dates']+app.vars['features']:
#            f.write('%s\n'%(feat))
#        f.close()

        return redirect('/graph')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/graph')
def graph():
    name = app.vars['name']
    plotcols = app.vars['features']
    dates = app.vars['dates']
    n = len(plotcols)
    api_key = os.environ.get('QUANDL_KEY')
    payload = {'api_key':api_key, 'ticker':name,
               'date.gte':dates[0], 'date.lte':dates[1],
               'qopts.columns':'date,'+','.join(plotcols)}
#    f = open('%s_graph.txt'%(app.vars['name']),'w')
#    for k,v in payload.items():
#        f.write('%s:%s\n'%(k,v))
#    f.close()
    r = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES', 
                     params = payload)
    
    if r.status_code != 200:
        return "Something's wrong with thes request. Please check ticker entry and try again."
    
    jdata = r.json()
    jtable = jdata.get("datatable")
    data = jtable.get('data')
    clist = jtable.get('columns')
    colnames = [x.get('name') for x in clist]
    
    data_df = pd.read_json(json.dumps(data))
    data_df.columns = colnames
    data_df.date = pd.to_datetime(data_df.date)
    
    p = figure(x_axis_type="datetime", 
               title=name+" QUANDL WIKI Stock Prices from "+dates[0]+" to "+dates[1])

    p.grid.grid_line_alpha=0.3
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    
    colors=brewer['Dark2'][4]
    for i in range(n):
        p.line(data_df.date, data_df[plotcols[i]], 
               legend = name+" : "+plotcols[i],color=colors[i])
    
    p.legend.location = "top_left"
    
    script, div = components(p)
    
    resources = INLINE.render()
    html = render_template('embed.html', plot_script=script, plot_div=div,
                           resources=resources, name=name, 
                           glink='https://www.google.com/finance?q='+name)
    

    html=file_html(p, CDN, "plot")
    return html

if __name__ == '__main__':
    app.run(port=33507)
