import motor.motor_asyncio
from config import Config
import time
import logging

logger = logging.getLogger("Botskingdoms")

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.blacklisted = self.db.blacklisted
        self.premium = self.db.premium
        self.settings = self.db.settings

    async def get_admins(self):
        settings = await self.settings.find_one({'id': 'admin_list'})
        if settings:
            admins = settings.get('admins', Config.Botskingdoms)
            Botskingdoms = admins
            return Botskingdoms
        admins = Config.Botskingdoms
        Botskingdoms = admins
        return Botskingdoms

    async def add_admin(self, admin_id):
        await self.settings.update_one({'id': 'admin_list'}, {'$addToSet': {'admins': int(admin_id)}}, upsert=True)

    async def remove_admin(self, admin_id):
        await self.settings.update_one({'id': 'admin_list'}, {'$pull': {'admins': int(admin_id)}})

    async def set_shortlink(self, url, api):
        await self.settings.update_one({'id': 'shortlink'}, {'$set': {'url': url, 'api': api}}, upsert=True)

    async def get_shortlink(self):
        return await self.settings.find_one({'id': 'shortlink'})

    def new_user(self, id):
        return dict(
            id=id,
            join_date=time.time(),
            thumb=None,
            caption=None,
            autorename_format=None,
            media_type="document", # document, video
            metadata_text=None,
            metadata_status=False,
            credits=10, # default credits
            is_premium=False,
            premium_expiry=0,
            rename_count=0,
            is_sequencing=False,
            sequence_files=[]
        )

    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return True if user else False

    async def get_user_data(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def set_thumb(self, id, file_id):
        await self.col.update_one({'id': int(id)}, {'$set': {'thumb': file_id}})

    async def get_thumb(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('thumb', None) if user else None

    async def set_caption(self, id, caption):
        await self.col.update_one({'id': int(id)}, {'$set': {'caption': caption}})

    async def get_caption(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('caption', None) if user else None

    async def set_autorename_format(self, id, format):
        await self.col.update_one({'id': int(id)}, {'$set': {'autorename_format': format}})

    async def get_autorename_format(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('autorename_format', None) if user else None

    async def set_media_type(self, id, media_type):
        await self.col.update_one({'id': int(id)}, {'$set': {'media_type': media_type}})

    async def get_media_type(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('media_type', 'document') if user else 'document'

    async def set_metadata(self, id, text, status=None):
        update_data = {'metadata_text': text}
        if status is not None:
            update_data['metadata_status'] = status
        await self.col.update_one({'id': int(id)}, {'$set': update_data})

    async def set_metadata_status(self, id, status):
        await self.col.update_one({'id': int(id)}, {'$set': {'metadata_status': status}})

    async def get_metadata(self, id):
        user = await self.col.find_one({'id': int(id)})
        if user:
            return user.get('metadata_text', None), user.get('metadata_status', False)
        return None, False

    async def ban_user(self, user_id):
        await self.blacklisted.insert_one({'id': int(user_id)})

    async def unban_user(self, user_id):
        await self.blacklisted.delete_one({'id': int(user_id)})

    async def is_banned(self, user_id):
        user = await self.blacklisted.find_one({'id': int(user_id)})
        return True if user else False

    async def add_premium(self, user_id, expiry_time):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'is_premium': True, 'premium_expiry': expiry_time}})

    async def remove_premium(self, user_id):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'is_premium': False, 'premium_expiry': 0}})

    async def is_premium(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        if user and user.get('is_premium'):
            if user.get('premium_expiry') > time.time():
                return True
            else:
                await self.remove_premium(user_id)
        return False

    async def add_credits(self, user_id, credits):
        await self.col.update_one({'id': int(user_id)}, {'$inc': {'credits': credits}})

    async def get_credits(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        return user.get('credits', 0) if user else 0

    async def get_top_renamers(self):
        # This is a bit arbitrary, but we can use credits spent or just users with most credits?
        # Let's say we have a rename_count field too.
        top_users = self.col.find({}).sort('rename_count', -1).limit(10)
        return top_users

    async def increment_rename_count(self, user_id):
        await self.col.update_one({'id': int(user_id)}, {'$inc': {'rename_count': 1}})

    async def start_sequence(self, user_id):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'is_sequencing': True, 'sequence_files': []}})

    async def add_to_sequence(self, user_id, file_id, file_name, media_type):
        await self.col.update_one(
            {'id': int(user_id)},
            {'$push': {'sequence_files': {'file_id': file_id, 'file_name': file_name, 'media_type': media_type}}}
        )

    async def get_sequence(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        return user.get('sequence_files', []) if user else []

    async def stop_sequence(self, user_id):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'is_sequencing': False, 'sequence_files': []}})
        await self.settings.update_one({'id': 'stats'}, {'$inc': {'total_sequences': 1}}, upsert=True)

    async def is_sequencing(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        return user.get('is_sequencing', False) if user else False

    async def get_total_sequences(self):
        stats = await self.settings.find_one({'id': 'stats'})
        return stats.get('total_sequences', 0) if stats else 0

db = None
if Config.DB_URL:
    db = Database(Config.DB_URL, Config.DB_NAME)
