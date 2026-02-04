import os
import subprocess
import asyncio
import logging
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

logger = logging.getLogger("Botskingdoms")

async def fix_thumbnail(thumbnail_path):
    # This function would use ffmpeg to resize the thumbnail if needed
    # but for now, we'll just return it.
    # Telegram requires thumbnails to be < 200kb and < 320px
    return thumbnail_path

async def take_screen_shot(video_file, output_directory, ttl):
    out_put_file_name = os.path.join(output_directory, str(ttl) + ".jpg")
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    return None

async def add_metadata(input_file, output_file, metadata_text):
    # Apply metadata using ffmpeg
    # metadata_text will be applied to title and author
    command = [
        "ffmpeg",
        "-i", input_file,
        "-metadata", f"title={metadata_text}",
        "-metadata", f"author={metadata_text}",
        "-metadata", f"artist={metadata_text}",
        "-metadata", f"comment={metadata_text}",
        "-codec", "copy",
        output_file
    ]
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await process.communicate()
    return output_file

def get_duration(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata and metadata.has("duration"):
        return metadata.get('duration').seconds
    return 0

def get_width_height(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata:
        if metadata.has("width") and metadata.has("height"):
            return metadata.get("width"), metadata.get("height")
    return 0, 0
