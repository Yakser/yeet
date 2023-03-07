from examples.controllers import HomeController, ProfileController
from yeet.app import Yeet

app = Yeet()

app.add_route('^home/(.*)$', HomeController())
app.add_route('^home/profile(.*)$', ProfileController())

if __name__ == '__main__':
    app.run(host='', port=8080)
