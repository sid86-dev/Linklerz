from app import app
from app.modules import *
from app.db import *
from app.builder import *

# Auth
from Auth.facebook import *
from Auth.twilio_ import *
from Auth.google import *
from Auth.redis_ import *


# index route
@app.route('/')
def index():
    return render_template('index.html')


# error handler route
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


# setting route


@app.route('/settings/<string:username>')
def settings(username):
    if ('user' in session and session['user'] == username):
        return render_template('settings.html', username=username)
    else:
        return render_template('404.html')


# home route
@app.route('/home/<string:username>')
def home(username):
    if ('user' in session and session['user'] == username):
        credentials = Users.query.filter_by(username=username).first()
        # credentials = get_credentials(username)
        linktype = credentials.linktype
        list_linktype = get_linktype(linktype)
        return render_template('home.html', list_linktype=list_linktype, credentials=credentials)
    return redirect('/login')


# edit route
@app.route('/edit/<string:username>')
def edit(username):
    if ('user' in session and session['user'] == username):
        credentials = Users.query.filter_by(username=username).first()
        linktype = credentials.linktype
        linkurl = credentials.linkurl
        list_linktype = get_linktype(linktype)
        list_linkurl = get_linktype(linkurl)

        linkdic = {}
        for key in list_linktype:
            for value in list_linkurl:
                linkdic[key] = value
                list_linkurl.remove(value)
                break

        plan = credentials.plan
        if plan == "free":
            num = 5 - len(list_linktype)
        else:
            num = 10 - len(list_linktype)
        return render_template('edit.html', linkdic=linkdic, num=num, credentials=credentials)
    return redirect('/login')


# profile route
@app.route("/profile/<string:username>", methods=['GET', 'POST'])
def profile(username):
    error = ''
    if request.method == "POST":
        get_username = request.form.get('username')
        get_auth1 = request.form.get('auth_switch_on')
        get_auth2 = request.form.get('auth_switch_off')

        print(get_auth1)
        print(get_auth2)

        credentials = Users.query.filter_by(username=username).first()

        # auth on/off
        auth_update = credentials.auth

        if auth_update == 'yes':
            if get_auth1 == 'open_to_close':
                a = 'd'
            else:
                credentials.auth = 'no'
                print(credentials.auth)
                db.session.commit()

        elif auth_update == 'no':
            if get_auth2 == 'close_to_open':
                credentials.auth = 'yes'
                print(credentials.auth)
                db.session.commit()
            else:
                a = 'd'

        # credentials = Users.query.filter_by(username=get_username).first()
        # credentials.auth = get_auth
        # db.session.commit()

        try:
            if get_username == username:
                return redirect(f'/home/{get_username}')
            credentials = Users.query.filter_by(username=get_username).first()
            # to verify
            email = credentials.email

            # return to the same route with error
            credentials = Users.query.filter_by(username=username).first()
            error = 'Username already exist'
            return render_template('profile.html', credentials=credentials, error=error)
        except:


            # print(credentials)
            credentials.username = get_username

            db.session.commit()
            # handle log info
            session.pop('user')
            session['user'] = get_username
            return redirect(f'/home/{get_username}')

    try:
        if ('user' in session and session['user'] == username):
            credentials = Users.query.filter_by(username=username).first()
            return render_template('profile.html', credentials=credentials, error=error)
    except:
        return redirect('/login')


# saving data


@app.route('/save', methods=['GET', 'POST'])
def save():
    if request.method == "POST":
        username = session['user']
        if ('user' in session and session['user'] == username):
            credentials = Users.query.filter_by(username=username).first()
            linktype = credentials.linktype
            list_linktype = get_linktype(linktype)
            # print(list_linktype)
            # get old edited inklist
            oldlist_linktype = []
            oldlist_linkurl = []
            for item in list_linktype:
                old_linktype = request.form.get(f'{item}type', '')
                old_linkurl = request.form.get(item, '')
                if old_linktype != '' and old_linkurl != '':
                    oldlist_linktype.append(old_linktype)
                    oldlist_linkurl.append(old_linkurl)

            # get new edited inklist
            new_linktype = request.form.get(f'new_linktype', '')
            new_linkurl = request.form.get(f'new_linkurl', '')

            if new_linktype != "" and new_linkurl != "":
                oldlist_linktype.append(new_linktype)
                oldlist_linkurl.append(new_linkurl)

            x = ">".join(oldlist_linktype)
            y = ">".join(oldlist_linkurl)

            credentials.linktype = x
            credentials.linkurl = y

            db.session.commit()
            return redirect(f'/home/{username}')


