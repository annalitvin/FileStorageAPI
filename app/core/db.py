from databases import Database

from core.config import settings

database = Database(settings.async_database_url, min_size=5, max_size=20)
