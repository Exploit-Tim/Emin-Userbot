# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
#
# Ported by Koala @manusiarakitann
# Recode by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio

from telethon.errors import FloodWaitError

from pyAyiin import ayiin, cmdHelp
from pyAyiin.config import GCAST_BLACKLIST
from pyAyiin.decorator import ayiinCmd
from pyAyiin.utils import eod, eor
from pyAyiin.database.blGcast import (
    addGcastGroup,
    addGcastPrivate,
    delGcastGroup,
    delGcastPrivate,
    getGcastGroup,
    getGcastPrivate,
)

from . import cmd


@ayiinCmd(pattern="gcast(?: |$)(.*)")
async def gcast(event):
    BLACKLIST_GCAST = getGcastGroup()
    if xx := event.pattern_match.group(1):
        msg = xx
    elif event.is_reply:
        reply = await event.get_reply_message()
        msg = reply.text
    else:
        return await eod(event, "**ᴛᴀᴍʙᴀʜᴋᴀɴ ᴘᴇꜱᴀɴ ᴀᴛᴀᴜ ʙᴀʟᴀꜱ ꜱᴇʙᴜᴀʜ ᴘᴇꜱᴀɴ**")
    kk = await eor(event, "`ᴍᴇᴍᴘʀᴏꜱᴇꜱ . . . ᴍᴏʜᴏɴ ᴛᴜɴɢɢᴜ ꜱᴇʙᴇɴᴛᴀʀ . . .`")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_group:
            chat = x.id
            if chat not in GCAST_BLACKLIST and chat not in BLACKLIST_GCAST:
                try:
                    await event.client.send_message(chat, msg, file=reply.media if reply else None)
                    await asyncio.sleep(0.1)
                    done += 1
                except FloodWaitError as anj:
                    await asyncio.sleep(int(anj.seconds))
                    await event.client.send_message(chat, msg, file=reply.media if reply else None)
                    done += 1
                except BaseException:
                    er += 1
    await kk.edit(
        f"**ᴘʀᴏꜱᴇꜱ ᴛᴇʟᴀʜ ꜱᴇʟᴇꜱᴀɪ.**\n **ʙᴇʀʜᴀꜱɪʟ ᴍᴇɴɢɪʀɪᴍ ᴘᴇꜱᴀɴ ᴋᴇ** {done} **ɢʀᴜᴘ.**\n**ɢᴀɢᴀʟ ᴍᴇɴɢɪʀɪᴍ ᴘᴇꜱᴀɴ ᴋᴇ** {er} **ɢʀᴜᴘ.**"
    )


@ayiinCmd(pattern="gucast(?: |$)(.*)")
async def gucast(event):
    BLACKLIST_GCAST = getGcastPrivate()
    if xx := event.pattern_match.group(1):
        msg = xx
    elif event.is_reply:
        reply = await event.get_reply_message()
        msg = reply.text
    else:
        return await eod(event, "**ᴛᴀᴍʙᴀʜᴋᴀɴ ᴘᴇꜱᴀɴ ᴀᴛᴀᴜ ʙᴀʟᴀꜱ ꜱᴇʙᴜᴀʜ ᴘᴇꜱᴀɴ**")
    kk = await eor(event, "`ᴍᴇᴍᴘʀᴏꜱᴇꜱ . . . ᴍᴏʜᴏɴ ᴛᴜɴɢɢᴜ ꜱᴇʙᴇɴᴛᴀʀ . . .`")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            if chat not in ayiin._devs and chat not in BLACKLIST_GCAST:
                try:
                    await event.client.send_message(chat, msg, file=reply.media if reply else None)
                    await asyncio.sleep(0.1)
                    done += 1
                except FloodWaitError as anj:
                    await asyncio.sleep(int(anj.seconds))
                    await event.client.send_message(chat, msg, file=reply.media if reply else None)
                    done += 1
                except BaseException:
                    er += 1
    await kk.edit(
        f"**ᴘʀᴏꜱᴇꜱ ᴛᴇʟᴀʜ ꜱᴇʟᴇꜱᴀɪ.**\n **ʙᴇʀʜᴀꜱɪʟ ᴍᴇɴɢɪʀɪᴍ ᴘᴇꜱᴀɴ ᴋᴇ** {done} **ᴄʜᴀᴛ.**\n**ɢᴀɢᴀʟ ᴍᴇɴɢɪʀɪᴍ ᴘᴇꜱᴀɴ ᴋᴇ** {er} **ᴄʜᴀᴛ.**"
    )


