"""
models.py

App Engine datastore models

"""


from google.appengine.ext import db


class Movie(db.Model):
    
    title = db.StringProperty(required=True)
    year = db.StringProperty(required=True)
    poster = db.StringProperty(required=True)
    
    description = db.TextProperty(required=True)
    
    imdb_id = db.StringProperty(required=True)
    
    votes = db.IntegerProperty(required=False, default=0)
    
    updated = db.DateTimeProperty(auto_now_add=True)
    timestamp = db.DateTimeProperty(auto_now_add=True)
    
    facebook_uid = db.StringProperty(required=True)
    facebook_name = db.StringProperty(required=True)
    
    service_id = db.StringProperty(required=True, default="0")
    
    being_made = db.BooleanProperty(default=False)
    already_made = db.BooleanProperty(default=False)

class Vote(db.Model):
    
    service_id = db.StringProperty(required=True, default="0")
    facebook_uid = db.StringProperty(required=True)
    facebook_name = db.StringProperty(required=True)
    
    timestamp = db.DateTimeProperty(auto_now_add=True)
    
