"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""

import os, io
import urllib
from textwrap import wrap
import datetime

from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import render_template, flash, url_for, redirect, jsonify, make_response, send_file, abort, request

from models import Movie, Vote
from decorators import login_required, admin_required
from forms import SearchForm, VoteForm, MovieForm

from google.appengine.api import urlfetch

import logging

import settings

import json


def home():
    
    q = Movie.all()
    q.order("-votes")
    
    return render_template('home.html', movies=q.run(limit=11), form=SearchForm(), image_path=settings.IMAGE_PATH, total=q.count(), offset=0)

def movie(id):
    
    if request.method == "GET":
        
        movie = _fetch_movie(id)
        if movie is not None:
            if request.is_xhr:
                return jsonify({"service_id":movie.service_id, "title": movie.title, "description": movie.description, "poster": movie.poster, "year": movie.year, "imdb_id": movie.imdb_id, "votes": movie.votes, "in_production": movie.being_made, "produced": movie.already_made, "facebook_uid": movie.facebook_uid, "facebook_name": movie.facebook_name})
            
            voters = _fetch_latest_votes(id)
            
            return render_template('single.html', movie=movie, image_path=settings.IMAGE_PATH, voters=voters)
    
    if request.method == "POST":
        form = MovieForm(request.form)
        if form.validate() is False:
            
            for error in form.errors:
                logging.info(error)
            
            return abort(500)
        
        if _validate_user(form.facebook_uid.data, form.facebook_token.data):
            
            movie = _fetch_movie(form.service_id.data)
            
            if movie is None:
                
                m = Movie(service_id=form.service_id.data, title=form.title.data, year=form.year.data.split("-")[0], poster=form.poster.data, description=form.description.data, imdb_id=form.imdb_id.data, facebook_uid=form.facebook_uid.data, facebook_name=form.facebook_name.data)
                m.save()
            
            return jsonify(result="success")
        
        return abort(500)
    
    return abort(404)


def movies():
    
    if request.is_xhr:
    
        q = Movie.all()
        q.order("-votes")
    
        limit = 11
        offset = 0
    
        if "limit" in request.form:
            try:
                limit = int(request.form['limit'])
            except Exception, e:
                pass
    
        if "offset" in request.form:
            try:
                offset = int(request.form['offset'])
            except Exception, e:
                pass
    
        return render_template('includes/movielist.html', movies=q.run(limit=limit, offset=offset), image_path=settings.IMAGE_PATH, total=q.count(), offset=offset)
    
    return redirect(url_for('home'))


def vote(id):
    
    form = VoteForm(request.form)
    
    if request.method == "POST" and form.validate():
        
        if _validate_user(form.facebook_uid.data, form.facebook_token.data):
            
            if _make_vote(form.service_id.data, form.facebook_uid.data, form.facebook_name.data):
                
                return jsonify(result="success")
            else:
                logging.info("could not make vote..")
        else:
            
            logging.info("could not validate user...")
            
    else:
       
       logging.info(len(form.errors))
       for error in form.errors:
           logging.info(error)
    
    return abort(403)


def _validate_user(uid, token):
    
    url = "https://graph.facebook.com/%s?fields=id&access_token=%s" % (uid, token)
    
    try:
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            
            try:
                data = json.loads(result.content)
                
                if 'id' in data:
                    return True
                
            except Exception, e:
                pass
    except Exception, e:
        pass
    
    return False

def _make_vote(id, uid, name):
            
    movie = _fetch_movie(id)
    
    if movie:
        
        q = db.Query(Vote)
        q.filter('service_id =', id)
        q.filter('facebook_uid =', uid)
            
        existing_vote = q.get()
        
        if existing_vote:
            return False
        
        movie.votes = movie.votes + 1;
        movie.put()
        
        thevote = Vote(service_id=id, facebook_uid=uid, facebook_name=name)
        thevote.save()
        
        return True
    
    return False
    
def _fetch_movie(id):
    
    q = db.Query(Movie)
    q.filter('service_id =', id)
        
    movie = q.get()
    if movie:
        return movie
        
    q = db.Query(Movie)
    q.filter('imdb_id =', id)
        
    movie = q.get()
    if movie:
        return movie
    
    return None
    
def _fetch_latest_votes(id, limit=10):
    q = db.Query(Vote)
    q.filter('service_id =', id)
    q.order('-timestamp')
        
    return q.run(limit=limit)
    
def _fetch_latest_vote(id):
    q = db.Query(Vote)
    q.filter('service_id =', id)
    q.order('-timestamp')
        
    vote = q.get()
    if vote:
        return vote
        
    return None
    

