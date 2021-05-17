
from py4web import action, request, abort, redirect, URL
from bottle import static_file
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from wtforms import Form, BooleanField, StringField, SelectField,validators, SubmitField, FileField, TextAreaField
import os
from . import settings
from hashlib import md5
from time import localtime

# Kevin Keller wtforms test, copy from https://groups.google.com/g/py4web/c/ORW-ZeGgAjM



#@unauthenticated("index", "index.html")
#def index():
#    user = auth.get_user()
#    flash.set("Hello world")
#    message = T("Hello {first_name}".format(**user) if user else "Hello")
#    return dict(message=message)

from py4web.core import Template  # , Reloader
from yatl.helpers import A, I, SPAN, XML, DIV, P
from py4web import action, request, response, abort, redirect, URL, Field



@unauthenticated("index", "index.html")
def index():
    user = auth.get_user()
    message = T("Hello, {first_name}".format(**user) if user else "Hello")
    mymenu = DIV(
               P( "wtforms-test:  pip install wtforms;"),
               P( "pls, login or register; known users anil@nil.com , bnil@nil.com , cnil@nil.com ; pass= xyz12345 "),
               A( "register", _role="button", _href=URL('register', ),) ,
               A( "upload", _role="button", _href=URL('upload', ),) ,
               A( "skipakke", _role="button", _href=URL('skipakke', ),) ,
              )
    return dict(message=message, mymenu=mymenu)




def renamefile(extension):
    prefix = md5(str(localtime()).encode('utf-8')).hexdigest()
    return f"{prefix}{extension}"


class UploadForm(Form):
    image        = FileField(u'Image File')
    description  = TextAreaField(u'Image Description')
    submit = SubmitField ("Send")

@action("upload", method=["POST", "GET"])
@action.uses(db, session, auth, "upload.html")
def upload():

    user = auth.get_user()
    message = T("Hello, {first_name}".format(**user) if user else "Hello")
    if user is None:
        redirect(URL('index'))
 

    form = UploadForm(request.POST)
    if form.image.data:
        image_data = request.files.get('image')
        orgfilename=image_data.filename
        name, ext = os.path.splitext(image_data.filename)
        if ext not in ('.png', '.jpg', '.jpeg'):
            return "File extension not allowed."
        renamedfile=renamefile(ext)
        file_path = "{path}/{file}".format(path=settings.UPLOAD_PATH, file=renamedfile)
        db.test.update_or_insert(file=renamedfile)
        image_data.save(file_path)
   
    fileimg = db(db.test.id=='2').select(db.test.file).first()
    downloadurl= f'/{settings.APP_NAME}/static/images/'
    #downloadurl='/wtformtest/static/images/'
   
    return dict(form=form,fileimg=fileimg, downloadurl=downloadurl)
    
    


class RegistrationForm(Form):
    email        = StringField('Email Address', [validators.Length(min=6, max=35)])
    name        =  StringField('Name', [validators.Length(min=6, max=35)])
    submit = SubmitField ("Send")
  

class SkipakkeForm(Form):
    alpin_ski = SelectField('Select your ski size', choices=[])
    submit = SubmitField ( " Send ")

@action("skipakke", method=["POST", "GET"])
@action.uses(db, session, auth, "ski.html")
def skipakke():

    user = auth.get_user()
    message = T("Hello, {first_name}".format(**user) if user else "Hello")
    if user is None:
        redirect(URL('index'))

    form = SkipakkeForm(request.POST)

    # Clear the SelectField on page load
    form.alpin_ski.choices = []        

    dalrows = db(db.skipakke_alpin_ski.stock > 0).select(db.skipakke_alpin_ski.length,db.skipakke_alpin_ski.id)
    for dalrow in dalrows:
        alplength=str(dalrow.length)
        form.alpin_ski.choices += [(dalrow.id, alplength + ' cm')]
        
    return dict(form=form)





@action("register", method=["POST", "GET"])
@action("register/<id>", method=["POST", "GET"])
@action.uses(db, session, auth, "register.html")
def register(id=None):

    user = auth.get_user()
    if user is None:
        redirect(URL('index'))
    
    form = RegistrationForm(request.POST)
        
    if id !=None:
        formvalues=db(db.test.id==id).select(db.test.name, db.test.email).first()
        form.email.data=formvalues.email
        form.name.data=formvalues.name
        
    if request.method == 'POST':
        email =  request.forms.get('email')
        # showing whats submitted
        print (email)
        # showing whats submitted
        for key, value in request.forms.items():
            if key !="submit":
                print("For name " + key + ", the value is " + value)
        # showing whats submitted
        print(list(request.forms.items()))
        # deleting submit values from submit button itself before insert into db
        del request.forms['submit']
        # showing submit data after removing submit values from dict, ready to be inserted into db
        db.test.file.default="none.jpg"
        print(list(request.forms.items()))
        db.test.update_or_insert(db.test.id==id, **db.test._filter_fields(request.forms))
        if id !=None:
            redirect(URL('register/'+id))
        else:
            redirect(URL('register'))
            
    return dict(form=form)
   
