# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# Recode by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import logging
from asyncio import sleep
from traceback import format_exc

from telethon.errors import (
    BadRequestError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from telethon.errors.rpcerrorlist import (
    ChatAdminRequiredError,
    UserAdminInvalidError,
    UserIdInvalidError,
)
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChatAdminRights,
    ChatBannedRights,
    User,
    InputChatPhotoEmpty,
    MessageMediaPhoto,
)

from pyAyiin import ayiin, cmdHelp
from pyAyiin.decorator import ayiinCmd, ayiinHandler
from pyAyiin.lib.tools import media_type
from pyAyiin.utils import eod, eor
from pyAyiin.database.muted import (
    addGmute,
    addMute,
    cekMute,
    cekGmute,
    delGmute,
    delMute,
)

from . import cmd

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)


LOGS = logging.getLogger(__name__)
MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================


@ayiinCmd(pattern="setgpic( -s| -d)$", only="groups")
async def set_group_photo(event):
    "For changing Group dp"
    flag = (event.pattern_match.group(1)).strip()
    if flag == "-s":
        replymsg = await event.get_reply_message()
        photo = None
        if replymsg and replymsg.media:
            if isinstance(replymsg.media, MessageMediaPhoto):
                photo = await event.client.download_media(message=replymsg.photo)
            elif "image" in replymsg.media.document.mime_type.split("/"):
                photo = await event.client.download_file(replymsg.media.document)
            else:
                return await eor(event, "**ᴍᴇᴅɪᴀ ᴛɪᴅᴀᴋ ᴠᴀʟɪᴅ**", time=10)
        if photo:
            try:
                await event.client(
                    EditPhotoRequest(
                        event.chat_id, await event.client.upload_file(photo)
                    )
                )
                await eor(event, "**ʙᴇʀʜᴀꜱɪʟ ᴍᴇɴɢᴜʙᴀʜ ᴘʀᴏꜰɪʟ ɢʀᴜᴘ**", time=10)
            except PhotoCropSizeSmallError:
                return await eor(
                    event,
                    "**ɢᴀᴍʙᴀʀ ᴛᴇʀʟᴀʟᴜ ᴋᴇᴄɪʟ**",
                    time=10
                )
            except ImageProcessFailedError:
                return await eor(event, "**ꜱᴀʏᴀ ᴍᴇᴍᴇʀʟᴜᴋᴀɴ ʜᴀᴋ ᴀᴅᴍɪɴ ᴜɴᴛᴜᴋ ᴍᴇʟᴀᴋᴜᴋᴀɴ ᴛɪɴᴅᴀᴋᴀɴ ɪɴɪ!**", time=10)
            except Exception as e:
                return await eor(event, "**​ᴋᴇꜱᴀʟᴀʜᴀɴ​ : **`{}`".format(e))
    else:
        try:
            await event.client(EditPhotoRequest(event.chat_id, InputChatPhotoEmpty()))
        except Exception as e:
            return await eor(event, "**ᴋᴇꜱᴀʟᴀʜᴀɴ : **`{}`".format(e))
        await eor(event, "**ꜰᴏᴛᴏ ᴘʀᴏꜰɪʟ ɢʀᴜᴘ ʙᴇʀʜᴀꜱɪʟ ᴅɪʜᴀᴘᴜꜱ.**", time=30)


@ayiinCmd(pattern="promote(?:\\s|$)([\\s\\S]*)", only="groups")
async def promote(event):
    new_rights = ChatAdminRights(
        add_admins=False,
        change_info=True,
        invite_users=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
        manage_call=True,
    )
    user, rank = await ayiin.getUserFromEvent(event)
    if not rank:
        rank = "admin"
    if not user:
        return
    await eor(event, "`​🇲​​🇪​​🇲​​🇵​​🇷​​🇴​​🇲​​🇴​​🇸​​🇮​​🇰​​🇦​​🇳​...`")
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await eod(event, "**ᴛɪᴅᴀᴋ ᴍᴇᴍᴘᴜɴʏᴀɪ ɪᴢɪɴ!**")
    await eor(event, "`ʙᴇʀʜᴀꜱɪʟ ᴅɪᴘʀᴏᴍᴏꜱɪᴋᴀɴ!`", time=30)


@ayiinCmd(pattern="demote(?:\\s|$)([\\s\\S]*)", only="groups")
async def demote(event):
    "ᴛᴏ ᴅᴇᴍᴏᴛᴇ ᴀ ᴘᴇʀꜱᴏɴ ɪɴ ɢʀᴏᴜᴘ"
    user, _ = await ayiin.getUserFromEvent(event)
    if not user:
        return
    await eor(event, "`ᴍᴇɴᴜʀᴜɴᴋᴀɴ...`")
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
        manage_call=None,
    )
    rank = "admin"
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))
    except BadRequestError:
        return await eor(event, "**ᴛɪᴅᴀᴋ ᴍᴇᴍᴘᴜɴʏᴀɪ ɪᴢɪɴ!**")
    await eor(event, "`ʙᴇʀʜᴀꜱɪʟ ᴅɪᴛᴜʀᴜɴᴋᴀɴ!`", time=30)


