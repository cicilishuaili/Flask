# Flask on Heroku

This project is intended to help tie together some important concepts and
technologies from TDI 12-day course, including Git, Flask, JSON, Pandas,
Requests, Heroku, and Bokeh for visualization.

The repository used a basic framework for a Flask configuration that will
work on Heroku. That original repo can be found [here](https://github.com/thedataincubator/flask-framework).

The [finished example](https://sli-flask-demo.herokuapp.com/) that demonstrates some basic functionality.

**problems encountered/ lessons learned**

* *Package version agreement for Bokeh.* Need to specify one and the same in BokehJS resources and requirements.txt (0.12.6 here). Depends on how you choose to embed the plot. Took quite a while to get it right.
* *Figuring out json format.* Pretty good once structure becomes clear.
* *Figuring out Flask.* Took a few scattered tries to pick up. Been wanting to play a bit with HTML that was more than changing colors, hopefully all good from here.
* *Storing API key as a config variable.* Always good to know.
* *Running Heroku locally.* Using Pipenv to create a virtualenv and install dependencies.


Pandas is great as always.
