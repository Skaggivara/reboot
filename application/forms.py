# -*- coding: utf-8 -*-
"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from flaskext import wtf
from flaskext.wtf import validators
    
    
class SearchForm(wtf.Form):
    title = wtf.TextField('Title', validators=[validators.Required(), validators.length(min=2,max=60)])


"""
facebook_uid: "663145775", 
facebook_token: "AAADzRtZCrZCOIBAH5RxDqoa29z28xh5PrrUg7pZAidwhRgTG9…IpiPw61fkjMAysgva5w4PVBmOV6HNFaiZBRIan3lb5odAZDZD", facebook_name: "Isak Wiström", title: "Alien", description: "During its return to the earth, commercial spacesh…e planted inside its unfortunate host is birthed."…}
description: "During its return to the earth, commercial spaceship Nostromo intercepts a distress signal from a distant planet. When a three-member team of the crew discovers a chamber containing thousands of eggs on the planet, a creature inside one of the eggs attacks an explorer. The entire crew is unaware of the impending nightmare set to descend upon them when the alien parasite planted inside its unfortunate host is birthed."
facebook_name: "Isak Wiström"
facebook_token: "AAADzRtZCrZCOIBAH5RxDqoa29z28xh5PrrUg7pZAidwhRgTG9F8H3g1iiyNAGIpiPw61fkjMAysgva5w4PVBmOV6HNFaiZBRIan3lb5odAZDZD"
facebook_uid: "663145775"
imdb_id: "tt0078748"
poster: "/uU9R1byS3USozpzWJ5oz7YAkXyk.jpg"
service_id: 348
title: "Alien"
year: "1979-05-25"
"""

class MovieForm(wtf.Form):
    title = wtf.TextField('Title', validators=[validators.Required(), validators.length(min=2,max=60)])
    year = wtf.TextField('Year', validators=[validators.Required(), validators.length(min=2,max=60)])
    poster = wtf.TextField('Poster', validators=[validators.Required(), validators.length(min=2,max=200)])
    
    description = wtf.TextAreaField('Description', validators=[validators.Required()])
    
    imdb_id = wtf.TextField('Imdb id', validators=[validators.Required(), validators.length(min=2,max=60)])
    service_id = wtf.TextField('Service id', validators=[validators.Required(), validators.length(min=2,max=60)])
    
    facebook_name = wtf.TextField('Facebook name', validators=[validators.Required(), validators.length(min=2,max=60)])
    facebook_uid = wtf.TextField('Facebook uid', validators=[validators.Required(), validators.length(min=2,max=60)])
    facebook_token = wtf.TextField('Facebook token', validators=[validators.Required(), validators.length(min=2,max=200)])

class VoteForm(wtf.Form):
    
    service_id = wtf.TextField('Service ID', validators=[validators.Required(), validators.length(min=2,max=60)])
    facebook_uid = wtf.TextField('Facebook ID', validators=[validators.Required(), validators.length(min=2,max=100)])
    facebook_name = wtf.TextField('Facebook name', validators=[validators.Required(), validators.length(min=2,max=60)])
    facebook_token = wtf.TextField('Facebook token', validators=[validators.Required(), validators.length(min=2,max=200)])