from yeet.app import Yeet
from yeet.templating import render_template

app = Yeet()


@app.route('/')
def home():
    return render_template('base.html')


if __name__ == '__main__':
    app.run(host='', port=8080)
