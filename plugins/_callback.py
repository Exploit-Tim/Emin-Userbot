import random
import re

from telethon import Button
from telethon.sync import custom, events
from telethon.tl.types import InputWebDocument

from pyAyiin import ayiin, cmdHelp
from pyAyiin.database.handler import getHandler
from pyAyiin.database.sudo import getSudo



BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\<buttonurl:(?:/{0,2})(.+?)(:same)?\>)")


main_help_button = [
    [
        Button.inline("•• ᴘʟᴜɢɪɴ ••", data="reopen"),
        Button.inline("ᴍᴇɴᴜ ᴠᴄ ••", data="inline_yins"),
    ],
    [
        Button.inline("⚙️ ᴀʟᴀᴛ ᴘᴇᴍɪʟɪᴋ", data="yins_langs"),
        Button.url("ᴘᴇɴɢᴀᴛᴜʀᴀɴ ⚙️", url=f"t.me/{ayiin.bot.me.username}?start="),
    ],
    [Button.inline("•• ᴋᴇᴍʙᴀʟɪ ••", data="close")],
]


@ayiin.bot.on(
    events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(rb"reopen")
    )
)
async def on_plug_in_callback_query_handler(event):
    sudoer = getSudo()
    logoyins = random.choice(
        [
            "assets/inline1.png",
            "assets/inline2.png",
            "assets/inline3.png"
        ]
    )
    if event.query.user_id == ayiin.me.id or event.query.user_id in sudoer:
        buttons = ayiin.paginateHelp(0, cmdHelp, "helpme")
        text = f"**✨ ᴇᴍɪɴ-ᴜsᴇʀʙᴏᴛ ɪɴʟɪɴᴇ ᴍᴇɴᴜ ✨**\n\n⍟ **ᴅᴇᴘʟᴏʏ :** •[{ayiin._host}]•\n⍟ **ᴏᴡɴᴇʀ** {ayiin.me.first_name}\n⍟ **ᴊᴜᴍʟᴀʜ :** {len(cmdHelp)} **Modules**"
        await event.edit(
            text,
            file=logoyins,
            buttons=buttons,
            link_preview=False,
        )
    else:
        reply_pop_up_alert = f"ᴋᴀᴍᴜ ᴛɪᴅᴀᴋ ᴅɪɪᴢɪɴᴋᴀɴ, ɪɴɪ ᴜꜱᴇʀʙᴏᴛ ᴍɪʟɪᴋ {ayiin.me.first_name}"
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


