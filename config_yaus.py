from flask import Flask, request, render_template, redirect, url_for
from urlparse import urlparse
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, update, create_engine
from sqlalchemy.sql import select, exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__)   # create an instance of the Flask class
engine = create_engine('sqlite:///main.db', connect_args={'check_same_thread': False})  # create db engine
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()  # make session
Base = declarative_base()   # class Base

def gnb64(s):
    '''
    :param s: sting to encode
    :return: encoded string
    '''
    b64s = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    encode = ""  # empty encoded string
    shift = 0    # remainder of the binary number when make 6 byte of 8 byte
    for i in xrange(len(s)):
        if shift == 0:  # first step, 6 numbers from binary ASCII number from the left
            encode += b64s[ord(s[i]) >> 2]  # encode
            shift = 2   # remainder 2 digits from the right
        elif shift == 6:  # penultimate step for iteration
            encode += b64s[ord(s[i - 1])]
            encode += b64s[ord(s[i]) >> 2]  # again first step
            shift = 2
        else:
            index1 = ord(s[i - 1]) & (2 ** shift - 1)  # make shift from the right of first binary number
            index2 = ord(s[i]) >> (shift + 2)  # binary ASCII number of the next char
            index = (index1 << (6 - shift)) | index2  # next 6 digits from
            encode += b64s[index]  # encode
            shift += 2
    if shift != 0:  # last encode step
        encode += b64s[(ord(s[len(s) - 1]) & (2 ** shift - 1)) << (6 - shift)]  # remainder of binary add to encode alg
    if len(encode) % 4:
        for i in xrange(4 - len(encode) % 4):  # add '=' while encoded string multiply of 4
            encode += '='
    return encode

class YAUS_t(Base):    # make db
    __tablename__ = 'yaus_t'   # name of table
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String)
    short_url = Column(String)

    def __init__(self, url, short_url):
        self.url = url
        self.short_url = short_url


Base.metadata.create_all(engine)    # create!
