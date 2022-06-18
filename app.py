from flask import Flask, redirect, render_template, url_for
import os
# import pandas as pd
app = Flask(__name__)

@app.route('/')
def encoder():
  return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')
if __name__ == "__main__":
  app.run(debug=True)

# add last modified timestamp to fix browser caching of old assets
@app.context_processor
def override_url_for():
  return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
  if endpoint == 'static':
    filename = values.get('filename', None)
    if filename:
      file_path = os.path.join(app.root_path, endpoint, filename)
      values['q'] = int(os.stat(file_path).st_mtime)
  return url_for(endpoint, **values)