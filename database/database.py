import motor.motor_asyncio
from config import Config
import time
import logging

logger = logging.getLogger("Botskingdoms")

class Database:
    def __init__(self, uri, database_name):
        if not uri:
            self._client = None
            self.db = None
            self.col = None
            self.blacklisted = None
            self.premium = None
            self.settings = None
            logger.warning("No DB_URL provided. Database features will be disabled.")
            return
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.blacklisted = self.db.blacklisted
        self.premium = self.db.premium
        self.settings = self.db.settings

    async def get_admins(self):
        if self.settings is None:
            return list(set(Config.Botskingdoms))
        settings = await self.settings.find_one({'id': 'admin_list'})
        db_admins = settings.get('admins', []) if settings else []
        return list(set(db_admins + Config.Botskingdoms))

    async def add_admin(self, admin_id):
        if self.settings is None: return
        await self.settings.update_one({'id': 'admin_list'}, {'$addToSet': {'admins': int(admin_id)}}, upsert=True)

    async def remove_admin(self, admin_id):
        if self.settings is None: return
        await self.settings.update_one({'id': 'admin_list'}, {'$pull': {'admins': int(admin_id)}})

    async def set_shortlink(self, url, api):
        if self.settings is None: return
        await self.settings.update_one({'id': 'shortlink'}, {'$set': {'url': url, 'api': api}}, upsert=True)

    async def get_shortlink(self):
        if self.settings is None: return None
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
            sequence_files=[],
            used_trial=False
        )

    async def add_user(self, id):
        if self.col is None: return
        if await self.is_user_exist(id): return
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        if self.col is None: return False
        user = await self.col.find_one({'id': int(id)})
        return True if user else False

    async def get_user_data(self, id):
        if self.col is None: return {}
        user = await self.col.find_one({'id': int(id)})
        return user if user else {}

    async def total_users_count(self):
        if self.col is None: return 0
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        if self.col is None:
            # Return an empty async iterator
            async def empty_gen():
                if False: yield None
            return empty_gen()
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        if self.col is None: return
        await self.col.delete_many({'id': int(user_id)})

    async def set_thumb(self, id, file_id):
        if self.col is None: return
        await self.col.update_one({'id': int(id)}, {'$set': {'thumb': file_id}})

    async def get_thumb(self, id):
        if self.col is None: return None
        user = await self.col.find_one({'id': int(id)})
        return user.get('thumb', None) if user else None

    async def set_caption(self, id, caption):
        if self.col is None: return
        await self.col.update_one({'id': int(id)}, {'$set': {'caption': caption}})

    async def get_caption(self, id):
        if self.col is None: return None
        user = await self.col.find_one({'id': int(id)})
        return user.get('caption', None) if user else None

    async def set_autorename_format(self, id, format):
        if self.col is None: return
        await self.col.update_one({'id': int(id)}, {'$set': {'autorename_format': format}})

    async def get_autorename_format(self, id):
        if self.col is None: return None
        user = await self.col.find_one({'id': int(id)})
        return user.get('autorename_format', None) if user else None

    async def set_media_type(self, id, media_type):
        if self.col is None: return
        await self.col.update_one({'id': int(id)}, {'$set': {'media_type': media_type}})

    async def get_media_type(self, id):
        if self.col is None: return 'document'
        user = await self.col.find_one({'id': int(id)})
        return user.get('media_type', 'document') if user else 'document'

    async def set_metadata(self, id, text, status=None):
        if self.col is None: return
        update_data = {'metadata_text': text}
        if status is not None:
            update_data['metadata_status'] = status
        await self.col.update_one({'id': int(id)}, {'$set': update_data})

    async def set_metadata_status(self, id, status):
        if self.col is None: return
        await self.col.update_one({'id': int(id)}, {'$set': {'metadata_status': status}})

    async def get_metadata(self, id):
        if self.col is None: return None, False
        user = await self.col.find_one({'id': int(id)})
        if user:
            return user.get('metadata_text', None), user.get('metadata_status', False)
        return None, False

    async def ban_user(self, user_id):
        if self.blacklisted is None: return
        await self.blacklisted.insert_one({'id': int(user_id)})

    async def unban_user(self, user_id):
        if self.blacklisted is None: return
        await self.blacklisted.delete_one({'id': int(user_id)})

    async def is_banned(self, user_id):
        if self.blacklisted is None: return False
        user = await self.blacklisted.find_one({'id': int(user_id)})
        return True if user else False

    async def add_premium(self, user_id, expiry_time):
        if self.col is None: return
        await self.col.update_one({'id': int(user_id)}, {'$set': {'is_premium': True, 'premium_expiry': expiry_time}})

    async def remove_premium(self, user_id):
        if self.col is None: return
        await self.col.update_one({'id': int(user_id)}, {'$set': {'is_premium': False, 'premium_expiry': 0}})

    async def is_premium(self, user_id):
        if self.col is None: return False
        user = await self.col.find_one({'id': int(user_id)})
        if user and user.get('is_premium'):
            if user.get('premium_expiry') > time.time():
                return True
            else:
                await self.remove_premium(user_id)
        return False

    async def add_credits(self, user_id, credits):
        if self.col is None: return
        await self.col.update_one({'id': int(user_id)}, {'$inc': {'credits': credits}})

    async def get_credits(self, user_id):
        if self.col is None: return 0
        user = await self.col.find_one({'id': int(user_id)})
        return user.get('credits', 0) if user else 0

    async def get_top_renamers(self):
        if self.col is None:
            async def empty_gen():
                if False: yield None
            return empty_gen()
        top_users = self.col.find({}).sort('rename_count', -1).limit(10)
        return top_users

    async def increment_rename_count(self, user_id):
        if self.col is None: return
        await self.col.update_one({'id': int(user_id)}, {'$inc': {'rename_count': 1}})

    async def start_sequence(self, user_id):
        if self.col is None: return
        await self.col.update_one({'id': int(user_id)}, {'$set': {'is_sequencing': True, 'sequence_files': []}})

    async def add_to_sequence(self, user_id, file_id, file_name, media_type):
        if self.col is None: return
        await self.col.update_one(
            {'id': int(user_id)},
            {'$push': {'sequence_files': {'file_id': file_id, 'file_name': file_name, 'media_type': media_type}}}
        )

    async def get_sequence(self, user_id):
        if self.col is None: return []
        user = await self.col.find_one({'id': int(user_id)})
        return user.get('sequence_files', []) if user else []

    async def stop_sequence(self, user_id):
        if self.col is None: return
        await self.col.update_one({'id': int(user_id)}, {'$set': {'is_sequencing': False, 'sequence_files': []}})
        if self.settings is not None:
            await self.settings.update_one({'id': 'stats'}, {'$inc': {'total_sequences': 1}}, upsert=True)

    async def is_sequencing(self, user_id):
        if self.col is None: return False
        user = await self.col.find_one({'id': int(user_id)})
        return user.get('is_sequencing', False) if user else False

    async def has_used_trial(self, user_id):
        if self.col is None: return True
        user = await self.col.find_one({'id': int(user_id)})
        return user.get('used_trial', False) if user else True

    async def set_used_trial(self, user_id):
        if self.col is None: return
        await self.col.update_one({'id': int(user_id)}, {'$set': {'used_trial': True}})

    async def get_total_sequences(self):
        if self.settings is None: return 0
        stats = await self.settings.find_one({'id': 'stats'})
        return stats.get('total_sequences', 0) if stats else 0

db = Database(Config.DB_URL, Config.DB_NAME)
