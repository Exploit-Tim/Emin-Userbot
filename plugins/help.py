# Copyright (C) 2020 TeamDerUntergang.
#
# SedenUserBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SedenUserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# @Qulec tarafından yazılmıştır.
# Thanks @Spechide.

from telethon.errors.rpcerrorlist import BotInlineDisabledError as noinline
from telethon.errors.rpcerrorlist import BotResponseTimeoutError as timout
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest

from pyAyiin import ayiin, cmdHelp
from pyAyiin.database.handler import getHandler
from pyAyiin.decorator import ayiinCmd
from pyAyiin.utils import eod, eor


@ayiinCmd(pattern="help(?: |$)(.*)")
async def helpyins(event):
    xx = await eor(event, "✨")
    cmd = getHandler()
    if event.fwd_from:
        return
    args = event.pattern_match.group(1).lower()
    if args:
        if args in cmdHelp:
            await xx.edit(f"{cmdHelp[args]}\n\n© Emin")
        else:
            await eod(
                xx,
                f"**ᴍᴏᴅᴜʟ {args} ᴛɪᴅᴀᴋ ᴅɪᴋᴇᴛᴀʜᴜɪ**, **ꜱɪʟᴀʜᴋᴀɴ ᴋᴇᴛɪᴋ {cmd}help ᴜɴᴛᴜᴋ ᴍᴇʟɪʜᴀᴛ ᴍᴏᴅᴜʟ.**"
            )
    else:
        if ayiin.bot.me.username is not None:
            chat = "@Botfather"
            try:
                results = await event.client.inline_query(
                    ayiin.bot.me.username,
                    "@eminsupport"
                )
                await results[0].click(
                    event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
                )
                await xx.delete()
            except timout:
                return await xx.edit(
                    f"ʙᴏᴛ ᴛɪᴅᴀᴋ ᴍᴇɴᴀɴɢɢᴀᴘɪ ɪɴʟɪɴᴇ ᴋᴜᴇʀɪ.\nꜱɪʟᴀʜᴋᴀɴ ᴋᴇᴛɪᴋ `{cmd}restart`"
                )
            except noinline:
                await xx.edit(
                    "**ɪɴʟɪɴᴇ ᴍᴏᴅᴇ ᴛɪᴅᴀᴋ ᴀᴋᴛɪꜰ.**\n__ꜱᴇᴅᴀɴɢ ᴍᴇɴʏᴀʟᴀᴋᴀɴɴʏᴀ, ʜᴀʀᴀᴘ ᴛᴜɴɢɢᴜ ꜱᴇʙᴇɴᴛᴀʀ...__",
                )
                async with event.client.conversation(chat) as conv:
                    try:
                        first = await conv.send_message("/setinline")
                        second = await conv.get_response()
                        third = await conv.send_message(ayiin.bot.me.username)
                        fourth = await conv.get_response()
                        fifth = await conv.send_message("Search")
                        sixth = await conv.get_response()
                        await event.client.send_read_acknowledge(conv.chat_id)
                    except YouBlockedUserError:
                        await event.client(UnblockRequest(chat))
                        first = await conv.send_message("/setinline")
                        second = await conv.get_response()
                        third = await conv.send_message(ayiin.bot.me.username)
                        fourth = await conv.get_response()
                        fifth = await conv.send_message("Search")
                        sixth = await conv.get_response()
                        await event.client.send_read_acknowledge(conv.chat_id)
                    await xx.edit(
                        f"**ʙᴇʀʜᴀꜱɪʟ ᴍᴇɴʏᴀʟᴀᴋᴀɴ ᴍᴏᴅᴇ ɪɴʟɪɴᴇ**\n\n**ᴋᴇᴛɪᴋ** `{cmd}help` **ʟᴀɢɪ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴋᴀ ᴍᴇɴᴜ ʙᴀɴᴛᴜᴀɴ.**"
                    )
                await event.client.delete_messages(
                    conv.chat_id,
                    [first.id, second.id, third.id, fourth.id, fifth.id, sixth.id],
                )
        else:
            await xx.edit(
                "**ꜱɪʟᴀʜᴋᴀɴ ʙᴜᴀᴛ ʙᴏᴛ ᴅɪ @BotFather ᴅᴀɴ ᴛᴀᴍʙᴀʜᴋᴀɴ ᴠᴀʀ** `BOT_TOKEN` & `BOT_USERNAME`",
            )
