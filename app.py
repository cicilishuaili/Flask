from flask import Flask, render_template, request, redirect
import pandas as pd
import requests
import json
from bokeh.plotting import figure
#from bokeh.models import HoverTool
from bokeh.palettes import brewer
import os
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

app = Flask(__name__)

@app.route('/')
def home():
    return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        name = request.form['ticker']
        features = request.form.getlist('features')
        dates = request.form.getlist('dates')
        
        api_key = os.environ.get('QUANDL_KEY')
        payload = {'api_key':api_key,
                   'ticker':name,
                   'date.gte':dates[0], 'date.lte':dates[1],
                   'qopts.columns':'date,'+','.join(features)}

        r = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES', 
                         params=payload)
        
        if r.status_code != 200:
            return "Something's wrong with the request. Please check ticker entry and try again."
        
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
        
    #    hover = HoverTool(
    #        tooltips=[
    #            ('Value', '$y'),
    #            ('Date', '$x{%F}')],
    #        formatters={
    #            '$x'      : 'datetime',
    #        },
    #        mode='vline'
    #)
     
    #    p.add_tools(hover)
    
        p.grid.grid_line_alpha = 0.3
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Price ($)'
        
        colors = brewer['Dark2'][4]
        for i in range(len(features)):
            p.circle(data_df.date, data_df[features[i]], 
                   legend=name+" : "+features[i],
                   color=colors[i], size=2, alpha=0.5)
            p.line(data_df.date, data_df[features[i]], 
                   legend=name+" : "+features[i],
                   color=colors[i],alpha=0.5)
        
        p.legend.location = "top_left"
        
        script, div = components(p)
        
        resources = INLINE.render()
        html = render_template('embed.html', plot_script=script, plot_div=div,
                               resources=resources, name=name)
    
        return encode_utf8(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=33507)