@ayiinCmd(pattern="blchat$")
async def sudo(event):
    me = await event.client.get_me()
    BLACKLIST_GCAST = getGcastGroup()
    BLACKLIST_GCAST_PRIVATE = getGcastPrivate()
    textGroup = '\n'
    for bl in BLACKLIST_GCAST:
        textGroup += f"   » {bl}\n"

    textPrivate = '\n'
    for bl in BLACKLIST_GCAST_PRIVATE:
        textPrivate += f"   » {bl}\n"

    await eor(
        event, 
        f"""
**🔮 𝗕𝗹𝗮𝗰𝗸𝗹𝗶𝘀𝘁 𝗚𝗖𝗔𝗦𝗧:** `Enabled`

📚 **ʙʟᴀᴄᴋʟɪꜱᴛ ɢʀᴏᴜᴘ:**
{textGroup}

📚 **ʙʟᴀᴄᴋʟɪꜱᴛ ᴘʀɪᴠᴀᴛᴇ:**
{textPrivate}


ᴋᴇᴛɪᴋ `{cmd}addblacklist g` ᴅɪ ɢʀᴜᴘ ʏᴀɴɢ ɪɴɢɪɴ ᴀɴᴅᴀ ᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇ ᴅᴀꜰᴛᴀʀ ʙʟᴀᴄᴋʟɪꜱᴛ ɢᴄᴀꜱᴛ."""
    )


@ayiinCmd(pattern="addblacklist (.*)")
async def add(event):
    command = event.pattern_match.group(1)
    if not command:
        return await eod(event, f"**ʙᴇʀɪᴋᴀɴ ꜱᴀʏᴀ ᴋᴀᴛᴀ ᴋᴜɴᴄɪ g/p. ᴄᴏɴᴛᴏʜ :** `{cmd}addblacklist g` ᴀᴛᴀᴜ `{cmd}addblacklist p`")

    xxnx = await eor(event, '**ᴍᴇᴍᴘʀᴏꜱᴇꜱ...**')
    if command == "g":
        gcastGroup = getGcastGroup()
        if event.chat_id in gcastGroup:
            await eod(
                event,
                "**ɢʀᴜᴘ ɪɴɪ ꜱᴜᴅᴀʜ ᴀᴅᴀ ᴅᴀʟᴀᴍ ᴅᴀꜰᴛᴀʀ ʙʟᴀᴄᴋʟɪꜱᴛ ɢᴄᴀꜱᴛ.**"
            )
            return
        else:
            addGcastGroup(event.chat_id)
            await xxnx.edit(
                f"**ʙᴇʀʜᴀꜱɪʟ ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ** `{event.chat_id}` **ᴋᴇ ᴅᴀꜰᴛᴀʀ ʙʟᴀᴄᴋʟɪꜱᴛ ɢᴄᴀꜱᴛ ɢʀᴜᴘ.**"
            )

    elif command == "p":
        gcastPrivate = getGcastPrivate()
        if event.chat_id in gcastPrivate:
            await eod(
                event,
                "**ɪᴅ ᴘᴇɴɢɢᴜɴᴀ ɪɴɪ ꜱᴜᴅᴀʜ ᴀᴅᴀ ᴅᴀʟᴀᴍ ᴅᴀꜰᴛᴀʀ ʙʟᴀᴄᴋʟɪꜱᴛ ɢᴄᴀꜱᴛ.**"
            )
            return
        else:
            addGcastPrivate(event.chat_id)
            await xxnx.edit(
                f"**ʙᴇʀʜᴀꜱɪʟ ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ** `{event.chat_id}` **ᴋᴇ ᴅᴀꜰᴛᴀʀ ʙʟᴀᴄᴋʟɪꜱᴛ ɢᴄᴀꜱᴛ ᴘʀɪʙᴀᴅɪ.**"
            )

    else:
        await eod(event, f"**ʙᴇʀɪᴋᴀɴ ꜱᴀʏᴀ ᴋᴀᴛᴀ ᴋᴜɴᴄɪ g/p. ᴄᴏɴᴛᴏʜ :** `{cmd}addblacklist g` ᴀᴛᴀᴜ `{cmd}addblacklist p`")


