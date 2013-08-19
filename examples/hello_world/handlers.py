# -*- coding: utf-8 -*-
from gunstar.http import RequestHandler


class IndexHandler(RequestHandler):
    
    def get(self):
        self.render_template('index.html')


class OtherHandler(RequestHandler):
    
    def get(self, name):
        self.render_template('index.html', name=name)
