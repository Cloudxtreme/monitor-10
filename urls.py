from tornado.web import StaticFileHandler
from handlers.dashboard import DashboardHandler, ServerStatHandler


url_patterns = [
    # Favicon
    (r"/(favicon.ico)", StaticFileHandler, {"path": "/images/favicon.ico"}),

    # Auth URL configurations.
    (r"/stat/memory/?$",
     DashboardHandler,
     dict(template="memory_stat.html")),
    (r"/stat/http/?$",
     DashboardHandler,
     dict(template="http_stat.html")),
    (r"/serverstat/?$", ServerStatHandler),

]
