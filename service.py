import endpoints
from google.appengine.ext import ndb
from google.appengine.api import users
from protorpc import messages, message_types, remote
from decorator import need_auth


class Suggestion(messages.Message):
    author = messages.StringField(1)
    title = messages.StringField(2)
    plot = messages.StringField(3)
    date = messages.StringField(4)


class SuggestionList(messages.Message):
    items = messages.MessageField(Suggestion, 1, repeated=True)


class SuggestionModel(ndb.Model):
    author = ndb.UserProperty()
    title = ndb.StringProperty()
    plot = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


@endpoints.api(name='suggestion',
               description="API for storing and accessing movie suggestions",
               version='v1')
class SuggestionAPI(remote.Service):
    @endpoints.method(Suggestion, Suggestion, name="suggestion.insert",
                      path="suggestion",
                      http_method='POST')
    def insert_suggestion(self, request):
        user = users.get_current_user()
        basic_auth = self.request_state.headers.get('authorization')

        @need_auth(basic_auth, 'insert')
        def create_suggestion(author, title, plot):
            return SuggestionModel(author=author, title=title, plot=plot)
        create_suggestion(user, request.title, request.plot).put()
        return request

    @endpoints.method(message_types.VoidMessage, SuggestionList,
                      name="suggestion.list",
                      path="suggestions",
                      http_method='GET')
    def list_suggestions(self, unused_request):
        suggestions = []
        for sugg in SuggestionModel.query():
            if sugg.author:
                author = sugg.author.nickname()
            else:
                author = 'Anonymous'
            suggestions.append(Suggestion(author=author,
                                          title=sugg.title,
                                          plot=sugg.plot))
        return SuggestionList(items=suggestions)


api = endpoints.api_server([SuggestionAPI])
