import dns.resolver

# Configure dnspython with public fallback nameservers
# Fixes intermittent SRV query timeouts on Linux/Fedora (systemd-resolved 127.0.0.53)
try:
    custom_resolver = dns.resolver.Resolver()
    custom_resolver.nameservers = ['8.8.8.8', '1.1.1.1', '8.8.4.4']
    dns.resolver.default_resolver = custom_resolver
except Exception:
    pass

from pymongo import MongoClient
from app.config.settings import MONGO_URI

# Use connect=False and serverSelectionTimeoutMS to prevent blocking on import
client = MongoClient(
    MONGO_URI,
    connect=False,
    serverSelectionTimeoutMS=3000
)

# Use database from URI if specified, else fallback to 'smritiroots'
try:
    db = client.get_default_database()
except Exception:
    db = client["smritiroots"]

if db is None:
    db = client["smritiroots"]