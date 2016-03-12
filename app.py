import tornado
import rethinkdb as r

import tornado.ioloop
import tornado.web
from tornado.web import asynchronous
import time
class MainHandler(tornado.web.RequestHandler):
    @asynchronous
    def get(self):
        for i in range(10):
            time.sleep(1)
            self.write(str(i))
            self.flush()
        self.finish()

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
