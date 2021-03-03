import tornado.ioloop
import tornado.web
from app_config import settings
from routes.route import route
# from routes.api import route_api

if __name__ == "__main__":
    # app = tornado.web.Application(route_api, **settings)
    app = tornado.web.Application(route, **settings)

    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()