@ayiinCmd(pattern="ban(?:\\s|$)([\\s\\S]*)", only="groups")
async def ban(bon):
    me = await bon.client.get_me()
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        return await eor(bon, "**ɢᴀɢᴀʟ ᴅɪᴋᴀʀᴇɴᴀᴋᴀɴ ʙᴜᴋᴀɴ ᴀᴅᴍɪɴ.**")

    user, reason = await ayiin.getUserFromEvent(bon)
    if not user:
        return
    ayiin = await eor(bon, "`ᴘᴇᴍʀᴏꜱᴇꜱᴀɴ ʟᴀʀᴀɴɢᴀɴ...`")
    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        return await eor(bon, "**ᴛɪᴅᴀᴋ ᴍᴇᴍᴘᴜɴʏᴀɪ ɪᴢɪɴ!**")
    if reason:
        await ayiin.edit(
            f"""
\\**#𝘽𝙖𝙣𝙣𝙚𝙙_𝙐𝙨𝙚𝙧**//

**𝙁𝙞𝙧𝙨𝙩 𝙉𝙖𝙢𝙚 :** [{user.first_name}](tg://user?id={user.id})
**𝙐𝙨𝙚𝙧 𝙄𝘿 :** `{str(user.id)}`
**𝘼𝙘𝙩𝙞𝙤𝙣 :** `𝘽𝙖𝙣𝙣𝙚𝙙 𝙐𝙨𝙚𝙧`
**𝙍𝙚𝙖𝙨𝙤𝙣 :** `{reason}`
**𝘽𝙖𝙣𝙣𝙚𝙙 𝘽𝙮 :** `{me.first_name}`
**𝙋𝙤𝙬𝙚𝙧𝙚𝙙 𝘽𝙮 : ✧ ᴇᴍɪɴ-ᴜsᴇʀʙᴏᴛ ✧**
"""
        )
    else:
        await ayiin.edit(
            f"""
\\**#𝘽𝙖𝙣𝙣𝙚𝙙_𝙐𝙨𝙚𝙧**//

**𝙁𝙞𝙧𝙨𝙩 𝙉𝙖𝙢𝙚 :** [{user.first_name}](tg://user?id={user.id})
**𝙐𝙨𝙚𝙧 𝙄𝘿 :** `{str(user.id)}`
**𝘼𝙘𝙩𝙞𝙤𝙣 :** `𝘽𝙖𝙣𝙣𝙚𝙙 𝙐𝙨𝙚𝙧`
**𝘽𝙖𝙣𝙣𝙚𝙙 𝘽𝙮 :** `{me.first_name}`
**𝙋𝙤𝙬𝙚𝙧𝙚𝙙 𝘽𝙮 : ✧ ᴇᴍɪɴ-ᴜsᴇʀʙᴏᴛ ✧**
"""
        )


