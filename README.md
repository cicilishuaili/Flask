# Flask on Heroku

This project help ties together some important concepts and
technologies, including Git, Flask, JSON, Pandas,
Requests, Heroku, and Bokeh for visualization.

The app use a basic framework for a Flask configuration that will
work on Heroku. That original template repo can be found [here](https://github.com/thedataincubator/flask-framework).

The [finished example](https://sli-flask-demo.herokuapp.com/) that demonstrates some basic functionality.

**problems encountered/ lessons learned**

* _Figuring out Flask._ Took a few scattered tries to pick up. Been wanting to play a bit with HTML that was more than changing colors, hopefully all good from here.
* _Figuring out json format._ Pretty good once structure becomes clear.
* _Storing API key as a config variable._ Always good to know.
* _Running Heroku locally._ Using Pipenv to create a virtualenv and install dependencies.
* _Package version agreement for Bokeh._ Need to specify one and the same in BokehJS resources and requirements.txt (0.12.6 here). Depends on how you choose to embed the plot. Took quite a while to get it right.

Pandas is great as always.
