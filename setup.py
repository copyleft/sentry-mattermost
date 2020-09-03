from setuptools import setup

setup(
    name="sentry-mattermost",
    version="1.0.0",
    author="Copyleft Solutions",
    description="A Sentry plugin to send Mattermost notifications via webhooks.",
    license="MIT",
    keywords="sentry mattermost",
    packages=['sentry_mattermost'],
    entry_points={
        'sentry.plugins': [
            'mattermost = sentry_mattermost.plugin:MattermostPlugin'
        ],
    },
)
