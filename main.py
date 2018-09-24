from config_yaus import *
from func import gnb64


@app.route('/', methods=['GET', 'POST'])
def home():
    '''
    Main page. Get URL from user, validate it for include http part and compare with existing URLs in database.
    If URL already in database return existing short link, else generate new and add new row in database.
    :return: If users's URL not empty -- redirect to new page with shorten URL.
    '''
    if request.method == 'POST':
        user_url = str(request.form.get('url'))
        if user_url:  # check for empty string
            if not urlparse(user_url).scheme:   # check http part
                user_url = 'http://' + user_url
            ex_id = session.query(YAUS_t.id).filter_by(url=user_url).scalar()   # is the same URL already exist in db?
            if not ex_id:  # if URL is new
                try:
                    last_id = session.query(YAUS_t.id).order_by(YAUS_t.id.desc()).first() # get last row id
                    real_id = last_id[0] + 1     # id of current new URL
                except TypeError:
                    real_id = 1   # table is empty, this is the first URL in db
                short_url = str(gnb64(str(real_id)))  # encode id with base64 algoritm
                session.add(YAUS_t(user_url, short_url))    # add both URLs in db
            else:
                short_url = session.query(YAUS_t.short_url).filter_by(id=ex_id).scalar() # URL already exist in db
            session.commit()
            short_url_link = '127.0.0.1:5000/%s' % short_url    # make link to redirect
            return redirect(url_for('shortened', url=short_url_link))   # redirect to shortened page
        else:
            return render_template('home.html')  # empty user's URL
    else:
        return render_template('home.html')  # wrong request method


@app.route('/shortened/')
def shortened():
    '''
    Page with shorten URL.
    :return: Shorten URL with link to users page
    '''
    url = request.args.get('url')
    return render_template('shortened.html', url=url)  # add short url to html page


@app.route('/<short_url>/')
def redirect_url(short_url):
    '''
    :param short_url: generated short URL
    :return: redirected to user page
    '''
    short_url_link = session.query(YAUS_t.url).filter_by(short_url=short_url).scalar() #get user's URL from db with short one
    if short_url_link is not None:
        return redirect(short_url_link)  # redirect to url
    return redirect(url_for('home'))    # redirect to home page if short_url doesn't exist in db


if __name__ == '__main__':
    app.run()   # run the program
