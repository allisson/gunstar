# -*- coding: utf-8 -*-

def index(req, res):
    res.render_template('index.html', name='Gunstar')
    return res

def other(req, res, name):
    res.render_template('index.html', name=name)
    return res