@ayiinCmd(pattern="unban(?:\\s|$)([\\s\\S]*)", only="groups")
async def nothanos(unbon):
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        return await eor(unbon, "**ɢᴀɢᴀʟ ᴅɪᴋᴀʀᴇɴᴀᴋᴀɴ ʙᴜᴋᴀɴ ᴀᴅᴍɪɴ.**")
    await eor(unbon, '**ᴍᴇᴍᴘʀᴏꜱᴇꜱ...**')
    user = await ayiin.getUserFromEvent(unbon)
    user = user[0]
    if not user:
        return
    try:
        await unbon.client(EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await eor(unbon, "`ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ʟᴀʀᴀɴɢᴀɴ ʙᴇʀʜᴀꜱɪʟ ᴅɪʟᴀᴋᴜᴋᴀɴ!`", time=10)
    except UserIdInvalidError:
        await eor(unbon, "`​ꜱᴇᴘᴇʀᴛɪɴʏᴀ ᴛᴇʀᴊᴀᴅɪ ᴋᴇꜱᴀʟᴀʜᴀɴ​!`", time=10)


@ayiinCmd(pattern="mute(?: |$)(.*)", only="groups")
async def spider(spdr):
    chat = await spdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        return await eor(spdr, "**​ɢᴀɢᴀʟ ᴅɪᴋᴀʀᴇɴᴀᴋᴀɴ ʙᴜᴋᴀɴ ᴀᴅᴍɪɴ.**")
    user, reason = await ayiin.getUserFromEvent(spdr)
    if not user:
        return
    self_user = await spdr.client.get_me()
    if user.id == self_user.id:
        return await eor(spdr, "**ᴛɪᴅᴀᴋ ʙɪꜱᴀ ᴍᴇᴍʙɪꜱᴜᴋᴀɴ ᴅɪʀɪ ꜱᴇɴᴅɪʀɪ​..（>﹏<）**")
    if user.id in ayiin._devs:
        return await eor(spdr, "**ɢᴀɢᴀʟ ᴍᴇᴍʙɪꜱᴜᴋᴀɴ, ᴋᴀʀɴᴀ ᴅɪᴀ ᴀᴅᴀʟᴀʜ ᴘᴇᴍʙᴜᴀᴛ ꜱᴀʏᴀ 🤪**")
    await eor(
        spdr,
        "**​ᴍᴇᴍʙɪꜱᴜᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ​...**"
    )
    muting = cekMute(self_user.id)
    if user.id in muting:
        return await eor(spdr, "**ᴋᴇꜱᴀʟᴀʜᴀɴ!** `ᴘᴇɴɢɢᴜɴᴀ ꜱᴜᴅᴀʜ ᴅɪʙɪꜱᴜᴋᴀɴ​.`")
    try:
        await spdr.client(EditBannedRequest(spdr.chat_id, user.id, MUTE_RIGHTS))
        addMute(self_user.id, user.id)
        if reason:
            await eor(
                spdr,
                f"""
\\**#𝙈𝙪𝙩𝙚𝙙_𝙐𝙨𝙚𝙧**//

**𝙁𝙞𝙧𝙨𝙩 𝙉𝙖𝙢𝙚 :** [{user.first_name}](tg://user?id={user.id})
**𝙐𝙨𝙚𝙧 𝙄𝘿 :** `{user.id}`
**𝙍𝙚𝙖𝙨𝙤𝙣 :** `{reason}`
**𝙈𝙪𝙩𝙚𝙙 𝘽𝙮 :** `{self_user.first_name}`
**𝙋𝙤𝙬𝙚𝙧𝙚𝙙 𝘽𝙮 : ✧ ᴇᴍɪɴ-ᴜsᴇʀʙᴏᴛ ✧**
"""
            )
        else:
            await eor(
                spdr,
                f'''
\\**#𝙈𝙪𝙩𝙚𝙙_𝙐𝙨𝙚𝙧**//

**𝙁𝙞𝙧𝙨𝙩 𝙉𝙖𝙢𝙚 :** [{user.first_name}](tg://user?id={user.id})
**𝙐𝙨𝙚𝙧 𝙄𝘿 :** `{user.id}`
**𝘼𝙘𝙩𝙞𝙤𝙣 :** `𝙈𝙪𝙩𝙚𝙙 𝙐𝙨𝙚𝙧`
**𝙈𝙪𝙩𝙚𝙙 𝘽𝙮 :** `{self_user.first_name}`
**𝙋𝙤𝙬𝙚𝙧𝙚𝙙 𝘽𝙮 : ✧ ᴇᴍɪɴ-ᴜsᴇʀʙᴏᴛ ✧**
'''
            )
    except UserIdInvalidError:
        return await eor(spdr, "**​ᴛᴇʀᴊᴀᴅɪ ᴋᴇꜱᴀʟᴀʜᴀɴ!**", time=10)


@ayiinCmd(pattern="unmute(?: |$)(.*)", only="groups")
async def unmoot(unmot):
    self_user = await unmot.client.get_me()
    chat = await unmot.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        return await eor(unmot, "**ɢᴀɢᴀʟ ᴅɪᴋᴀʀᴇɴᴀᴋᴀɴ ʙᴜᴋᴀɴ ᴀᴅᴍɪɴ.**", time=10)
    xx = await eor(unmot, '**ᴍᴇᴍᴘʀᴏꜱᴇꜱ...**')
    user = await ayiin.getUserFromEvent(unmot)
    user = user[0]
    if not user:
        return xx.edit("​ɴᴏᴛ ᴜꜱᴇʀ​")
    muted = cekMute(self_user.id)
    if muted:
        muting = eval(muted)
    else:
        muting = muted
    if user.id not in muting:
        return await xx.edit("**ᴋᴇꜱᴀʟᴀʜᴀɴ! ᴘᴇɴɢɢᴜɴᴀ ꜱᴜᴅᴀʜ ᴛɪᴅᴀᴋ ᴅɪʙɪꜱᴜᴋᴀɴ.**")
    try:
        await unmot.client(EditBannedRequest(unmot.chat_id, user.id, UNBAN_RIGHTS))
        await xx.edit("**​ʙᴇʀʜᴀꜱɪʟ ᴍᴇʟᴀᴋᴜᴋᴀɴ ᴜɴᴍᴜᴛᴇ!**")
        delMute(self_user.id, user.id)
    except UserIdInvalidError:
        return await eod(xx, "**ᴛᴇʀᴊᴀᴅɪ ᴋᴇꜱᴀʟᴀʜᴀɴ​!**")


@ayiinHandler()
async def muter(moot):
    me = await moot.client.get_me()
    muted = cekMute(me.id)
    gmuted = cekGmute(me.id)
    rights = ChatBannedRights(
        until_date=None,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True,
    )
    if muted:
        for i in eval(muted):
            if str(i) == str(moot.sender_id):
                await moot.delete()
                await moot.client(
                    EditBannedRequest(moot.chat_id, moot.sender_id, rights)
                )
    elif gmuted:
        for i in eval(gmuted):
            if str(i) == str(moot.sender_id):
                await moot.delete()


@ayiinCmd(pattern="ungmute(?: |$)(.*)", only="groups")
async def ungmoot(un_gmute):
    me = await un_gmute.client.get_me()
    chat = await un_gmute.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        return await eor(un_gmute, "**ɢᴀɢᴀʟ ᴅɪᴋᴀʀᴇɴᴀᴋᴀɴ ʙᴜᴋᴀɴ ᴀᴅᴍɪɴ.**", time=10)
    ayiin = await eor(un_gmute, '**ᴍᴇᴍᴘʀᴏꜱᴇꜱ...**')
    user = await ayiin.getUserFromEvent(un_gmute)
    user = user[0]
    if not user:
        return
    await ayiin.edit("**ᴍᴇᴍʙᴜᴋᴀ ɢʟᴏʙᴀʟ ᴍᴜᴛᴇ ᴘᴇɴɢɢᴜɴᴀ​...**")
    ungmuting = cekGmute(me.id)
    if user.id in ungmuting:
        await ayiin.edit("**ᴋᴇꜱᴀʟᴀʜᴀɴ!** ᴘᴇɴɢɢᴜɴᴀ ꜱᴜᴅᴀʜ ᴛɪᴅᴀᴋ ᴅɪ ʙɪꜱᴜᴋᴀɴ ɢʟᴏʙᴀʟ...")
        delGmute(me.id, user.id)
        return
    else:
        await ayiin.edit("**ʙᴇʀʜᴀꜱɪʟ! ᴘᴇɴɢɢᴜɴᴀ ꜱᴜᴅᴀʜ ᴛɪᴅᴀᴋ ᴅɪ ʙɪꜱᴜᴋᴀɴ**", time=10)


@ayiinCmd(pattern="gmute(?: |$)(.*)", only="groups")
async def gspider(gspdr):
    try:
        chat = await gspdr.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return await eor(gspdr, "**ɢᴀɢᴀʟ ᴅɪᴋᴀʀᴇɴᴀᴋᴀɴ ʙᴜᴋᴀɴ ᴀᴅᴍɪɴ.**", time=10)
        ayiin = await eor(gspdr, '**ᴍᴇᴍᴘʀᴏꜱᴇꜱ...**')
        user, reason = await ayiin.getUserFromEvent(gspdr)
        if not user:
            return
        self_user = await gspdr.client.get_me()
        if user.id == self_user.id:
            return await ayiin.edit("**ᴛɪᴅᴀᴋ ʙɪꜱᴀ ᴍᴇᴍʙɪꜱᴜᴋᴀɴ ᴅɪʀɪ ꜱᴇɴᴅɪʀɪ..（>﹏<）**")
        if user.id in ayiin._devs:
            return await ayiin.edit("**ɢᴀɢᴀʟ ᴍᴇᴍʙɪꜱᴜᴋᴀɴ ɢʟᴏʙᴀʟ, ᴋᴀʀɴᴀ ᴅɪᴀ ᴀᴅᴀʟᴀʜ ᴘᴇᴍʙᴜᴀᴛ ꜱᴀʏᴀ 🤪**")
        await ayiin.edit("**​ʙᴇʀʜᴀꜱɪʟ ᴍᴇᴍʙɪꜱᴜᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ!**")
        gmuted = cekGmute(self_user.id)
        if user.id in gmuted:
            await eor(gspdr, "**​ᴋᴇꜱᴀʟᴀʜᴀɴ! ᴘᴇɴɢɢᴜɴᴀ ꜱᴜᴅᴀʜ ᴅɪʙɪꜱᴜᴋᴀɴ​.**")
            return
        else:
            addGmute(self_user.id, user.id)
            if reason:
                await ayiin.edit(
                    f'''
\\**#𝙂𝙈𝙪𝙩𝙚𝙙_𝙐𝙨𝙚𝙧**//

**𝙁𝙞𝙧𝙨𝙩 𝙉𝙖𝙢𝙚 :** [{user.first_name}](tg://user?id={user.id})
**𝙐𝙨𝙚𝙧 𝙄𝘿 :** `{user.id}`
**𝙍𝙚𝙖𝙨𝙤𝙣 :** `{reason}`
**𝙂𝙢𝙪𝙩𝙚𝙙 𝘽𝙮 :** `{self_user.first_name}`
**𝙋𝙤𝙬𝙚𝙧𝙚𝙙 𝘽𝙮 : ✧ ᴇᴍɪɴ-ᴜsᴇʀʙᴏᴛ ✧**
'''
                )
            else:
                await ayiin.edit(
                    f'''
\\**#𝙂𝙢𝙪𝙩𝙚𝙙_𝙐𝙨𝙚𝙧**//

**𝙁𝙞𝙧𝙨𝙩 𝙉𝙖𝙢𝙚 :** [{user.first_name}](tg://user?id={user.id})
**𝙐𝙨𝙚𝙧 𝙄𝘿:** `{user.id}`
**𝘼𝙘𝙩𝙞𝙤𝙣 :** `𝙂𝙡𝙤𝙗𝙖𝙡 𝙈𝙪𝙩𝙚𝙙`
**𝙂𝙢𝙪𝙩𝙚𝙙 𝘽𝙮 :** `{self_user.first_name}`
**𝙋𝙤𝙬𝙚𝙧𝙚𝙙 𝘽𝙮 : ✧ ᴇᴍɪɴ-ᴜsᴇʀʙᴏᴛ ✧**
'''
                )
    except BaseException:
        await eor(ayiin, f'{format_exc()}')


@ayiinCmd(pattern="zombies(?: |$)(.*)", only="groups")
async def rm_deletedacc(show):
    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "**ɢʀᴜᴘ ʙᴇʀꜱɪʜ, ᴛɪᴅᴀᴋ ᴍᴇɴᴇᴍᴜᴋᴀɴ ᴀᴋᴜɴ ᴛᴇʀʜᴀᴘᴜꜱ.**"
    if con != "clean":
        await eor(show, "`ᴍᴇɴᴄᴀʀɪ ᴀᴋᴜɴ ᴅᴇᴘʀᴇꜱɪ...`")
        async for user in show.client.iter_participants(show.chat_id):
            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = f"**ᴍᴇɴᴇᴍᴜᴋᴀɴ** `{del_u}` **ᴀᴋᴜɴ ᴅᴇᴘʀᴇꜱɪ/ᴛᴇʀʜᴀᴘᴜꜱ/ᴢᴏᴍʙɪᴇ ᴅᴀʟᴀᴍ ɢʀᴜᴘ ɪɴɪ,**\n**ʙᴇʀꜱɪʜᴋᴀɴ ɪᴛᴜ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ᴘᴇʀɪɴᴛᴀʜ** `{cmd}zombies clean`"
        return await show.edit(del_status)
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        return await eor(show, "**ᴍᴀᴀꜰ ᴋᴀᴍᴜ ʙᴜᴋᴀɴ ᴀᴅᴍɪɴ!**")
    await eor(show, "`ᴍᴇɴɢʜᴀᴘᴜꜱ ᴀᴋᴜɴ ᴅᴇᴘʀᴇꜱɪ...`")
    del_u = 0
    del_a = 0
    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS)
                )
            except ChatAdminRequiredError:
                return await eor(show, "`ᴛɪᴅᴀᴋ ᴍᴇᴍɪʟɪᴋɪ ɪᴢɪɴ ʙᴀɴɴᴇᴅ ᴅᴀʟᴀᴍ ɢʀᴜᴘ ɪɴɪ`")
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await show.client(EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1
    if del_u > 0:
        del_status = f"**ᴍᴇᴍʙᴇʀꜱɪʜᴋᴀɴ** `{del_u}` **ᴀᴋᴜɴ ᴛᴇʀʜᴀᴘᴜꜱ**"
    if del_a > 0:
        del_status = f"**ᴍᴇᴍʙᴇʀꜱɪʜᴋᴀɴ** `{del_u}` **ᴀᴋᴜɴ ᴛᴇʀʜᴀᴘᴜꜱ**\n`{del_a}` **ᴀᴋᴜɴ ᴀᴅᴍɪɴ ʏᴀɴɢ ᴛᴇʀʜᴀᴘᴜꜱ ᴛɪᴅᴀᴋ ᴅɪʜᴀᴘᴜꜱ.**"
    await show.edit(del_status)
    await sleep(2)
    await show.delete()
    if ayiin.BOTLOG_CHATID:
        await show.client.send_message(
            ayiin.BOTLOG_CHATID, 
            f"**#ᴢᴏᴍʙɪᴇꜱ**\n**ᴍᴇᴍʙᴇʀꜱɪʜᴋᴀɴ** `{del_u}` **ᴀᴋᴜɴ ᴛᴇʀʜᴀᴘᴜꜱ!**\n**ɢʀᴜᴘ:** {show.chat.title}(`{show.chat_id}`)"
        )


@ayiinCmd(pattern="admins$", only="groups")
async def get_admin(show):
    info = await show.client.get_entity(show.chat_id)
    title = info.title or "ɢʀᴜᴘ ɪɴɪ"
    mentions = f"<b>♕︎ ᴅᴀꜰᴛᴀʀ ᴀᴅᴍɪɴ ɢʀᴜᴘ {title}:</b> \n"
    try:
        async for user in show.client.iter_participants(
            show.chat_id, filter=ChannelParticipantsAdmins
        ):
            if not user.deleted:
                link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
                mentions += f"\n✧ {link}"
            else:
                mentions += f"\n⍟ ᴀᴋᴜɴ ᴛᴇʀʜᴀᴘᴜꜱ <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += f" {str(err)}" + "\n"
    await show.edit(mentions, parse_mode="html")


@ayiinCmd(pattern="pin( loud|$)")
async def pin(event):
    to_pin = event.reply_to_msg_id
    if not to_pin:
        return await eor(event, "`ʙᴀʟᴀꜱ ᴘᴇꜱᴀɴ ᴜɴᴛᴜᴋ ᴍᴇʟᴀᴋᴜᴋᴀɴ ᴘᴇɴʏᴇᴍᴀᴛᴀɴ.`", time=30)
    options = event.pattern_match.group(1)
    is_silent = bool(options)
    try:
        await event.client.pin_message(event.chat_id, to_pin, notify=is_silent)
    except BadRequestError:
        return await eod(event, "**ᴛɪᴅᴀᴋ ᴍᴇᴍᴘᴜɴʏᴀɪ ɪᴢɪɴ!**", time=5)
    except Exception as e:
        return await eod(event, "**ᴋᴇꜱᴀʟᴀʜᴀɴ : **`{}`".format(e), time=5)
    await eor(event, "`ᴘᴇꜱᴀɴ ʙᴇʀʜᴀꜱɪʟ ᴅɪꜱᴇᴍᴀᴛᴋᴀɴ!`")


@ayiinCmd(pattern="unpin( all|$)")
async def pin(event):
    to_unpin = event.reply_to_msg_id
    options = (event.pattern_match.group(1)).strip()
    if not to_unpin and options != "all":
        return await eor(
            event,
            f"**ʙᴀʟᴀꜱ ᴋᴇ ᴘᴇꜱᴀɴ ᴜɴᴛᴜᴋ ᴍᴇʟᴇᴘᴀꜱ ᴘɪɴ ᴀᴛᴀᴜ ɢᴜɴᴀᴋᴀɴ** `{cmd}unpin all` **ᴜɴᴛᴜᴋ ᴍᴇʟᴇᴘᴀꜱ ꜱᴇᴍᴜᴀ ᴘɪɴ**",
            time=20,
        )
    try:
        if to_unpin and not options:
            await event.client.unpin_message(event.chat_id, to_unpin)
            await eor(event, "`ʙᴇʀʜᴀꜱɪʟ ᴍᴇɴɢʜᴀᴘᴜꜱ ᴘᴇꜱᴀɴ ꜱᴇᴍᴀᴛᴀɴ!`")
        elif options == "all":
            await event.client.unpin_message(event.chat_id)
            await eor(event, "`ʙᴇʀʜᴀꜱɪʟ ᴍᴇɴɢʜᴀᴘᴜꜱ ꜱᴇᴍᴜᴀ ᴘᴇꜱᴀɴ ꜱᴇᴍᴀᴛᴀɴ!`")
        else:
            return await eor(
                event,
                f"**ʙᴀʟᴀꜱ ᴋᴇ ᴘᴇꜱᴀɴ ᴜɴᴛᴜᴋ ᴍᴇʟᴇᴘᴀꜱ ᴘɪɴ ᴀᴛᴀᴜ ɢᴜɴᴀᴋᴀɴ** `{cmd}unpin all`",
                time=20,
            )
    except BadRequestError:
        return await eor(event, "**ᴛɪᴅᴀᴋ ᴍᴇᴍᴘᴜɴʏᴀɪ ɪᴢɪɴ!**", time=10)
    except Exception as e:
        return await eor(event, "**ᴋᴇꜱᴀʟᴀʜᴀɴ : **`{}`".format(e), time=10)


@ayiinCmd(pattern="kick(?: |$)(.*)", only="groups")
async def kick(usr):
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        return await eor(usr, "**ɢᴀɢᴀʟ ᴅɪᴋᴀʀᴇɴᴀᴋᴀɴ ʙᴜᴋᴀɴ ᴀᴅᴍɪɴ.**")
    user, reason = await ayiin.getUserFromEvent(usr)
    if not user:
        return await eor(usr, "**ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇɴᴇᴍᴜᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ.**")
    xxnx = await eor(usr, '**ᴍᴇᴍᴘʀᴏꜱᴇꜱ...**')
    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(0.5)
    except Exception as e:
        noperm = "**ᴛɪᴅᴀᴋ ᴍᴇᴍᴘᴜɴʏᴀɪ ɪᴢɪɴ!**" + "\n" + e
        return await eod(usr, noperm)
    if reason:
        await xxnx.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **ᴛᴇʟᴀʜ ᴅɪᴋɪᴄᴋ ᴅᴀʀɪ ɢʀᴜᴘ**\n**ᴀʟᴀꜱᴀɴ:** `{reason}`"
        )
    else:
        await xxnx.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **ᴛᴇʟᴀʜ ᴅɪᴋɪᴄᴋ ᴅᴀʀɪ ɢʀᴜᴘ.**"
        )


