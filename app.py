from flask import Flask, render_template, url_for, abort
import random, os
# import pandas as pd
app = Flask(__name__)
app.debug = False

if __name__ == '__main__':
  app.run(host='0.0.0.0')

@app.template_filter('shuffle')
def filter_shuffle(seq):
  try:
    result = list(seq)
    random.shuffle(result)
    return result
  except:
    return seq

# Capitalize first letter, leave rest unchanged
# for page titles in _header.html
@app.template_filter('capfirst')
def filter_capfirst(s):
  return s[:1].upper() + s[1:]

# @app.route('/')
# def index():
#   return render_template('index.html')

# @app.route('/work')
# def work():
#   path = "static/img/projects"
#   fname = []
#   for root, d_names, f_names in os.walk(path):
#     for f in f_names:
#       fname.append(os.path.join(root, f))
#   return render_template('work.html', work_list = fname)

@app.route('/')
def work():
  path = "static/img/projects"
  fname = []
  for root, d_names, f_names in os.walk(path):
    for f in f_names:
      fname.append(os.path.join(root, f))
  return render_template('work.html', work_list = fname)

@app.route('/news')
def news():
  return render_template('news.html')

@app.route('/shop')
def shop():
  return render_template('shop.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/contact')
def contact():
  return render_template('contact.html')

@app.route('/projects/<project>')
def project(project):
  path = "static/img/projects/" + project
  fname = []
  for root, d_names, f_names in os.walk(path):
    for f in f_names:
      fname.append(os.path.join(root, f))
  return render_template('projects/' + project + '.html', project = project, work_list = fname)

# @app.route('/products/<product>')
# def product(product):
#   return render_template('products/' + product + '.html', product = product)

@app.errorhandler(404)
def page_not_found(error):
  return render_template('error.html'), 404

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