@ayiinCmd(pattern="delblacklist(?:\\s|$)([\\s\\S]*)")
async def _(event):
    command = event.pattern_match.group(1)
    if not command:
        return await eod(event, f"**ʙᴇʀɪᴋᴀɴ ꜱᴀʏᴀ ᴋᴀᴛᴀ ᴋᴜɴᴄɪ g/p. ᴄᴏɴᴛᴏʜ :** `{cmd}addblacklist g` ᴀᴛᴀᴜ `{cmd}addblacklist p`")
    
    xxx = await eor(event, '**ᴍᴇᴍᴘʀᴏꜱᴇꜱ...**')
    
    if command == "g":
        gcastGroup = getGcastGroup()
        if event.chat_id in gcastGroup:
            delGcastGroup(event.chat_id)
            await xxx.edit(f"**ʙᴇʀʜᴀꜱɪʟ ᴍᴇɴɢʜᴀᴘᴜꜱ** `{event.chat_id}` **ᴅᴀʀɪ ᴅᴀꜰᴛᴀʀ ʙʟᴀᴄᴋʟɪꜱᴛ ɢᴄᴀꜱᴛ ɢʀᴜᴘ.**"
            )
        else:
            await eod(
                xxx,
                "**ɢʀᴜᴘ ɪɴɪ ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴅᴀʟᴀᴍ ᴅᴀꜰᴛᴀʀ ʙʟᴀᴄᴋʟɪꜱᴛ ɢᴄᴀꜱᴛ.**",
                time=45
            )

    elif command == "p":
        gcastPrivate = getGcastPrivate()
        if event.chat_id in gcastPrivate:
            delGcastPrivate(event.chat_id)
            await xxx.edit(f"**ʙᴇʀʜᴀꜱɪʟ ᴍᴇɴɢʜᴀᴘᴜꜱ** `{event.chat_id}` **ᴅᴀʀɪ ᴅᴀꜰᴛᴀʀ ʙʟᴀᴄᴋʟɪꜱᴛ ɢᴄᴀꜱᴛ ᴘʀɪʙᴀᴅɪ.**"
            )
        else:
            await eod(
                xxx,
                "**ɪᴅ ᴘᴇɴɢɢᴜɴᴀ ɪɴɪ ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴅᴀʟᴀᴍ ᴅᴀꜰᴛᴀʀ ʙʟᴀᴄᴋʟɪꜱᴛ ɢᴄᴀꜱᴛ.**",
                time=45
            )

    else:
        await eod(event, f"**ʙᴇʀɪᴋᴀɴ ꜱᴀʏᴀ ᴋᴀᴛᴀ ᴋᴜɴᴄɪ g/p. ᴄᴏɴᴛᴏʜ :** `{cmd}addblacklist g` ᴀᴛᴀᴜ `{cmd}addblacklist p`")


cmdHelp.update(
    {
        "ɢᴄᴀꜱᴛ": f"**ᴘʟᴜɢɪɴ : **`ɢᴄᴀꜱᴛ`\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}gcast` <ᴛᴇxᴛ/ʀᴇᴘʟʏ ᴍᴇᴅɪᴀ>\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴍᴇɴɢɪʀɪᴍ ɢʟᴏʙᴀʟ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴘᴇꜱᴀɴ ᴋᴇ ꜱᴇʟᴜʀᴜʜ ɢʀᴜᴘ ʏᴀɴɢ ᴋᴀᴍᴜ ᴍᴀꜱᴜᴋ. (ʙɪꜱᴀ ᴍᴇɴɢɪʀɪᴍ ᴍᴇᴅɪᴀ/ꜱᴛɪᴄᴋᴇʀ)\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}blchat`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴜɴᴛᴜᴋ ᴍᴇɴɢᴇᴄᴇᴋ ɪɴꜰᴏʀᴍᴀꜱɪ ᴅᴀꜰᴛᴀʀ ʙʟᴀᴄᴋʟɪꜱᴛ ɢᴄᴀꜱᴛ.\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}addblacklist`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴜɴᴛᴜᴋ ᴍᴇɴᴀᴍʙᴀʜᴋᴀɴ ɢʀᴜᴘ ᴛᴇʀꜱᴇʙᴜᴛ ᴋᴇ ʙʟᴀᴄᴋʟɪꜱᴛ ɢᴄᴀꜱᴛ.\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}delblacklist`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴜɴᴛᴜᴋ ᴍᴇɴɢʜᴀᴘᴜꜱ ɢʀᴜᴘ ᴛᴇʀꜱᴇʙᴜᴛ ᴅᴀʀɪ ʙʟᴀᴄᴋʟɪꜱᴛ ɢᴄᴀꜱᴛ.\
        \n  •  **ɴᴏᴛᴇ : **ᴋᴇᴛɪᴋ ᴘᴇʀɪɴᴛᴀʜ** `{cmd}addblacklist` **ᴅᴀɴ** `{cmd}delblacklist` **ᴅɪ ɢʀᴜᴘ ʏᴀɴɢ ᴋᴀᴍᴜ ʙʟᴀᴄᴋʟɪꜱᴛ.\
    "
    }
)


cmdHelp.update(
    {
        "gucast": f"**Plugin : **`gucast`\
        \n\n  »  **Perintah :** `{cmd}gucast` <text/reply media>\
        \n  »  **Kegunaan : **Mengirim Global Broadcast pesan ke Seluruh Private Massage / PC yang masuk. (Bisa Mengirim Media/Sticker)\
    "
    }
)
