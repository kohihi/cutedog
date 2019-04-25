from .development import Development
from .production import Production

settings = dict(
    dev=Development,
    pro=Production,
)