@ayiinCmd(pattern=r"undlt( -u)?(?: |$)(\d*)?")
async def _iundlt(event):
    catevent = await eor(event, "`ᴍᴇɴᴄᴀʀɪ ᴛɪɴᴅᴀᴋᴀɴ ᴛᴇʀʙᴀʀᴜ...`")
    flag = event.pattern_match.group(1)
    if event.pattern_match.group(2) != "":
        lim = int(event.pattern_match.group(2))
        if lim > 15:
            lim = int(15)
        if lim <= 0:
            lim = int(1)
    else:
        lim = int(5)
    adminlog = await event.client.get_admin_log(
        event.chat_id,
        limit=lim,
        edit=False,
        delete=True
    )
    deleted_msg = f"**{lim} ᴘᴇꜱᴀɴ ʏᴀɴɢ ᴅɪʜᴀᴘᴜꜱ ᴅɪ ɢʀᴜᴘ ɪɴɪ:**"
    if not flag:
        for msg in adminlog:
            ruser: User = (
                await event.client(
                    GetFullUserRequest(
                        msg.old.from_id.user_id
                    )
                )
            ).users[0]
            _media_type = media_type(msg.old)
            mention = ayiin.mentionuser(
                ruser.first_name,
                ruser.id
            )
            if _media_type is None:
                deleted_msg += f"\n☞ __{msg.old.message}__ **ᴅɪᴋɪʀɪᴍ ᴏʟᴇʜ** {mention}"
            else:
                deleted_msg += f"\n☞ __{_media_type}__ **ᴅɪᴋɪʀɪᴍ ᴏʟᴇʜ** {mention}"
        await eor(catevent, deleted_msg)
    else:
        main_msg = await eor(catevent, deleted_msg)
        for msg in adminlog:
            ruser: User = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).users[0]
            _media_type = media_type(msg.old)
            ment = ayiin.mentionuser(
                ruser.first_name,
                ruser.id
            )
            if _media_type is None:
                await main_msg.reply(
                    f"`{msg.old.message}`\n**ᴅɪᴋɪʀɪᴍ ᴏʟᴇʜ** {ment}"
                )
            else:
                await main_msg.reply(
                    f"`{msg.old.message}`\n**ᴅɪᴋɪʀɪᴍ ᴏʟᴇʜ** {ment}",
                    file=msg.old.media,
                )


