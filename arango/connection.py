from pyArango.connection import Connection

conn = Connection(username="root", password="root")
db_name = "logistics"
if not conn.databases.get(db_name, None):
    db = conn.createDatabase(name="logistics")

db_conn = conn[db_name]


if not db_conn.hasCollection("provider"):
    db_conn.createCollection(name="provider")
    # pc = db_conn.createDocument()
    """
    Name, Email, Phone Number, Language, Currency
    # name, email, mobile, language, currency
    """
if not db_conn.hasCollection("service_area"):
    db_conn.createCollection(name="service_area")
    """
    provider id, geojson polygons, polygon name, price
    """