# delete route


@app.route('/delete/<link_name>')
def delete(link_name):
    username = session['user']
    if ('user' in session and session['user'] == username):
        credentials = Users.query.filter_by(username=username).first()
        linktype = credentials.linktype
        linkurl = credentials.linkurl
        list_linktype = get_linktype(linktype)
        list_linkurl = get_linktype(linkurl)
        # get index and delete with the index
        index = list_linktype.index(link_name)
        list_linktype.remove(link_name)
        list_linkurl.remove(list_linkurl[index])

        x = ">".join(list_linktype)
        y = ">".join(list_linkurl)

        credentials.linktype = x
        credentials.linkurl = y

        db.session.commit()
        return redirect(f'/edit/{username}')
    return redirect(f'/edit/{username}')


@app.route('/auth_verify/<string:userid>/<string:authid>', methods=['POST'])
def verify_otp(userid, authid):
    if request.method == 'POST':
        otp = ""
        for i in range(4):
            get_otp1 = request.form.get(f'otpinput{i + 1}')
            otp += get_otp1

        code = get_cache(authid[:5])
        print(code)

        try:
            if int(code.decode('ascii')) == int(otp):
                credentials = Users.query.filter_by(userid=userid).first()
                username = credentials.username
                session['user'] = username

                return redirect(f"/home/{username}")


            elif code == 'Code Expired':
                return redirect('/login')

        except:
            return redirect('/login')


# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    auth = "no"

    args_authid = request.args.get('auth')
    args_userid = request.args.get('userid')
    args_phone = request.args.get('phone')
    phone = args_phone
    userid = args_userid

    try:
        get_user_id = get_userid(args_authid)
        # print(get_user_id)
        if get_user_id.decode('ascii') == args_userid:
            auth = 'yes'
    except:
        auth = 'no'

    authorization_url, state = flow.authorization_url()
    session['state'] = state
    try:
        username = session['user']
        if ('user' in session and session['user'] == username):
            return redirect(f'/home/{username}')
    except:
        login_fail = ""
        login_type = "Member"
        if request.method == 'POST':
            username_get = request.form.get('username').lower()
            # if '.com' in username_get:
            # username_get = username_get.lower()
            userpass_get = request.form.get('password')
            userpass_encrypt = encrypt(userpass_get)
            try:
                if '@' in username_get:
                    credentials = Users.query.filter_by(
                        email=username_get).first()
                    password = credentials.password
                    if password == 'google_auth':
                        login_fail = "Please sign in using Google"
                        return render_template('login.html', login_fail=login_fail, login_type=login_type,
                                               authorization_url=authorization_url, auth=auth, phone=phone,
                                               args_authid=args_authid, userid=userid)

                    elif password == userpass_encrypt:
                        if credentials.auth == 'no':
                            session['user'] = credentials.username
                            return redirect(f'/home/{credentials.username}')
                        elif credentials.auth == 'yes':
                            auth = 'yes'
                            phone = credentials.phone
                            userid = credentials.userid
                            authid = verify_user(userid, phone)
                            return redirect(f"/login?auth={authid}&userid={userid}&phone={phone}")


                    else:
                        login_fail = "Username and Password do not match"
                        return render_template('login.html', login_fail=login_fail, login_type=login_type,
                                               authorization_url=authorization_url, auth=auth, phone=phone,
                                               args_authid=args_authid, userid=userid)

                elif '@' not in username_get:
                    credentials = Users.query.filter_by(
                        username=username_get).first()
                    if credentials.password == userpass_encrypt:
                        # set the session variable
                        if credentials.auth == 'no':
                            session['user'] = credentials.username
                            return redirect(f'/home/{credentials.username}')
                        elif credentials.auth == 'yes':
                            auth = 'yes'
                            phone = credentials.phone
                            userid = credentials.userid
                            authid = verify_user(userid, phone)
                            return redirect(f"/login?auth={authid}&userid={userid}&phone={phone}")


                    else:
                        login_fail = "Username and Password do not match"
                        return render_template('login.html', login_fail=login_fail, login_type=login_type,
                                               authorization_url=authorization_url, auth=auth, phone=phone,
                                               args_authid=args_authid, userid=userid)
            except:
                login_fail = "Username and Password do not match"
                return render_template('login.html', login_fail=login_fail, login_type=login_type,
                                       authorization_url=authorization_url, auth=auth, phone=phone,
                                       args_authid=args_authid, userid=userid)
        return render_template('login.html', login_fail=login_fail, login_type=login_type,
                               authorization_url=authorization_url, auth=auth, phone=phone, args_authid=args_authid,
                               userid=userid)