@ayiin.bot.on(events.InlineQuery)
async def inline_handler(event):
    builder = event.builder
    result = None
    query = event.text
    logoyins = random.choice(
        [
            "assets/inline1.png",
            "assets/inline2.png",
            "assets/inline3.png"
        ]
    )
    botusername = ayiin.bot.me.username
    if event.query.user_id == ayiin.me.id and query.startswith(
            "@EminSupport"):
        buttons = ayiin.paginateHelp(0, cmdHelp, "helpme")
        result = await event.builder.photo(
            file=logoyins,
            link_preview=False,
            text=f"**✨ ᴇᴍɪɴ-ᴜsᴇʀʙᴏᴛ ɪɴʟɪɴᴇ ᴍᴇɴᴜ ✨**\n\n⍟ **ᴅᴇᴘʟᴏʏ :** •[{ayiin._host}]•\n⍟ **ᴏᴡɴᴇʀ :** {ayiin.me.first_name}\n⍟ **ᴊᴜᴍʟᴀʜ :** {len(cmdHelp)} **Modules**",
            buttons=main_help_button,
        )
    elif query.startswith("repo"):
        result = builder.article(
            title="Repository",
            description="Repository Emin - Userbot",
            url="https://t.me/grupmedia",
            thumb=InputWebDocument(
                logoyins,
                0,
                "image/jpeg",
                []),
            text="**Emin-Userbot**\n➖➖➖➖➖➖➖➖➖➖\n✧  **ʀᴇᴘᴏ :** [iniemin](https://t.me/iniemin)\n✧ **sᴜᴘᴘᴏʀᴛ :** @EminSupport\n✧ **ʀᴇᴘᴏsɪᴛᴏʀʏ :** [Emin-Userbot](https://github.com/Rans33281/Emin-Userbot)\n➖➖➖➖➖➖➖➖➖➖",
            buttons=[
                [
                    custom.Button.url(
                        "ɢʀᴏᴜᴘ",
                        "https://t.me/grupmedia"),
                    custom.Button.url(
                        "ʀᴇᴘᴏ",
                        "https://github.com/Rans33281/Emin-Userbot"),
                ],
            ],
            link_preview=False,
        )
    elif query.startswith("Inline buttons"):
        markdown_note = query[14:]
        prev = 0
        note_data = ""
        buttons = []
        for match in BTN_URL_REGEX.finditer(markdown_note):
            n_escapes = 0
            to_check = match.start(1) - 1
            while to_check > 0 and markdown_note[to_check] == "\\":
                n_escapes += 1
                to_check -= 1
            if n_escapes % 2 == 0:
                buttons.append(
                    (match.group(2), match.group(3), bool(
                        match.group(4))))
                note_data += markdown_note[prev: match.start(1)]
                prev = match.end(1)
            elif n_escapes % 2 == 1:
                note_data += markdown_note[prev:to_check]
                prev = match.start(1) - 1
            else:
                break
        else:
            note_data += markdown_note[prev:]
        message_text = note_data.strip()
        tl_ib_buttons = ayiin.buildKeyboard(buttons)
        result = builder.article(
            title="Inline creator",
            text=message_text,
            buttons=tl_ib_buttons,
            link_preview=False,
        )
    else:
        result = builder.article(
            title="✨ ᴇᴍɪɴ-ᴜsᴇʀʙᴏᴛ ✨",
            description="Emin - Userbot | Telethon",
            url="https://t.me/EminSupport",
            thumb=InputWebDocument(
                logoyins,
                0,
                "image/jpeg",
                []),
            text=f"**Emin-Userbot**\n➖➖➖➖➖➖➖➖➖➖\n✧ **ᴏᴡɴᴇʀ :** [{ayiin.me.first_name}](tg://user?id={ayiin.me.id})\n✧ **ᴀssɪsᴛᴀɴᴛ:** {botusername}\n➖➖➖➖➖➖➖➖➖➖\n**ᴜᴘᴅᴀᴛᴇs :** @EminSupport\n➖➖➖➖➖➖➖➖➖➖",
            buttons=[
                [
                    custom.Button.url(
                        "ɢʀᴏᴜᴘ",
                        "https://t.me/grupmedia"),
                    custom.Button.url(
                        "ʀᴇᴘᴏ",
                        "https://github.com/Rans33281/Emin-Userbot"),
                ],
            ],
            link_preview=False,
        )
    await event.answer(
        [result], switch_pm="👥 USERBOT PORTAL", switch_pm_param="start"
    )

@ayiin.bot.on(
    events.callbackquery.CallbackQuery(
        data=re.compile(rb"helpme_next\((.+?)\)")
    )
)
async def on_plug_in_callback_query_handler(event):
    sudoer = getSudo()

    if event.query.user_id == ayiin.me.id or event.query.user_id in sudoer:
        current_page_number = int(
            event.data_match.group(1).decode("UTF-8"))
        buttons = ayiin.paginateHelp(
            current_page_number + 1, cmdHelp, "helpme")
        await event.edit(buttons=buttons)
    else:
        reply_pop_up_alert = (
            f"ᴋᴀᴍᴜ ᴛɪᴅᴀᴋ ᴅɪɪᴢɪɴᴋᴀɴ, ɪɴɪ ᴜꜱᴇʀʙᴏᴛ ᴍɪʟɪᴋ {ayiin.me.first_name}"
        )
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

