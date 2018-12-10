import cherrypy
import os
import simplejson

STATIC_DIR = os.path.join(os.path.abspath("."), u"static")

class AjaxApp(object):
    @cherrypy.expose
    def index(self):
        return open(os.path.join(STATIC_DIR, u'index.html'))

    @cherrypy.expose
    def submit(self, name):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        format = cherrypy.config.get('greeting.format')
        return simplejson.dumps({'title': format.format(name)})
        # return simplejson.dumps({'title': "Hello, %s" % name})

cherrypy.config.update("service.conf")
config = {'/static': {
    'tools.staticdir.on' : True,
    'tools.staticdir.dir' : STATIC_DIR
}}
cherrypy.tree.mount(AjaxApp(), '/', config=config)
cherrypy.engine.signals.subscribe()
cherrypy.engine.start()
cherrypy.engine.block()
