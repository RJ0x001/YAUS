from config_yaus import *


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_url = str(request.form.get('url'))
        if urlparse(user_url).scheme == '':
            user_url = 'http://' + user_url
        ex_id = session.query(YAUS_t.id).filter_by(url=user_url).scalar()
        if ex_id is None:
            try:
                last_id = session.query(YAUS_t.id).order_by(YAUS_t.id.desc()).first()
                real_id = last_id[0] + 1
            except TypeError:
                real_id = 1
            id_work = str(real_id).encode('ascii')
            short_url = str(base64.b64encode(id_work)).rstrip("=")
            session.add(YAUS_t(user_url, short_url))
        else:
            short_url = session.query(YAUS_t.short_url).filter_by(id=ex_id).scalar()
        session.commit()
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
    short_url_link = session.query(YAUS_t.url).filter_by(short_url=short_url).scalar()
    if short_url_link is not None:
        return redirect(short_url_link)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
