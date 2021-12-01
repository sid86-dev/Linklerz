from app import settings

def login_with_google(info):
    email = info['email']
    credentials = Users.query.filter_by(email=email).first()
    username = credentials.username
    session['user'] = username
    return username


def signup_with_google(info):
    email = info['email'].lower()
    f_name = info['given_name'].lower()
    l_name = info['family_name'].lower()

    num = random.randint(11, 500)
    username = f"{f_name[:4]}{l_name}{num}"

    token = gen_token(email)
    final_token = f"https://lerz.herokuapp.com/confirm/{token}"
    # entry to database
    threading.Thread(target=entry, args=(
        username, "google_auth", email), name='thread_function').start()

    # send confirmation email
    threading.Thread(target=send_email, args=(
        email, username, final_token), name='thread_function').start()
    # add username session variable
    session['user'] = username

    return email