@ayiin.bot.on(
    events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(rb"helpme_close\((.+?)\)")
    )
)
async def on_plug_in_callback_query_handler(event):
    sudoer = getSudo()
    logoyins = random.choice(
        [
            "assets/inline1.png",
            "assets/inline2.png",
            "assets/inline3.png"
        ]
    )
    if event.query.user_id == ayiin.me.id or event.query.user_id in sudoer:  # @Kyy-Userbot
        # https://t.me/TelethonChat/115200
        await event.edit(
            file=logoyins,
            link_preview=True,
            buttons=main_help_button)

@ayiin.bot.on(
    events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(rb"gcback")
    )
)
async def gback_handler(event):
    sudoer = getSudo()
    logoyins = random.choice(
        [
            "assets/inline1.png",
            "assets/inline2.png",
            "assets/inline3.png"
        ]
    )
    if event.query.user_id == ayiin.me.id or event.query.user_id in sudoer:  # @Ayiin-Userbot
        # https://t.me/TelethonChat/115200
        text = (
            f"**✨ ᴇᴍɪɴ-ᴜsᴇʀʙᴏᴛ ɪɴʟɪɴᴇ ᴍᴇɴᴜ ✨**\n\n✧ **ᴏᴡɴᴇʀ :** [{ayiin.me.first_name}](tg://user?id={ayiin.me.id})\n✧ **ᴊᴜᴍʟᴀʜ :** {len(cmdHelp)} **ᴍᴏᴅᴜʟᴇꜱ**")
        await event.edit(
            text,
            file=logoyins,
            link_preview=True,
            buttons=main_help_button)


@ayiin.bot.on(events.CallbackQuery(data=b"inline_yins"))
async def about(event):
    sudoer = getSudo()

    if event.query.user_id == ayiin.me.id or event.query.user_id in sudoer:
        await event.edit(f"""
•Menu• - Voice chat group untuk [{ayiin.me.first_name}](tg://user?id={ayiin.me.id})
""",
                            buttons=[
                                [
                                    Button.inline("⍟ ᴠᴄ ᴘʟᴜɢɪɴ ⍟",
                                                data="vcplugin"),
                                    Button.inline("⍟ ᴠᴄ ᴛᴏᴏʟs ⍟",
                                                data="vctools")],
                                [custom.Button.inline(
                                    "ʙᴀᴄᴋ", data="gcback")],
                            ]
                            )
    else:
        reply_pop_up_alert = f"❌ 𝗗𝗜𝗦𝗖𝗟𝗔𝗜𝗠𝗘𝗥 ❌\n\nᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴍᴇᴍᴘᴜɴʏᴀɪ ʜᴀᴋ ᴜɴᴛᴜᴋ ᴍᴇɴᴇᴋᴀɴ ᴛᴏᴍʙᴏʟ ɪɴɪ"
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

