# Telegram Auto Renamer Bot

A powerful and fast Telegram bot to rename files, change metadata, and manage thumbnails.

## Features
- Renames very fast.
- Metadata Support.
- Permanent Thumbnail support.
- Supports Broadcasts.
- Set custom caption.
- Custom Start-up pic.
- Force subscribe available.
- Supports unlimited renaming at a time.
- Deploy to Koyeb, Heroku, Railway, Render.
- Automatically rename your files.
- File Sequencing: Organize and sequence your files in order.
- Set mediatype to upload filetype.
- Premium subscription & credits system.
- Admin commands for user management.

## Commands
- `/start` – Check whether the bot is alive
- `/trial` – Get free trial premium
- `/ssequence` – Start a file sequencing session
- `/esequence` – End a file sequencing session and receive files
- `/stats` – View global and personal statistics
- `/autorename` – Set auto-rename format
- `/showformat` – View your current rename format
- `/source` – Select rename source
- `/cancel` – Clear current queue
- `/queue` – Check current queues
- `/info` – View your account info
- `/leaderboard` – Top 10 renamers
- `/setmedia` – Choose allowed media types
- `/setthumb` – Set thumbnail
- `/viewthumb` – View current thumbnail
- `/delthumb` – Delete thumbnail
- `/get_thumb` – Extract thumbnail from video/file
- `/set_caption` – Set custom caption
- `/see_caption` – View current caption
- `/del_caption` – Delete caption
- `/meta` – Set metadata text
- `/setallmeta` – Apply metadata to all fields
- `/metaon` – Enable metadata
- `/metaoff` – Disable metadata
- `/plan` – View premium plans
- `/premium` – Check pre/plans
- `/premium_users` – List premium users
- `/addcredit` – Add credits to user
- `/remcredit` – Remove credits
- `/add_premium` – Add premium user
- `/remove_premium` – Remove premium user
- `/restart` – Restart bot
- `/status` – Bot status
- `/users` – Total users
- `/broadcast` – Broadcast message
- `/ban` – Ban a user
- `/unban` – Unban user
- `/admin_mode` – Toggle admin/user mode
- `/add_admin` – Add sudo/admin (Owner only)
- `/shortlink` – Configure link shortener

## BotFather Commands
```
start - Check whether the bot is alive
autorename - Set auto-rename format
showformat - View your current rename format
source - Select rename source
cancel - Clear current queue
queue - Check current queues
info - View your account info
leaderboard - Top 10 renamers
setmedia - Choose allowed media types
setthumb - Set thumbnail
viewthumb - View current thumbnail
delthumb - Delete thumbnail
get_thumb - Extract thumbnail from video/file
see_caption - View current caption
del_caption - Delete caption
meta - Set metadata text
setallmeta - Apply metadata to all fields
metaon - Enable metadata
metaoff - Disable metadata
plan - View premium plans
premium - Check pre/plans
trial - Get free trial premium
stats - View bot statistics
```

## Deployment

### Variables
- `API_ID`: Your Telegram API ID.
- `API_HASH`: Your Telegram API Hash.
- `BOT_TOKEN`: Your Telegram Bot Token.
- `DB_URL`: Your MongoDB URL.
- `ADMIN`: IDs of admins separated by space.
- `FORCE_SUB`: Username of the channel for force subscribe (without @).
- `START_PIC`: URL of the image to show on /start.
- `LOG_CHANNEL`: ID of the channel for logs.

### Deploy to Heroku
1. Click the Deploy button (if available) or use Heroku CLI.
2. Set the environment variables.
3. Scale the worker dyno.

### Deploy to Koyeb / Render / Railway
1. Use the provided `Dockerfile`.
2. Set the environment variables.

**By @Botskingdoms**
