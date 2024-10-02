INSTALLED_APPS = [
    # другие приложения
    'debug_toolbar',
]

MIDDLEWARE = [
    # другие middleware
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]