@ayiin.bot.on(
    events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(rb"vcplugin")
    )
)
async def on_plug_in_callback_query_handler(event):
    sudoer = getSudo()
    cmd = getHandler()

    if event.query.user_id == ayiin.me.id or event.query.user_id in sudoer:
        text = (
            f"""
✘ **ᴘᴇʀɪɴᴛᴀʜ ʏᴀɴɢ ᴛᴇʀꜱᴇᴅɪᴀ ᴅɪ ᴠᴄᴘʟᴜɢɪɴ** ✘

»  **ᴘᴇʀɪɴᴛᴀʜ : **`{cmd}play` <ᴊᴜᴅᴜʟ ʟᴀɢᴜ/ʟɪɴᴋ ʏᴛ>
»  **ᴋᴇɢᴜɴᴀᴀɴ :** __ᴜɴᴛᴜᴋ ᴍᴇᴍᴜᴛᴀʀ ʟᴀɢᴜ ᴅɪ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ɢʀᴏᴜᴘ ᴅᴇɴɢᴀɴ ᴀᴋᴜɴ ᴋᴀᴍᴜ.__

»  **ᴘᴇʀɪɴᴛᴀʜ : **`{cmd}vplay` <ᴊᴜᴅᴜʟ ᴠɪᴅᴇᴏ/ʟɪɴᴋ ʏᴛ>
»  **ᴋᴇɢᴜɴᴀᴀɴ :** __ᴜɴᴛᴜᴋ ᴍᴇᴍᴜᴛᴀʀ ᴠɪᴅᴇᴏ ᴅɪ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ɢʀᴏᴜᴘ ᴅᴇɴɢᴀɴ ᴀᴋᴜɴ ᴋᴀᴍᴜ.__

»  **ᴘᴇʀɪɴᴛᴀʜ : **`{cmd}end`
»  **ᴋᴇɢᴜɴᴀᴀɴ :** __ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴇʀʜᴇɴᴛɪᴋᴀɴ ᴠɪᴅᴇᴏ/ʟᴀɢᴜ ʏᴀɴɢ ꜱᴇᴅᴀɴɢ ᴘᴜᴛᴀʀ ᴅɪ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ɢʀᴏᴜᴘ.__

»  **ᴘᴇʀɪɴᴛᴀʜ : **`{cmd}skip`
»  **ᴋᴇɢᴜɴᴀᴀɴ :** __ᴜɴᴛᴜᴋ ᴍᴇʟᴇᴡᴀᴛɪ ᴠɪᴅᴇᴏ/ʟᴀɢᴜ ʏᴀɴɢ ꜱᴇᴅᴀɴɢ ᴅɪ ᴘᴜᴛᴀʀ.__

»  **ᴘᴇʀɪɴᴛᴀʜ : **`{cmd}pause`
»  **ᴋᴇɢᴜɴᴀᴀɴ :** __ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴇʀʜᴇɴᴛɪᴋᴀɴ ᴠɪᴅᴇᴏ/ʟᴀɢᴜ ʏᴀɴɢ ꜱᴇᴅᴀɴɢ ᴅɪᴘᴜᴛᴀʀ.__

»  **ᴘᴇʀɪɴᴛᴀʜ : **`{cmd}resume`
»  **ᴋᴇɢᴜɴᴀᴀɴ :** __ᴜɴᴛᴜᴋ ᴍᴇʟᴀɴᴊᴜᴛᴋᴀɴ ᴘᴇᴍᴜᴛᴀʀᴀɴ ᴠɪᴅᴇᴏ/ʟᴀɢᴜ ʏᴀɴɢ ꜱᴇᴅᴀɴɢ ᴅɪᴘᴜᴛᴀʀ.__

»  **ᴘᴇʀɪɴᴛᴀʜ : **`{cmd}volume` 1-200
»  **ᴋᴇɢᴜɴᴀᴀɴ :** __Uᴜɴᴛᴜᴋ ᴍᴇɴɢᴜʙᴀʜ ᴠᴏʟᴜᴍᴇ (ᴍᴇᴍʙᴜᴛᴜʜᴋᴀɴ ʜᴀᴋ ᴀᴅᴍɪɴ).__

»  **ᴘᴇʀɪɴᴛᴀʜ : **`{cmd}playlist`
»  **ᴋᴇɢᴜɴᴀᴀɴ :** __ᴜɴᴛᴜᴋ ᴍᴇɴᴀᴍᴘɪʟᴋᴀɴ ᴅᴀꜰᴛᴀʀ ᴘᴜᴛᴀʀ ʟᴀɢᴜ/ᴠɪᴅᴇᴏ.__
""")
        logoyins = random.choice(
            [
                "assets/inline1.png",
                "assets/inline2.png",
                "assets/inline3.png"
            ]
        )
        await event.edit(
            text,
            file=logoyins,
            link_preview=True,
            buttons=[Button.inline("ʙᴀᴄᴋ", data="inline_yins")])
    else:
        reply_pop_up_alert = f"❌ 𝗗𝗜𝗦𝗖𝗟𝗔𝗜𝗠𝗘𝗥 ❌\n\nᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴍᴇᴍᴘᴜɴʏᴀɪ ʜᴀᴋ ᴜɴᴛᴜᴋ ᴍᴇɴᴇᴋᴀɴ ᴛᴏᴍʙᴏʟ ɪɴɪ"
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