cmdHelp.update(
    {
        "ᴀᴅᴍɪɴ": f"**ᴘʟᴜɢɪɴ : **`ᴀᴅᴍɪɴ`\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}promote <ᴜꜱᴇʀɴᴀᴍᴇ/ʀᴇᴘʟʏ> <ɴᴀᴍᴀ ᴛɪᴛʟᴇ (ᴏᴘᴛɪᴏɴᴀʟ)>`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴍᴇᴍᴘʀᴏᴍᴏꜱɪᴋᴀɴ ᴍᴇᴍʙᴇʀ ꜱᴇʙᴀɢᴀɪ ᴀᴅᴍɪɴ.\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}demote <ᴜꜱᴇʀɴᴀᴍᴇ/ʙᴀʟᴀꜱ ᴋᴇ ᴘᴇꜱᴀɴ>`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴍᴇɴᴜʀᴜɴᴋᴀɴ ᴀᴅᴍɪɴ ꜱᴇʙᴀɢᴀɪ ᴍᴇᴍʙᴇʀ.\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}ban <ᴜꜱᴇʀɴᴀᴍᴇ/ʙᴀʟᴀꜱ ᴋᴇ ᴘᴇꜱᴀɴ> <ᴀʟᴀꜱᴀɴ (ᴏᴘᴛɪᴏɴᴀʟ)>`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴍᴇᴍʙᴀɴɴᴇᴅ ᴘᴇɴɢɢᴜɴᴀ ᴅᴀʀɪ ɢʀᴜᴘ.\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}unban <ᴜꜱᴇʀɴᴀᴍᴇ/ʀᴇᴘʟʏ>`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴜɴʙᴀɴɴᴇᴅ ᴘᴇɴɢɢᴜɴᴀ ᴊᴀᴅɪ ʙɪꜱᴀ ᴊᴏɪɴ ɢʀᴜᴘ ʟᴀɢɪ.\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}mute <ᴜꜱᴇʀɴᴀᴍᴇ/ʀᴇᴘʟʏ> <ᴀʟᴀꜱᴀɴ (ᴏᴘᴛɪᴏɴᴀʟ)>`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴍᴇᴍʙɪꜱᴜᴋᴀɴ ꜱᴇꜱᴇᴏʀᴀɴɢ ᴅɪ ɢʀᴜᴘ, ʙɪꜱᴀ ᴋᴇ ᴀᴅᴍɪɴ ᴊᴜɢᴀ.\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}unmute <ᴜꜱᴇʀɴᴀᴍᴇ/ʀᴇᴘʟʏ>`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴍᴇᴍʙᴜᴋᴀ ʙɪꜱᴜ ᴏʀᴀɴɢ ʏᴀɴɢ ᴅɪʙɪꜱᴜᴋᴀɴ.\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : ** ᴍᴇᴍʙᴜᴋᴀ ɢʟᴏʙᴀʟ ᴍᴜᴛᴇ ᴏʀᴀɴɢ ʏᴀɴɢ ᴅɪʙɪꜱᴜᴋᴀɴ.\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}all`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴛᴀɢ ꜱᴇᴍᴜᴀ ᴍᴇᴍʙᴇʀ ᴅᴀʟᴀᴍ ɢʀᴜᴘ.\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}admins`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴍᴇʟɪʜᴀᴛ ᴅᴀꜰᴛᴀʀ ᴀᴅᴍɪɴ ᴅɪ ɢʀᴜᴘ.\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}setgpic <ꜰʟᴀɢꜱ> <ʙᴀʟᴀꜱ ᴋᴇ ɢᴀᴍʙᴀʀ>`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜʙᴀʜ ꜰᴏᴛᴏ ᴘʀᴏꜰɪʟ ɢʀᴜᴘ ᴀᴛᴀᴜ ᴍᴇɴɢʜᴀᴘᴜꜱ ɢᴀᴍʙᴀʀ ꜰᴏᴛᴏ ᴘʀᴏꜰɪʟ ɢʀᴜᴘ.\
        \n  •  **ꜰʟᴀɢꜱ :** `-s` = **ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜʙᴀʜ ꜰᴏᴛᴏ ɢʀᴜᴘ** ᴀᴛᴀᴜ `-d` = **ᴜɴᴛᴜᴋ ᴍᴇɴɢʜᴀᴘᴜꜱ ꜰᴏᴛᴏ ɢʀᴜᴘ**\
    "
    }
)


