# -*- coding: utf-8 -*-
from itsdangerous import URLSafeTimedSerializer, BadSignature


class Session(object):

    salt = 'cookie-session'
    
    def __init__(self, app, request, response):
        self.app = app
        self.request = request
        self.response = response
        self.modified = False
        self.cleared = False
        self.secret_key = self.app.config.get('SECRET_KEY')
        self.session_cookie_name = self.app.config.get('SESSION_COOKIE_NAME')
        self.session_cookie_domain = self.app.config.get('SESSION_COOKIE_DOMAIN')
        self.session_cookie_path = self.app.config.get('SESSION_COOKIE_PATH')
        self.session_cookie_httponly = self.app.config.get('SESSION_COOKIE_HTTPONLY')
        self.session_cookie_secure = self.app.config.get('SESSION_COOKIE_SECURE')
        self.max_age = self.app.config.get('PERMANENT_SESSION_LIFETIME')
        self.data = {}

        # init session
        self.get_session()

    def get_max_age(self):
        return self.max_age.seconds + (self.max_age.days * 24 * 3600)

    def get_cookie_domain(self):
        cookie_domain = self.session_cookie_domain
        if not cookie_domain:
            cookie_domain = self.request.host.rsplit(':', 1)[0]
        return cookie_domain

    def get_serializer(self):
        return URLSafeTimedSerializer(self.secret_key, salt=self.salt)

    def get_session(self):
        if not self.secret_key:
            return
        
        s = self.get_serializer()
        cookie_value = self.request.cookies.get(self.session_cookie_name)
        
        if not cookie_value:
            return
        
        try:
            self.data = s.loads(cookie_value, max_age=self.get_max_age())
        except BadSignature:
            return

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.modified = True

    def delete(self, key):
        self.data.pop(key, None)
        self.modified = True

    def clear(self):
        self.data.clear()
        self.cleared = True

    def save(self):
        if not self.secret_key:
            return

        if self.cleared:
            self.response.delete_cookie(
                self.session_cookie_name,
                path=self.session_cookie_path,
                domain=self.get_cookie_domain()
            )

        if self.modified:
            s = self.get_serializer()
            cookie_value = s.dumps(dict(self.data))
            self.response.set_cookie(
                self.session_cookie_name,
                cookie_value,
                max_age=self.max_age,
                path=self.session_cookie_path,
                domain=self.get_cookie_domain(),
                secure=self.session_cookie_secure,
                httponly=self.session_cookie_httponly
            )
        return
