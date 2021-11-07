from flask_oauth import OAuth

oauth = OAuth()
the_remote_app = oauth.remote_app('the remote app',
    ...
)