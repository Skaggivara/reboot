"""
urls.py

URL dispatch route mappings and error handlers

"""

from flask import render_template

from application import app
from application import views


## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=views.warmup)

# Home page
app.add_url_rule('/', 'home', view_func=views.home)

app.add_url_rule('/movie/<id>', 'movie', view_func=views.movie,methods=['GET', 'POST'])
app.add_url_rule('/vote/<id>', 'vote', view_func=views.vote,methods=['GET', 'POST'])
app.add_url_rule('/movies', 'movies', view_func=views.movies, methods=['GET'])
app.add_url_rule('/terms', 'terms', view_func=views.terms)
app.add_url_rule('/privacy', 'privacy', view_func=views.privacy)


# Home page
#app.add_url_rule('/create', 'create', view_func=views.create, methods=['GET', 'POST'])

# List
#app.add_url_rule('/list', 'list', view_func=views.list)
#app.add_url_rule('/list/<int:offset>', 'list', view_func=views.list)
#app.add_url_rule('/image/<key>', 'image', view_func=views.image)

#app.add_url_rule('/villkor', 'terms', view_func=views.terms)
#app.add_url_rule('/integritetspolicy', 'privacy', view_func=views.privacy)


# Examples list page
#app.add_url_rule('/examples', 'list_examples', view_func=views.list_examples, methods=['GET', 'POST'])

# Contrived admin-only view example
#app.add_url_rule('/admin_only', 'admin_only', view_func=views.admin_only)

# Delete an example (post method only)
#app.add_url_rule('/examples/delete/<int:example_id>', view_func=views.delete_example, methods=['POST'])


## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