@ayiin.bot.on(
    events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(rb"vctools")
    )
)
async def on_plug_in_callback_query_handler(event):
    sudoer = getSudo()
    cmd = getHandler()
    if event.query.user_id == ayiin.me.id or event.query.user_id in sudoer:
        text = (
            f"""
✘ **ᴘᴇʀɪɴᴛᴀʜ ʏᴀɴɢ ᴛᴇʀꜱᴇᴅɪᴀ ᴅɪ ᴠᴄᴛᴏᴏʟꜱ** ✘

»  **ᴘᴇʀɪɴᴛᴀʜ : **`{cmd}startvc`
»  **ᴋᴇɢᴜɴᴀᴀɴ :** __ᴜɴᴛᴜᴋ ᴍᴇᴍᴜʟᴀɪ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ɢʀᴏᴜᴘ.__

»  **ᴘᴇʀɪɴᴛᴀʜ : **`{cmd}stopvc`
»  **ᴋᴇɢᴜɴᴀᴀɴ :** __ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴇʀʜᴇɴᴛɪᴋᴀɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ɢʀᴏᴜᴘ.__

»  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}joinvc`
»  **ᴋᴇɢᴜɴᴀᴀɴ :** __Untuk Bergabung ke voice chat group.__

»  **ᴘᴇʀɪɴᴛᴀʜ : **`{cmd}leavevc`
»  **ᴋᴇɢᴜɴᴀᴀɴ :** __Untuk Turun dari voice chat group.__

»  **ᴘᴇʀɪɴᴛᴀʜ : **`{cmd}vctitle` <ᴛɪᴛʟᴇ ᴠᴄɢ>
»  **ᴋᴇɢᴜɴᴀᴀɴ :** __ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜʙᴀʜ ᴛɪᴛʟᴇ/ᴊᴜᴅᴜʟ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ɢʀᴏᴜᴘ.__

»  **ᴘᴇʀɪɴᴛᴀʜ : **`{cmd}vcinvite`
»  **ᴋᴇɢᴜɴᴀᴀɴ :** __ᴍᴇɴɢᴜɴᴅᴀɴɢ ᴍᴇᴍʙᴇʀ ɢʀᴏᴜᴘ ᴋᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ɢʀᴏᴜᴘ.__
""")
        logoyins = random.choice(
            [
                "assets/inline1.png",
                "assets/inline2.png",
                "assets/inline3.png"
            ]
        )
        await event.edit(
            text,
            file=logoyins,
            link_preview=True,
            buttons=[Button.inline("ʙᴀᴄᴋ", data="inline_yins")])
    else:
        reply_pop_up_alert = f"❌ 𝗗𝗜𝗦𝗖𝗟𝗔𝗜𝗠𝗘𝗥 ❌\n\nᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴍᴇᴍᴘᴜɴʏᴀɪ ʜᴀᴋ ᴜɴᴛᴜᴋ ᴍᴇɴᴇᴋᴀɴ ᴛᴏᴍʙᴏʟ ɪɴɪ"
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


