
from .common import db, Field
from pydal.validators import *


from .common import db, Field, Tags, groups
from pydal.validators import *
from py4web.utils.populate import populate
from yatl.helpers import SPAN, H6
import datetime


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

def get_download_url(file):                                                  
    return f"upload/{file}" 

db.define_table(
'test',
    Field ('name'),
    Field ('email'),
    Field('file', 'upload')
   )

db.define_table(
'skipakke_alpin_ski',
    Field ('length', 'integer'),
    Field ('stock', 'integer'),
    Field('title')
   )
#



db.commit()

if not db(db.auth_user).count():
    u1 = {
        "username": "anil",
        "email": "anil@nil.com",
        "password": str(CRYPT()("xyz12345")[0]),
        "first_name": "Anil_first",
        "last_name": "Anil_Last",
    }

    u2 = {
        "username": "bnil",
        "email": "bnil@nil.com",
        "password": str(CRYPT()("xyz12345")[0]),
        "first_name": "Bnil_first",
        "last_name": "Bnil_Last",
    }

    u3 = {
        "username": "cnil",
        "email": "cnil@nil.com",
        "password": str(CRYPT()("xyz12345")[0]),
        "first_name": "Cnil_first",
        "last_name": "Cnil_Last",
    }


    for e in [u1, u2, u3]: db.auth_user.insert(**db.auth_user._filter_fields(e) )
    db.commit()

    #groups = Tags(db.auth_user)

    groups.add(1, 'manager')
    groups.add(2, ['dancer', 'teacher'])
    groups.add(3, 'dancer')
    db.commit()


db.define_table(
    'test_table',
    Field( 'f0', 'string', label='l0'),
    Field( 'f1', 'string', label='l1'),
    Field( 'f2', 'string', label='l2'),
    )
db.commit()

if not db(db.test_table).count():
    populate(db.test_table, n=50)
    db.commit()



#
