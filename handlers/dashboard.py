import json
import redis
import tornado
import tornado.escape
import tornado.web
from tornado.escape import json_encode
from tornado import gen
import settings

import logging
logger = logging.getLogger('monitor.' + __name__)


class DashboardHandler(tornado.web.RequestHandler):
    template = "memory_stat.html"

    def initialize(self, template=template):
        self.template = template

    @gen.coroutine
    def get(self):
        kwargs = dict()
        super(DashboardHandler, self).render(self.template, **kwargs)


class ServerStatHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def get(self):
        r = redis.Redis(connection_pool=settings.REDIS_POOL)
        mem_key = "sg:monitor:animal:mem"
        mem_stat = r.zrange(mem_key, 0, -1) or []
        mem_stat = [eval(item) for item in mem_stat]
        print mem_stat

        http_key = "sg:monitor:animal:http"
        http_stat = r.zrange(http_key, 0, -1) or []
        http_stat = [json.loads(item) for item in http_stat]
        print http_stat

        kwargs = dict(mem_stat=mem_stat, http_stat=http_stat)
        self.render(None, data=kwargs)

    def render(self, template_name, **kwargs):
        self.write(json_encode(kwargs["data"]))
