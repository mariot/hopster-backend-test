import os

import jinja2
import webapp2

from google.appengine.api import users


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            username = user.nickname()
            greetings = 'Glad to see you back, '
            log_url = users.create_logout_url(self.request.uri)
            log_url_linktext = 'Sign out'
        else:
            username = 'Friend'
            greetings = 'Welcome to our World, '
            log_url = users.create_login_url(self.request.uri)
            log_url_linktext = 'Sign in'

        template_values = {
            'user': user,
            'username': username,
            'greetings': greetings,
            'log_url': log_url,
            'log_url_linktext': log_url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('client/index.html')
        self.response.write(template.render(template_values))


class AddSuggestion(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = JINJA_ENVIRONMENT.get_template('client/add_suggestion.html')
        if user:
            username = user.nickname()
            log_url = users.create_logout_url(self.request.uri)
            log_url_linktext = 'Sign out'
            template_values = {
                'user': user,
                'username': username,
                'log_url': log_url,
                'log_url_linktext': log_url_linktext,
            }

            self.response.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/add_suggestion', AddSuggestion),
], debug=True)
