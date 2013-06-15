from flask import Flask
import redis
import plivo
import os

# Configuring Flask Application
app = Flask(__name__)
app.config.from_object("core.settings")

# Configuring redis
redis_url = os.getenv('REDISTOGO_URL', app.config["APPLICATION_REDIS_URI"])
r = redis.from_url(redis_url)

# Configuring plivo
p = plivo.RestAPI(app.config["PLIVO_AUTH_ID"], app.config["PLIVO_AUTH_TOKEN"])


__import__("core.views")
