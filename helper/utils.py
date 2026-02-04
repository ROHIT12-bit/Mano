import math
import time
import re
import os
from datetime import datetime
from config import Config

def big_and_nice(text):
    if not text:
        return ""

    # Mathematical Sans-Serif Bold
    def get_char(c):
        o = ord(c)
        if 65 <= o <= 90: # A-Z
            return chr(o - 65 + 0x1D5D4)
        if 97 <= o <= 122: # a-z
            return chr(o - 97 + 0x1D5EE)
        if 48 <= o <= 57: # 0-9
            return chr(o - 48 + 0x1D7EC)
        return c

    # Pattern to find segments that should NOT be transformed
    # 1. HTML tags: <[^>]+>
    # 2. Placeholders: \{[^\}]+\}
    # 3. URLs: (?:http|https)://\S+|t\.me/\S+
    # 4. Mentions: @\w+
    # 5. Hashtags: #\w+
    # 6. Markdown URLs: \[[^\]]+\]\([^\)]+\)

    combined_pattern = r'(<[^>]+>|\{[^\}]+\}|(?:http|https)://\S+|t\.me/\S+|@\w+|#\w+|\[[^\]]+\]\([^\)]+\))'

    parts = re.split(combined_pattern, text)
    result = ""

    for part in parts:
        if not part:
            continue
        # If part matches any of the protected patterns, keep it as is
        if re.match(combined_pattern, part):
            result += part
        else:
            # Transform characters in this part
            transformed_part = "".join(get_char(c) for c in part)
            result += transformed_part

    return result

def quote_text(text):
    if not text:
        return ""
    # Automatically apply big and nice style
    bn_text = big_and_nice(text)

    # Add credits if not present
    if "Botskingdoms" not in bn_text:
        bn_text += f"\n\n{Config.CREDITS_LINE}"

    if "<blockquote>" in text:
        return text # Trust the source if it already has tags
    return f"<blockquote>{bn_text}</blockquote>"

def humanbytes(size):
    if not size:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = float(size)
    i = int(math.floor(math.log(size, 1024)))
    return f"{round(size / math.pow(1024, i), 2)} {units[i]}"

async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    # Update every 4 seconds to avoid floodwait
    if not hasattr(progress_for_pyrogram, "last_update_time"):
        progress_for_pyrogram.last_update_time = {}

    user_id = message.chat.id
    last_update = progress_for_pyrogram.last_update_time.get(user_id, 0)

    if current == total or (now - last_update) > 4:
        progress_for_pyrogram.last_update_time[user_id] = now
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \n<b>Progress:</b> {2}%\n".format(
            ''.join(["█" for i in range(math.floor(percentage / 5))]),
            ''.join(["░" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))

        tmp = progress + "<b>Done:</b> {0} of {1}\n<b>Speed:</b> {2}/s\n<b>ETA:</b> {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(
                text=quote_text("{}\n {}".format(ud_type, tmp))
            )
        except:
            pass

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

def get_wish():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 17:
        return "Good Afternoon"
    elif 17 <= hour < 21:
        return "Good Evening"
    else:
        return "Good Night"

def get_file_info(filename):
    # Regex patterns for common metadata in filenames
    year_match = re.search(r'(19|20)\d{2}', filename)
    quality_match = re.search(r'(\d{3,4}p|BRRip|Web-DL|WEB-DL|HDRip|DVDRip|BluRay)', filename, re.IGNORECASE)
    season_match = re.search(r'S(\d{1,2})', filename, re.IGNORECASE)
    episode_match = re.search(r'E(\d{1,3})', filename, re.IGNORECASE)
    language_match = re.search(r'(Hindi|English|Tamil|Telugu|Kannada|Malayalam|Bengali|Marathi|Punjabi|dual)', filename, re.IGNORECASE)

    return {
        'year': year_match.group(0) if year_match else "N/A",
        'quality': quality_match.group(0) if quality_match else "N/A",
        'season': season_match.group(1) if season_match else "N/A",
        'episode': episode_match.group(1) if episode_match else "N/A",
        'language': language_match.group(0) if language_match else "N/A"
    }

def get_fillings(message):
    fillings = {}

    # Common
    fillings['wish'] = get_wish()

    # File name and extension
    file = getattr(message, message.media.value) if message.media else None
    if file:
        filename = getattr(file, 'file_name', 'None')
        fillings['filename'] = filename
        fillings['filesize'] = humanbytes(getattr(file, 'file_size', 0))
        fillings['mime_type'] = getattr(file, 'mime_type', 'N/A')
        ext = os.path.splitext(filename)[1].replace('.', '') if '.' in filename else 'None'
        fillings['ext'] = ext

        # Extracted info from filename
        info = get_file_info(filename)
        fillings.update(info)

    # Caption logic
    if message.caption:
        # We store the raw caption text and html
        fillings['caption'] = message.caption
        try:
            # entities to html
            fillings['html_caption'] = message.caption.html
        except:
            fillings['html_caption'] = message.caption

        # Also provide big and nice versions
        fillings['bn_caption'] = big_and_nice(message.caption)
    else:
        fillings['html_caption'] = "N/A"
        fillings['caption'] = "N/A"
        fillings['bn_caption'] = "N/A"

    # Specific to Video
    if message.video:
        fillings['duration'] = TimeFormatter(message.video.duration * 1000)
        fillings['height'] = message.video.height
        fillings['width'] = message.video.width
        fillings['resolution'] = f"{message.video.width}x{message.video.height}"

    # Specific to Audio
    if message.audio:
        fillings['duration'] = TimeFormatter(message.audio.duration * 1000)
        fillings['title'] = message.audio.title if message.audio.title else "N/A"
        fillings['artist'] = message.audio.artist if message.audio.artist else "N/A"

    # Specific to Photo
    if message.photo:
        fillings['filesize'] = humanbytes(message.photo.file_size)
        fillings['width'] = message.photo.width
        fillings['height'] = message.photo.height
        # Photos don't usually have filenames in Pyrogram message objects unless it's a document-photo
        if 'filename' not in fillings:
             fillings['filename'] = "photo.jpg"
             fillings['ext'] = "jpg"

    return fillings
