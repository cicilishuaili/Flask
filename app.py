from flask import Flask, render_template, request, redirect

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

        f = open('%s.txt'%(app.vars['name']),'w')
        for feat in app.vars['dates']+app.vars['features']:
            f.write('%s\n'%(feat))
        f.close()

        return redirect('/graph')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/graph')
def graph():
    return "hello world"

if __name__ == '__main__':
    app.run(port=33507)
