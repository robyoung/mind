import os

from mind.app import create_app

app = create_app(os.environ.get('ENVIRONMENT', 'prod'))

from mind import commands  # noqa: F401, E402
