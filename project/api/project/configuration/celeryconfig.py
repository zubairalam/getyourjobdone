import djcelery

djcelery.setup_loader()

BROKER_URL = "redis://vagrant:vagrant@localhost:6379/0"
# CELERY_IGNORE_RESULT = True
# CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_TIMEZONE = "Europe/London"
CELERY_ENABLE_UTC = True

# store AsyncResult in redis
CELERY_RESULT_BACKEND = "redis"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_USER = "vagrant"
REDIS_PASSWORD = "vagrant"
# REDIS_CONNECT_RETRY = True