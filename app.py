import tornado
import rethinkdb as r

import tornado.ioloop
import tornado.web
from tornado.web import asynchronous
import time
class MainHandler(tornado.web.RequestHandler):
    def initialise(self, source):
        self.set_header('content-type', 'text/event-stream')
        self.set_header('cache-control', 'no-cache')
    @asynchronous
    def get(self):
        for i in range(10):
            time.sleep(1)
            self.write(str(i))
            self.flush()
        self.finish()
class IndexHandler(tornado.web.RequestHandler):
    s = """
    <!DOCTYPE html>
    <html>
    <head>
        <script>
            var source = new EventSource("/stream");
                source.onmessage = function(event) {
                console.log(event)
                        document.getElementById("output").innerHTML += event.data + "<br/>"
                            }
                                </script>
                                </head>
                                <body>
                                    <h1>Output</h1>
                                        <div id="output"></div>
                                        </body>
                                        </html>
    """
    def get(self):
        self.finish(self.s)

def make_app():
    return tornado.web.Application([
        (r"/stream", MainHandler),
        (r"/", IndexHandler),
        ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
