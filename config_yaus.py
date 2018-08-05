from flask import Flask, request, render_template, redirect, url_for
from urlparse import urlparse
import base64
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, update, create_engine
from sqlalchemy.sql import select, exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import base64


app = Flask(__name__)
engine = create_engine('sqlite:///main.db', connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()
test_url = 'rambler.ru'
Base = declarative_base()


class YAUS_t(Base):
    __tablename__ = 'yaus_t'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String)
    short_url = Column(String)

    def __init__(self, url, short_url):
        self.url = url
        self.short_url = short_url


Base.metadata.create_all(engine)
