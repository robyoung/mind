from flask import current_app
import twitter


class TwitterClient:
    def init_app(self, app):
        self._set_client(app)

    def _set_client(self, app):
        consumer_key = app.config['TWITTER_CONSUMER_KEY']
        consumer_secret = app.config['TWITTER_CONSUMER_SECRET']
        access_token_key = app.config['TWITTER_ACCESS_TOKEN']
        access_token_secret = app.config['TWITTER_ACCESS_TOKEN_SECRET']

        app.extensions.setdefault('twitter', {})
        app.extensions['twitter'][self] = twitter.Api(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_key=access_token_key,
            access_token_secret=access_token_secret)

    @property
    def client(self):
        try:
            return current_app.extensions['twitter'][self]
        except KeyError:
            raise TwitterClientError('Client not initialised')

    def __getattr__(self, name):
        return getattr(self.client, name)


class TwitterClientError(Exception):
    pass
