import string, random
import sys
import sqlite3 as lite

#conn = sqlite3.connect('first_database.db')
#cursor = conn.cursor()
url = 'https://stackoverflow.com/'

def url_gen():
    data = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(data) for key in range(5))
    return short_url
'''
for i in xrange(10):

    short_url = url_gen()
    cursor.execute("INSERT INTO YAUS (URL, SHORT_URL) VALUES ('%s', '%s');" % (url, short_url))

'''

try:
    con = lite.connect('first_database.db')
    short_url = url_gen()
    cur = con.cursor()

    #cur.executescript("INSERT INTO Cars(Name, Price) VALUES('%s', '%s');" % (url, short_url))
    #cur.execute("SELECT * FROM Cars")
    cur.execute("SELECT Price FROM Cars WHERE NAME =?", [url])
    con.commit()
    print(cur.fetchall())
except lite.Error, e:

    if con:
        con.rollback()

    print "Error %s:" % e.args[0]
    sys.exit(1)

finally:

    if con:
        con.close()