cmdHelp.update(
    {
        "ᴘɪɴ": f"**ᴘʟᴜɢɪɴ : **`ᴘɪɴ`\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}pin` <ʀᴇᴘʟʏ ᴄʜᴀᴛ>\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴜɴᴛᴜᴋ ᴍᴇɴʏᴇᴍᴀᴛᴋᴀɴ ᴘᴇꜱᴀɴ ᴅᴀʟᴀᴍ ɢʀᴜᴘ.\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}pin loud` <ʀᴇᴘʟʏ ᴄʜᴀᴛ>\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴜɴᴛᴜᴋ ᴍᴇɴʏᴇᴍᴀᴛᴋᴀɴ ᴘᴇꜱᴀɴ ᴅᴀʟᴀᴍ ɢʀᴜᴘ (ᴛᴀɴᴘᴀ ɴᴏᴛɪꜰɪᴋᴀꜱɪ) / ᴍᴇɴʏᴇᴍᴀᴛᴋᴀɴ ꜱᴇᴄᴀʀᴀ ᴅɪᴀᴍ ᴅɪᴀᴍ.\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}unpin` <ʀᴇᴘʟʏ ᴄʜᴀᴛ>\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴜɴᴛᴜᴋ ᴍᴇʟᴇᴘᴀꜱᴋᴀɴ ᴘɪɴ ᴘᴇꜱᴀɴ ᴅᴀʟᴀᴍ ɢʀᴜᴘ.\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}unpin all`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴜɴᴛᴜᴋ ᴍᴇʟᴇᴘᴀꜱᴋᴀɴ ꜱᴇᴍᴜᴀ ꜱᴇᴍᴀᴛᴀɴ ᴘᴇꜱᴀɴ ᴅᴀʟᴀᴍ ɢʀᴜᴘ.\
    "
    }
)


