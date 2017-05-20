from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from police.api import app as api
from flask import Flask, render_template

app = Flask(__name__)

# API endpoint for a healthcheck
@app.route('/health/')
def healthcheck():
    return 'Healthy', 200

# Endpoint for the demo comment section
@app.route('/demo/')
def demo():
    return render_template('demo.html')

dispatcher = DispatcherMiddleware(app, {
    '/api/v0': api,
})

if __name__ == '__main__':
    run_simple('localhost', 8080,
               dispatcher,
               use_reloader=True,
               use_debugger=True,
               use_evalex=True
               )
