from __future__ import absolute_import

from sentry_plugins.client import ApiClient


class MattermostApiClient(ApiClient):
    allow_redirects = False
    plugin_name = "mattermost"

    def __init__(self, webhook, username, icon_url, channel):
        self.webhook = webhook
        self.username = username
        self.icon_url = icon_url
        self.channel = channel

        super(MattermostApiClient, self).__init__()

    def request(self, data):
        return self._request(
            path=self.webhook,
            method="post",
            data=data,
            json=False,
            allow_text=True
        )

