from flask import Flask, request, render_template, redirect, url_for
import string,random
from urlparse import urlparse
import sqlite3


def url_gen():
    data = string.ascii_lowercase + string.digits
    short_url = ''.join(random.choice(data) for key in range(5))
    return short_url

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])

def home():
    if request.method == 'POST':
        conn = sqlite3.connect('first_database.db')
        cursor = conn.cursor()
        user_url = str(request.form.get('url'))
        if urlparse(user_url).scheme == '':
            user_url = 'http://' + user_url
        short_url = url_gen()
        cursor.execute("SELECT ID FROM YAUS WHERE URL =?", [user_url])
        data_ex = cursor.fetchone()
        if data_ex == None :
            cursor.execute("INSERT INTO YAUS (URL, SHORT_URL) VALUES ('%s', '%s')" % (user_url, short_url))
        else:
            cursor.execute("SELECT SHORT_URL FROM YAUS WHERE ID =?", [data_ex[0]])
            short_url = cursor.fetchone()
        conn.commit()
        conn.close()
        short_url_link = 'localhost:5000/%s' % short_url
        return redirect(url_for('shortened', url=short_url_link))
    else:
        return render_template('home.html')

@app.route('/shortened/')
def shortened():
    url = request.args.get('url')
    return render_template('shortened.html', url=url)

@app.route('/<short_url>/')
def redirect_url(short_url):
    conn = sqlite3.connect('first_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT URL FROM YAUS WHERE SHORT_URL =?", [short_url])
    short_url_link = cursor.fetchone()
    conn.close()
    if short_url_link != None:
        return redirect(short_url_link[0])
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
