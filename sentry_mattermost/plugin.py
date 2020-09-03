from __future__ import absolute_import

from sentry.plugins.bases.notify import NotifyPlugin
from sentry.utils import json
from sentry_plugins.base import CorePluginMixin
from sentry.integrations import FeatureDescription, IntegrationFeatures

from .client import MattermostApiClient

VERSION = "1.0.0"
AUTHOR = "Copyleft Solutions"
AUTHOR_URL = "https://copyleft.no"
DESCRIPTION = """
A Sentry plugin to send Mattermost notifications via webhooks.
"""

class MattermostPlugin(CorePluginMixin, NotifyPlugin):
    author = AUTHOR
    author_url = AUTHOR_URL
    version = VERSION
    resource_links = [
        ("Report Issue", "https://github.com/copyleft/sentry-mattermost/issues"),
        ("View Source", "https://github.com/copyleft/sentry-mattermost/tree/master/sentry_mattermost"),
    ]
    description = DESCRIPTION
    slug = "mattermost"
    title = "Mattermost"
    conf_title = "Mattermost"
    conf_key = "mattermost"
    required_field = "webhook"
    feature_descriptions = [
        FeatureDescription(
            """
            A Sentry plugin to send Mattermost notifications via webhooks.
            """,
            IntegrationFeatures.ALERT_RULE,
        ),
    ]

    def is_configured(self, project):
        return bool(self.get_option("webhook", project))

    def get_config(self, **kwargs):
        return [
            {
                "name": "webhook",
                "label": "Webhook URL",
                "type": "url",
                "required": True,
                "help": "Your incomming webhook URL",
            },
            {
                "name": "username",
                "label": "Bot Name",
                "type": "string",
                "default": "Sentry",
                "required": False,
                "help": "The name of the bot when posting messages.",
            },
            {
                "name": "icon_url",
                "label": "Icon URL",
                "type": "url",
                "required": False,
                "default": "http://myovchev.github.io/sentry-slack/images/logo32.png",
                "help": (
                    "The url of the icon to appear beside your bot (32px png).<br />"
                    "You may use http://myovchev.github.io/sentry-slack/images/logo32.png"
                ),
            },
            {
                "name": "channel",
                "label": "Destination",
                "type": "string",
                "placeholder": "e.g #notifications",
                "required": False,
                "help": (
                    "Optional #channel name or @user<br /><br />"
                    "When sending to a @user, the message will be sent from the creator of the webhook"
                ),
            },
        ]

    def get_client(self, project):
        return MattermostApiClient(
            self.get_option("webhook", project).strip(),
            (self.get_option("username", project) or "Sentry").strip(),
            (self.get_option("icon_url", project) or "").strip(),
            (self.get_option("channel", project) or "").strip()
        )

    def error_message_from_json(self, data):
        errors = data.get("message")

        if errors:
            return errors
        return None
    
    def notify(self, notification, **kwargs):
        event = notification.event
        group = event.group
        project = group.project

        if not self.is_configured(project):
            return

        title = event.title.encode("utf-8")

        if group.culprit:
            culprit = group.culprit.encode("utf-8")
        else:
            culprit = None

        project_name = project.get_full_name().encode("utf-8")

        fields = [
            {
                "title": "Culprit",
                "value": culprit,
                "short": False,
            },
        ]

        payload = {
            "attachments": [
                {
                    "fallback": "[%s] %s" % (project_name, title),
                    "title": "[%s] %s" % (project_name, title),
                    "title_link": group.get_absolute_url(params={"referrer": "mattermost"}),
                    "fields": fields,
                }
            ]
        }

        client = self.get_client(project)

        if client.username:
            payload["username"] = client.username.encode("utf-8")
        
        if client.channel:
            payload["channel"] = client.channel
        
        if client.icon_url:
            payload["icon_url"] = client.icon_url
        
        client.request({"payload": json.dumps(payload)})
