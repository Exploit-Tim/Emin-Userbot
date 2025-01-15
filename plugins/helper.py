""" Userbot module for other small commands. """

from pyAyiin import cmdHelp
from pyAyiin.decorator import ayiinCmd
from pyAyiin.utils import eor
from pyAyiin.database.variable import cekVar

from . import cmd


@ayiinCmd(pattern="ihelp$")
async def usit(event):
    me = await event.client.get_me()
    await eor(
        event,
        f"""
**ʜᴀʟᴏ {me.first_name} ᴊɪᴋᴀ ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴛᴀᴜ ᴜɴᴛᴜᴋ ᴍᴇᴍᴇʀɪɴᴛᴀʜ ꜱᴀʏᴀ ᴋᴇᴛɪᴋ** `{cmd}help` ᴀᴛᴀᴜ ʙɪꜱᴀ ᴍɪɴᴛᴀ ʙᴀɴᴛᴜᴀɴ ᴋᴇ:
⍟ **Group Support :** [𝙴𝙼𝙸𝙽 𝚂𝚄𝙿𝙿𝙾𝚁𝚃](t.me/EminChats)
⍟ **Channel Emin :** [𝙴𝙼𝙸𝙽 𝚂𝚄𝙿𝙿𝙾𝚁𝚃](t.me/EminSupport)
⍟ **Owner Repo :** [𝙴𝙼𝙸𝙽](t.me/AyiinXd)
⍟ **Repo :** [𝙴𝙼𝙸𝙽-𝚄𝚂𝙴𝚁𝙱𝙾𝚃](https://github.com/iniemin/Emin-Userbot)
"""
    )


@ayiinCmd(pattern="listvar$")
async def var(event):
    text = "**ʜᴀꜱɪʟ ᴅᴀᴛᴀʙᴀꜱᴇ ᴠᴀʀꜱ ᴅɪᴛᴇᴍᴜᴋᴀɴ.**\n\n**ɴᴏ | ᴠᴀʀɪᴀʙʟᴇ | ᴠᴀʟᴜᴇ**"
    no = 0
    listvar = cekVar()
    if listvar:
        for xd in listvar:
            no += 1
            text += f"\n{no}. {xd[0]} - {xd[1]}"
    else:
        text = "**ᴀɴᴅᴀ ʙᴇʟᴜᴍ ᴍᴇᴍɪʟɪᴋɪ ᴅᴀᴛᴀʙᴀꜱᴇ ᴠᴀʀꜱ.**"
    await eor(
        event,
        text
    )


cmdHelp.update(
    {
        "ʜᴇʟᴘᴇʀ": f"**ᴘʟᴜɢɪɴ : **`ʜᴇʟᴘᴇʀ`\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}ihelp`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴇᴍɪɴ-ᴜꜱᴇʀʙᴏᴛ.\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}listvar`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴍᴇʟɪʜᴀᴛ ᴅᴀꜰᴛᴀʀ ᴠᴀʀꜱ.\
    "
    }
)
