from motor.motor_asyncio import AsyncIOMotorClient
from umongo import Document, fields, Instance
from config import MONGO_DB_URI, DATABASE_NAME

# Connect to MongoDB
client = AsyncIOMotorClient(MONGO_DB_URI)
db = client[DATABASE_NAME]

# Init Umongo instance
instance = Instance(db)

@instance.register
class Media(Document):
    file_id = fields.StringField(required=True)
    file_unique_id = fields.StringField(required=True)
    title = fields.StringField()
    size = fields.StringField()
    mime_type = fields.StringField()
    caption = fields.StringField()
    chat_id = fields.IntegerField()
    message_id = fields.IntegerField()

    class Meta:
        collection = "media"