# facebook Auth
@app.route('/facebook/')
def facebook():
    # Facebook Oauth Config
    FACEBOOK_CLIENT_ID = params['facebook_client_id']
    FACEBOOK_CLIENT_SECRET = params['facebook_client_secret']
    oauth.register(
        name='facebook',
        client_id=FACEBOOK_CLIENT_ID,
        client_secret=FACEBOOK_CLIENT_SECRET,
        access_token_url='https://graph.facebook.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://www.facebook.com/dialog/oauth',
        authorize_params=None,
        api_base_url='https://graph.facebook.com/',
        client_kwargs={'scope': 'email'},
    )
    redirect_uri = url_for('facebook_auth', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)


@app.route('/facebook/Auth/')
def facebook_auth():
    token = oauth.facebook.authorize_access_token()
    resp = oauth.facebook.get('https://graph.facebook.com/me?fields=id,name,email,picture{url}')
    profile = resp.json()
    email = profile['email']
    name = profile['name']

    try:
        username = login_with_facebook(email)
        return redirect(f'/home/{username}')

    except:
        signup_with_facebook(email, name)
        return redirect(f'/datapolicy/{email}')


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(
        session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    try:
        username = login_with_google(id_info)
        return redirect(f'/home/{username}')
    except:
        email = signup_with_google(id_info)
        return redirect(f'/datapolicy/{email}')


@app.route('/datapolicy/<string:email>', methods=['GET', 'POST'])
def datapolicy(email):
    if request.method == "POST":
        return render_template('confirm.html', email_address=email)
    arg = ''
    credentials = {'username': 'Data Policy', 'email': email}
    return render_template('data_policy.html', credentials=credentials, arg=arg)


# signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    user_exist = "NO"
    if request.method == 'POST':
        useremail_get = request.form.get('email').lower()
        userpass_get = request.form.get('password')
        confirmpass_get = request.form.get('password_confirm')
        full_name = request.form.get('username').lower()
        num = random.randint(11, 500)
        username_get = f"{full_name[:4]}{full_name[-3:]}{num}"
        try:
            credentials = Users.query.filter_by(username=username_get).first()
            username = credentials.username
            user_exist = "YES"
            return render_template('signup.html', user_exist=user_exist, authorization_url=authorization_url)
        except:
            user_exist = "NO"
            if userpass_get == confirmpass_get:
                try:
                    credentials = Users.query.filter_by(
                        email=useremail_get).first()
                    useremail = credentials.email
                    email_exist = "yes"
                    return render_template('signup.html', user_exist=user_exist, email_exist=email_exist,
                                           authorization_url=authorization_url)
                except:
                    userpass_encrypt = encrypt(userpass_get)
                    session['user'] = username_get

                    token = gen_token(useremail_get)
                    final_token = f"https://lerz.herokuapp.com/confirm/{token}"
                    # entry to database
                    threading.Thread(target=entry, args=(
                        username_get, userpass_encrypt, useremail_get), name='thread_function').start()

                    # send confirmation email
                    threading.Thread(target=send_email, args=(
                        useremail_get, username_get, final_token), name='thread_function').start()

                    return render_template('confirm.html', email_address=useremail_get)
            else:
                match = "NO"
                return render_template('signup.html', user_exist=user_exist, match=match,
                                       authorization_url=authorization_url)
    return render_template('signup.html', user_exist=user_exist, authorization_url=authorization_url)


# email send
@app.route('/sendconfirm/<string:email>')
def emailconfirm(email):
    try:
        username = session['user']
        token = gen_token(email)
        final_token = f"https://lerz.herokuapp.com/confirm/{token}"

        send_email(email, username, final_token)
        return render_template('confirm.html', email_address=email)
    except:
        return redirect('/error')


@app.route('/confirm/<string:token>')
def confirm_email(token):
    email = s.loads(token, salt='email-confirm', max_age=172800)
    # data process
    credentials = Users.query.filter_by(email=email).first()
    credentials.confirmation = "yes"
    db.session.commit()
    return render_template('confirm_email.html', credentials=credentials)


# delete account


@app.route('/deletelog/<string:email>/<string:username>')
def delete_account(email, username):
    if ('user' in session and session['user'] == username):
        keyword = gen_word()
        word = f"{username}{keyword}"
        # credentials = Users.query.filter_by(username=username).first()
        return render_template('delete.html', username=username, word=word, email=email)


def delete_data(username):
    credentials = Users.query.filter_by(username=username).first()
    # delete data
    # email = credentials.email
    db.session.delete(credentials)
    db.session.commit()
    # return email


@app.route('/deletecheck/<string:username>/<string:word>/<string:email>', methods=['GET', 'POST'])
def delete_check(username, word, email):
    if request.method == "POST":
        inputtext = request.form.get('inputtext')
        if inputtext != word:
            return redirect(f'/deletelog/{username}')
        else:
            # query to database
            threading.Thread(target=delete_data, args=(
                username,), name='thread_function').start()

            # send delete email
            threading.Thread(target=delete_email, args=(
                email, username,), name='thread_function').start()

            return redirect('/logout')
    return redirect('/login')


# Logging out


@app.route('/logout')
def logout():
    try:
        session.pop('user')
        return redirect('/login')
    except:
        return render_template('404.html')


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    login_fail = ""
    login_type = "Admin"
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == params['admin_username'] and password == params['admin_password']:
            session['admin_user'] = params['admin_username']
            return redirect('/admin_dashboard')
        login_fail = "Username and Password do not match"
    try:
        return render_template('login.html', login_fail=login_fail, login_type=login_type)
    except:
        return render_template('404.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    try:
        if session['admin_user'] == params['admin_username']:
            credentials = Users.query.filter_by().all()
            return render_template('admin_dashboard.html', credentials=credentials)
    except:
        return redirect('/admin')


# render links


@app.route(
    '/li.<string:username>')
def link(username):
    credentials = Users.query.filter_by(username=username).first()
    linktype = credentials.linktype
    linkurl = credentials.linkurl
    list_linktype = get_linktype(linktype)
    list_linkurl = get_linktype(linkurl)
    theme = credentials.theme

    linkdic = {}
    for key in list_linktype:
        for value in list_linkurl:
            linkdic[key] = value
            list_linkurl.remove(value)
            break
    # return render_template('dark_theme.html', credentials=credentials, linkdic=linkdic)
    return render_template(f'{params[credentials.theme]}.html', credentials=credentials, linkdic=linkdic)


@app.route('/appearance/<string:username>', methods=['GET', 'POST'])
def appearance(username):
    if ('user' in session and session['user'] == username):
        credentials = Users.query.filter_by(username=username).first()
        if request.method == 'POST':
            theme = request.form.get('slider')
            # print((theme).upper())
            credentials.theme = theme
            db.session.commit()
            return redirect(f'/home/{{credentials.username}}')
        return render_template('appearance.html', credentials=credentials)
    else:
        return redirect('/login')


# @app.route('/bug')
# def bug():
#     credentials = Users.query.filter_by(username='sid86_').first()
#     password = encrypt(password='Siddharth8604')
#     credentials.password = password
#     db.session.commit()
#     return 'Done'


# api for linklerz.li
@app.route(
    '/api/<string:username>')
def api(username):
    try:
        credentials = Users.query.filter_by(username=username).first()
        linktype = credentials.linktype
        linkurl = credentials.linkurl
        list_linktype = get_linktype(linktype)
        list_linkurl = get_linktype(linkurl)

        linkdic = {}
        for key in list_linktype:
            for value in list_linkurl:
                linkdic[key] = value
                list_linkurl.remove(value)
                break
        arr = jsonify(api_conv(linkdic)
        return {'links': arr}
    except:
        return jsonify(username='Does not exist')


@app.route('/community')
def community():
    return render_template('community_select.html')


@app.route('/recovery', methods=['GET', 'POST'])
def recovery():
    fixed_credentials = {'username': 'Help Center'}
    arg = ''
    if request.method == 'POST':
        recoveryinput = request.form.get('recoveryinput')
        print(recoveryinput)
        try:
            if '@' in recoveryinput:
                credentials = Users.query.filter_by(
                    email=recoveryinput).first()
                email = credentials.email
                username = credentials.username
            else:
                credentials = get_credentials(recoveryinput)
                email = credentials.email
                username = credentials.username
            arg = 'success'
            delete_email(email, username)
            return render_template('recovery.html', credentials=fixed_credentials, arg=arg)
        except:
            arg = 'Username or Email does not exist'
            return render_template('recovery.html', credentials=fixed_credentials, arg=arg)
    return render_template('recovery.html', credentials=fixed_credentials, arg=arg)
