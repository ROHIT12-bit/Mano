import math
import time

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
                text="{}\n {}".format(ud_type, tmp)
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