cmdHelp.update(
    {
        "ᴜɴᴅᴇʟᴇᴛᴇ": f"**ᴘʟᴜɢɪɴ : **`ᴜɴᴅᴇʟᴇᴛᴇ`\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}undlt` <ᴊᴜᴍʟᴀʜ ᴄʜᴀᴛ>\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴜɴᴛᴜᴋ ᴍᴇɴᴅᴀᴘᴀᴛᴋᴀɴ ᴘᴇꜱᴀɴ ʏᴀɴɢ ᴅɪʜᴀᴘᴜꜱ ʙᴀʀᴜ-ʙᴀʀᴜ ɪɴɪ ᴅɪ ɢʀᴜᴘ\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}undlt -u` <ᴊᴜᴍʟᴀʜ ᴄʜᴀᴛ>\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴜɴᴛᴜᴋ ᴍᴇɴᴅᴀᴘᴀᴛᴋᴀɴ ᴘᴇꜱᴀɴ ᴍᴇᴅɪᴀ ʏᴀɴɢ ᴅɪʜᴀᴘᴜꜱ ʙᴀʀᴜ-ʙᴀʀᴜ ɪɴɪ ᴅɪ ɢʀᴜᴘ\
        \n  •  **ꜰʟᴀɢꜱ :** `-u` = **ɢᴜɴᴀᴋᴀɴ ꜰʟᴀɢꜱ ɪɴɪ ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜɴɢɢᴀʜ ᴍᴇᴅɪᴀ.**\
        \n\n  •  **ɴᴏᴛᴇ : ᴍᴇᴍʙᴜᴛᴜʜᴋᴀɴ ʜᴀᴋ ᴀᴅᴍɪɴ ɢʀᴜᴘ** \
    "
    }
)


