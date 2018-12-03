from app import app

@app.route('/')
@app.route('/index')
def hello():
    return 'Hey, dude!'


@app.route('/exchange')
def get_exchange():
    pass

## and go on
