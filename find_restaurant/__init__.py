from flask import Flask
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__)
app.config.from_object('config')

Base = declarative_base()
engine = create_engine(app.config['DATABASE_URI'])
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
dbsession = DBSession()

from find_restaurant.member.views import members
from find_restaurant.api.views import api
app.register_blueprint(members)
app.register_blueprint(api, url_prefix='/api')