cmdHelp.update(
    {
        "ɢᴍᴜᴛᴇ": f"**ᴘʟᴜɢɪɴ : **`ɢᴍᴜᴛᴇ`\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}gmute` <ᴜꜱᴇʀɴᴀᴍᴇ/ʀᴇᴘʟʏ> <ᴀʟᴀꜱᴀɴ (ᴏᴘᴛɪᴏɴᴀʟ)>\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴜɴᴛᴜᴋ ᴍᴇᴍʙɪꜱᴜᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ ᴅɪ ꜱᴇᴍᴜᴀ ɢʀᴜᴘ ʏᴀɴɢ ᴋᴀᴍᴜ ᴀᴅᴍɪɴ.\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}ungmute` <ᴜꜱᴇʀɴᴀᴍᴇ/ʀᴇᴘʟʏ>\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴋᴀ ɢʟᴏʙᴀʟ ᴍᴜᴛᴇ ᴘᴇɴɢɢᴜɴᴀ ᴅɪ ꜱᴇᴍᴜᴀ ɢʀᴜᴘ ʏᴀɴɢ ᴋᴀᴍᴜ ᴀᴅᴍɪɴ.\
    "
    }
)


cmdHelp.update(
    {
        "ᴢᴏᴍʙɪᴇꜱ": f"**ᴘʟᴜɢɪɴ : **`ᴢᴏᴍʙɪᴇꜱ`\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}zombies`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴜɴᴛᴜᴋ ᴍᴇɴᴄᴀʀɪ ᴀᴋᴜɴ ᴛᴇʀʜᴀᴘᴜꜱ ᴅᴀʟᴀᴍ ɢʀᴜᴘ\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}zombies clean`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴜɴᴛᴜᴋ ᴍᴇɴɢʜᴀᴘᴜꜱ ᴀᴋᴜɴ ᴛᴇʀʜᴀᴘᴜꜱ ᴅᴀʀɪ ɢʀᴜᴘ.\
    "
    }
)
