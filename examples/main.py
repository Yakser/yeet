import os

from controllers import HomeController, ProfileController
from python_yeet.app import Yeet

if __name__ == '__main__':
    app = Yeet(name=os.path.basename(os.getcwd()))

    app.add_route('^home/profile(.*)$', ProfileController)
    app.add_route('^home/(.*)$', HomeController)

    app.run(host='', port=8080)