"""
def create():
    
    # do some input validation
    form = CardForm(request.form)
    
    if request.method == "POST" and form.validate():
        
        to = form.to.data
        sender = form.sender.data
        message = form.message.data
        facebook_uid = form.facebook_uid.data
        facebook_name = form.facebook_name.data
    
        # path to local assets
        title_font_path = os.path.join(os.path.split(__file__)[0], 'assets/fonts/HelveticaNeue-Bold.ttf')
        body_font_path = os.path.join(os.path.split(__file__)[0], 'assets/fonts/HelveticaNeue.ttf')
        img_path = os.path.join(os.path.split(__file__)[0], 'assets/card.png')
    
        # lets create the image
        tcolor = (255,255,255)
        
        # first title
        title_font = ImageFont.truetype(title_font_path,20)
        title_text = to.strip()
        title_pos = (84,252)
        
        #then body
        body_font = ImageFont.truetype(title_font_path,15)
        body_text = message.strip()
        body_pos = (84, 282)

        img = Image.open(img_path)
        draw = ImageDraw.Draw(img)
        
        title_lines = wrap(title_text, 40)
        
        for line in title_lines:
            draw.text(title_pos, line.strip(), fill=tcolor, font=title_font)
            title_pos = (title_pos[0], title_pos[1]+20)
        
        body_pos = (body_pos[0], title_pos[1]+8)
        
        body_lines = wrap(body_text, 50)
        for line in body_lines:
            draw.text(body_pos, line.strip(), fill=tcolor, font=body_font)
            body_pos = (body_pos[0], body_pos[1]+20)
        
        body_pos = (body_pos[0], body_pos[1]+6)
        
        sender_text = "/%s" % sender
        sender_text = sender_text
        
        draw.text(body_pos, sender_text.strip(), fill=tcolor, font=body_font)
        
        del draw
    
        # create string output
        output = StringIO.StringIO()
        img.save(output, format="PNG")
    
        contents = output.getvalue()
        output.close()
    
        # create card
        card = Card(to=to, sender=sender, message=message, facebook_uid=facebook_uid, facebook_name=facebook_name, image=db.Blob(contents))
    
        try:
            card.put()
            return jsonify(result=card.key().id_or_name())
        except Exception, e:
            return jsonify(result={"error": "Could not save card"})
    
    else:
        return jsonify(result={"error":form.errors})

# list all posts
@admin_required
def list(offset=0):
    
    limit = 50
    time_filter = datetime.date(2012, 12, 11)
    
    try:
        count = Card.all().filter("timestamp >", time_filter).count(limit=4000)
    except Exception, e:
        return abort(500)
    
    try:
        result = Card.all().filter("timestamp >", time_filter).order("-timestamp").fetch(offset=offset,limit=limit)
    except Exception, e:
        return abort(500)
    
    return render_template("list.html", cards=result, offset=offset, totalcount=count, limit=limit, pagend=min(offset+limit, count))

# get images from blobproperty
def image(key):
    
    try:
        entity = Card.get_by_id(int(key))
    except Exception, e:
        entity = Card.get(key)
            
    if entity is not None:
        return send_file(filename_or_fp=io.BytesIO(entity.image), as_attachment=False, attachment_filename="%s.png" % key)
    
    return abort(404)
    

def card(key):
    
    try:
        entity = Card.get_by_id(int(key))
    except Exception, e:
        entity = Card.get(key)
            
    if entity is not None:
        return render_template('single.html', card=entity)
    
    return abort(404)

def terms():
    return render_template("terms.html")

def privacy():
    return render_template("privacy.html")

@login_required
def list_examples():

    examples = ExampleModel.all()
    form = ExampleForm()
    if form.validate_on_submit():
        example = ExampleModel(
            example_name = form.example_name.data,
            example_description = form.example_description.data,
            added_by = users.get_current_user()
        )
        try:
            example.put()
            example_id = example.key().id()
            flash(u'Example %s successfully saved.' % example_id, 'success')
            return redirect(url_for('list_examples'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_examples'))
    return render_template('list_examples.html', examples=examples, form=form)


@login_required
def delete_example(example_id):

    example = ExampleModel.get_by_id(example_id)
    try:
        example.delete()
        flash(u'Example %s successfully deleted.' % example_id, 'success')
        return redirect(url_for('list_examples'))
    except CapabilityDisabledError:
        flash(u'App Engine Datastore is currently in read-only mode.', 'info')
        return redirect(url_for('list_examples'))


@admin_required
def admin_only():

    return 'Super-seekrit admin page.'

"""

def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''
