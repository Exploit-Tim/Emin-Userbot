# ported from uniborg
# https://github.com/muhammedfurkan/UniBorg/blob/master/stdplugins/ezanvakti.py

import json

import requests

from pyAyiin import cmdHelp
from pyAyiin.decorator import ayiinCmd
from pyAyiin.utils import eor

from . import cmd


@ayiinCmd(pattern="adzan(?:\\s|$)([\\s\\S]*)")
async def get_adzan(adzan):
    "ꜱʜᴏᴡꜱ ʏᴏᴜ ᴛʜᴇ ɪꜱʟᴀᴍɪᴄ ᴘʀᴀʏᴇʀ ᴛɪᴍᴇꜱ ᴏꜰ ᴛʜᴇ ɢɪᴠᴇɴ ᴄɪᴛʏ ɴᴀᴍᴇ"
    input_str = adzan.pattern_match.group(1)
    LOKASI = "ᴊᴀᴋᴀʀᴛᴀ" if not input_str else input_str
    url = f"http://muslimsalat.com/{LOKASI}.json?key=bd099c5825cbedb9aa934e255a81a5fc"
    request = requests.get(url)
    if request.status_code != 200:
        return await eor(
            adzan,
            f"**ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇɴᴇᴍᴜᴋᴀɴ ᴋᴏᴛᴀ** `{LOKASI}`",
            time=120
        )
    result = json.loads(request.text)
    catresult = f"<b>ᴊᴀᴅᴡᴀʟ ꜱʜᴀʟᴀᴛ ʜᴀʀɪ ɪɴɪ:</b>\
            \n<b>📆 ᴛᴀɴɢɢᴀʟ </b><code>{result['items'][0]['date_for']}</code>\
            \n<b>📍 ᴋᴏᴛᴀ</b> <code>{result['query']}</code> | <code>{result['country']}</code>\
            \n\n<b>ᴛᴇʀʙɪᴛ  : </b><code>{result['items'][0]['shurooq']}</code>\
            \n<b>ꜱᴜʙᴜʜ : </b><code>{result['items'][0]['fajr']}</code>\
            \n<b>ᴢᴜʜᴜʀ  : </b><code>{result['items'][0]['dhuhr']}</code>\
            \n<b>ᴀꜱʜᴀʀ  : </b><code>{result['items'][0]['asr']}</code>\
            \n<b>ᴍᴀɢʜʀɪʙ : </b><code>{result['items'][0]['maghrib']}</code>\
            \n<b>ɪꜱʏᴀ : </b><code>{result['items'][0]['isha']}</code>\
    "
    await eor(adzan, catresult)


cmdHelp.update(
    {
        "ᴀᴅᴢᴀɴ": f"**ᴘʟᴜɢɪɴ : **`ᴀᴅᴢᴀɴ`\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}adzan` <ɴᴀᴍᴀ ᴋᴏᴛᴀ>\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴍᴇɴᴜɴᴊᴜᴋᴋᴀɴ ᴡᴀᴋᴛᴜ ᴊᴀᴅᴡᴀʟ ꜱʜᴏʟᴀᴛ ᴅᴀʀɪ ᴋᴏᴛᴀ ʏᴀɴɢ ᴅɪʙᴇʀɪᴋᴀɴ.\
    "
    }
)
