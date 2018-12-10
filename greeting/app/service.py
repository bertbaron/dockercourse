import cherrypy
import os
import simplejson
import time

STATIC_DIR = os.path.join(os.path.abspath("."), u"static")

cache = None
# Next two lines are to be enabled in assignment 5:
#import redis
#cache = redis.Redis(host='redis', port=6379)

# with redis enabled, this will store the hit count in the cache
def getHitCount():
    if not cache:
        return

    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

class AjaxApp(object):
    @cherrypy.expose
    def index(self):
        return open(os.path.join(STATIC_DIR, u'index.html'))

    @cherrypy.expose
    def submit(self, name):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        format = cherrypy.config.get('greeting.format')
        return simplejson.dumps({'title': format.format(name), 'hits':getHitCount()})

cherrypy.config.update("service.conf")
config = {'/static': {
    'tools.staticdir.on' : True,
    'tools.staticdir.dir' : STATIC_DIR
}}
cherrypy.tree.mount(AjaxApp(), '/', config=config)
cherrypy.engine.signals.subscribe()
cherrypy.engine.start()
cherrypy.engine.block()
