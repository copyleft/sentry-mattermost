# sentry-mattermost

Send notifications to Mattermost via webhooks. **Supports Sentry 20.9.0**

## Install
1. Add `https://github.com/copyleft/sentry-mattermost/archive/master.zip` to your `requirements.txt` file
2. Rebuild your docker image (ex.: `docker-compose up -d --build`)
3. The plugin should now be listed under legacy integrations / Integrations under Alerts settings.