@ayiin.bot.on(
    events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(rb"yins_langs")
    )
)
async def on_plug_in_callback_query_handler(event):
    sudoer = getSudo()
    cmd = getHandler()

    if event.query.user_id == ayiin.me.id or event.query.user_id in sudoer:
        text = (
            f"""
✘ **ᴘᴇʀɪɴᴛᴀʜ ʏᴀɴɢ ᴛᴇʀꜱᴇᴅɪᴀ ᴅɪ ᴛᴏᴏʟꜱ** ✘

»  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}lang`
»  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴜɴᴛᴜᴋ ᴍᴇɴɢᴜʙᴀʜ ʙᴀʜᴀꜱᴀ.

»  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}string`
»  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ꜱᴛʀɪɴɢ ꜱᴇꜱꜱɪᴏɴ.
""")
        logoyins = random.choice(
            [
                "assets/inline1.png",
                "assets/inline2.png",
                "assets/inline3.png"
            ]
        )
        await event.edit(
            text,
            file=logoyins,
            link_preview=True,
            buttons=[Button.inline("ʙᴀᴄᴋ", data="gcback")])
    else:
        reply_pop_up_alert = f"❌ 𝗗𝗜𝗦𝗖𝗟𝗔𝗜𝗠𝗘𝗥 ❌\n\nᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴍᴇᴍᴘᴜɴʏᴀɪ ʜᴀᴋ ᴜɴᴛᴜᴋ ᴍᴇɴᴇᴋᴀɴ ᴛᴏᴍʙᴏʟ ʙᴜᴛᴛᴏɴ ɪɴɪ"
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

@ayiin.bot.on(events.CallbackQuery(data=b"close"))
async def close(event):
    buttons = [
        (custom.Button.inline("ᴍᴀɪɴ ᴍᴇɴᴜ", data="gcback"),),
    ]
    logoyins = random.choice(
        [
            "assets/inline1.png",
            "assets/inline2.png",
            "assets/inline3.png"
        ]
    )
    await event.edit("**ᴍᴇɴᴜ ᴅɪᴛᴜᴛᴜᴘ**", file=logoyins, buttons=buttons)

@ayiin.bot.on(
    events.callbackquery.CallbackQuery(
        data=re.compile(rb"helpme_prev\((.+?)\)")
    )
)
async def on_plug_in_callback_query_handler(event):
    sudoer = getSudo()

    if event.query.user_id == ayiin.me.id or event.query.user_id in sudoer:
        current_page_number = int(
            event.data_match.group(1).decode("UTF-8"))
        buttons = ayiin.paginateHelp(
            current_page_number - 1, cmdHelp, "helpme")
        await event.edit(buttons=buttons)
    else:
        reply_pop_up_alert = f"ᴋᴀᴍᴜ ᴛɪᴅᴀᴋ ᴅɪɪᴢɪɴᴋᴀɴ, ɪɴɪ ᴜꜱᴇʀʙᴏᴛ ᴍɪʟɪᴋ {ayiin.me.first_name}"
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

@ayiin.bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ub_modul_(.*)")))
async def on_plug_in_callback_query_handler(event):
    sudoer = getSudo()
    cmd = getHandler()
    if event.query.user_id == ayiin.me.id or event.query.user_id in sudoer:
        modul_name = event.data_match.group(1).decode("UTF-8")

        cmdhel = str(cmdHelp[modul_name])
        if len(cmdhel) > 950:
            help_string = (
                str(cmdHelp[modul_name])
                .replace("`", "")
                .replace("**", "")[:950]
                + "..."
                + f"\n\nʙᴀᴄᴀ ᴛᴇᴋꜱ ʙᴇʀɪᴋᴜᴛɴʏᴀ ᴋᴇᴛɪᴋ {cmd}help "
                + modul_name
                + " "
            )
        else:
            help_string = (str(cmdHelp[modul_name]).replace(
                "`", "").replace("**", ""))

        reply_pop_up_alert = (
            help_string
            if help_string is not None
            else "{} ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴅᴏᴋᴜᴍᴇɴ ʏᴀɴɢ ᴛᴇʟᴀʜ ᴅɪᴛᴜʟɪꜱ ᴜɴᴛᴜᴋ ᴍᴏᴅᴜʟ.".format(
                modul_name
            )
        )
        await event.edit(
            reply_pop_up_alert, buttons=[
                Button.inline("ʙᴀᴄᴋ", data="reopen")]
        )

    else:
        reply_pop_up_alert = f"ᴋᴀᴍᴜ ᴛɪᴅᴀᴋ ᴅɪɪᴢɪɴᴋᴀɴ, ɪɴɪ ᴜꜱᴇʀʙᴏᴛ ᴍɪʟɪᴋ {ayiin.me.first_name}"
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
