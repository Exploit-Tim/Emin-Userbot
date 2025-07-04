# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" ᴜꜱᴇʀʙᴏᴛ ᴍᴏᴅᴜʟᴇ ᴄᴏɴᴛᴀɪɴɪɴɢ ᴄᴏᴍᴍᴀɴᴅꜱ ʀᴇʟᴀᴛᴇᴅ ᴛᴏ ᴀɴᴅʀᴏɪᴅ"""

import asyncio
import math
import os
import re
import time

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from requests import get

from pyAyiin import ayiin, cmdHelp
from pyAyiin.decorator import ayiinCmd
from pyAyiin.lib.tools import (
    human_to_bytes,
    humanbytes,
    md5,
    time_formatter,
)

from . import cmd

GITHUB = "https://github.com"
DEVICES_DATA = (
    "https://raw.githubusercontent.com/androidtrackers/"
    "certified-android-devices/master/by_device.json"
)


@ayiinCmd(pattern="magisk$")
async def magisk(request):
    """ᴍᴀɢɪꜱᴋ ʟᴀᴛᴇꜱᴛ ʀᴇʟᴇᴀꜱᴇꜱ"""
    magisk_dict = {
        "Stable": "https://raw.githubusercontent.com/topjohnwu/magisk-files/master/stable.json",
        "Beta": "https://raw.githubusercontent.com/topjohnwu/magisk-files/master/beta.json",
        "Canary": "https://raw.githubusercontent.com/topjohnwu/magisk-files/master/canary.json",
    }
    releases = "**ʟᴀᴛᴇꜱᴛ ᴍᴀɢɪꜱᴋ ʀᴇʟᴇᴀꜱᴇꜱ :**\n"
    async with ClientSession() as ses:
        for name, release_url in magisk_dict.items():
            async with ses.get(release_url) as resp:
                data = await resp.json(content_type="text/plain")
                version = data["magisk"]["version"]
                version_code = data["magisk"]["versionCode"]
                note = data["magisk"]["note"]
                url = data["magisk"]["link"]
                releases += (
                    f"**{name}** - __v{version} ({version_code})__ : "
                    f"[APK]({url}) | [Note]({note})\n"
                )
    await request.edit(releases)


@ayiinCmd(pattern=r"device(?: |$)(\S*)")
async def device_info(request):
    """ɢᴇᴛ ᴀɴᴅʀᴏɪᴅ ᴅᴇᴠɪᴄᴇ ʙᴀꜱɪᴄ ɪɴꜰᴏ ꜰʀᴏᴍ ɪᴛꜱ ᴄᴏᴅᴇɴᴀᴍᴇ"""
    textx = await request.get_reply_message()
    device = request.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text
    else:
        return await request.edit(f"`ᴜꜱᴀɢᴇ: {cmd}device <ᴄᴏᴅᴇɴᴀᴍᴇ> / <ᴍᴏᴅᴇʟ>`")
    try:
        found = get(DEVICES_DATA).json()[device]
    except KeyError:
        reply = f"`ᴄᴏᴜʟᴅɴ'ᴛ ꜰɪɴᴅ ɪɴꜰᴏ ᴀʙᴏᴜᴛ {device}!`\n"
    else:
        reply = f"ꜱᴇᴀʀᴄʜ ʀᴇꜱᴜʟᴛꜱ ꜰᴏʀ {device}:\n\n"
        for item in found:
            brand = item["brand"]
            name = item["name"]
            codename = device
            model = item["model"]
            reply += (
                f"{brand} {name}\n"
                f"**ᴄᴏᴅᴇɴᴀᴍᴇ**: `{codename}`\n"
                f"**ᴍᴏᴅᴇʟ**: {model}\n\n"
            )
    await request.edit(reply)


@ayiinCmd(pattern=r"codename(?: |)([\S]*)(?: |)([\s\S]*)")
async def codename_info(request):
    """ꜱᴇᴀʀᴄʜ ꜰᴏʀ ᴀɴᴅʀᴏɪᴅ ᴄᴏᴅᴇɴᴀᴍᴇ"""
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()
    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        return await request.edit("`ᴜꜱᴀɢᴇ: .codename <ʙʀᴀɴᴅ> <ᴅᴇᴠɪᴄᴇ>`")
    found = [
        i
        for i in get(DEVICES_DATA).json()
        if i["brand"].lower() == brand and device in i["name"].lower()
    ]
    if len(found) > 8:
        found = found[:8]
    if found:
        reply = f"ꜱᴇᴀʀᴄʜ ʀᴇꜱᴜʟᴛꜱ ꜰᴏʀ {brand.capitalize()} {device.capitalize()}:\n\n"
        for item in found:
            brand = item["brand"]
            name = item["name"]
            codename = item["device"]
            model = item["model"]
            reply += (
                f"{brand} {name}\n"
                f"**ᴄᴏᴅᴇɴᴀᴍᴇ**: `{codename}`\n"
                f"**ᴍᴏᴅᴇʟ**: {model}\n\n"
            )
    else:
        reply = f"`ᴄᴏᴜʟᴅɴ'ᴛ ꜰɪɴᴅ {device} ᴄᴏᴅᴇɴᴀᴍᴇ!`\n"
    await request.edit(reply)


@ayiinCmd(pattern="pixeldl(?: |$)(.*)")
async def download_api(dl):
    await dl.edit("`ᴄᴏʟʟᴇᴄᴛɪɴɢ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ꜰɪɴᴅ...`")
    URL = dl.pattern_match.group(1)
    URL_MSG = await dl.get_reply_message()
    if URL:
        pass
    elif URL_MSG:
        URL = URL_MSG.text
    else:
        await dl.edit("`ᴇᴍᴘᴛʏ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ...`")
        return
    if not re.findall(r"\bhttps?://download.*pixelexperience.*\.org\S+", URL):
        await dl.edit("`ɪɴᴠᴀʟɪᴅ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ...`")
        return
    driver = await ayiin.chrome()
    await dl.edit("`ɢᴇᴛᴛɪɴɢ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ...`")
    driver.get(URL)
    error = driver.find_elements_by_class_name("swal2-content")
    if len(error) > 0 and error[0].text == "ꜰɪʟᴇ ɴᴏᴛ ꜰᴏᴜɴᴅ.":
        await dl.edit(f"`ꜰɪʟᴇɴᴏᴛꜰᴏᴜɴᴅᴇʀʀᴏʀ`: {URL} ɪꜱ ɴᴏᴛ ꜰᴏᴜɴᴅ.")
        return
    datas = driver.find_elements_by_class_name("download__meta")
    """ - ᴇɴᴜᴍᴇʀᴀᴛᴇ ᴅᴀᴛᴀ ᴛᴏ ᴍᴀᴋᴇ ꜱᴜʀᴇ ᴡᴇ ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴇ ᴍᴀᴛᴄʜᴇᴅ ᴠᴇʀꜱɪᴏɴ - """
    md5_origin = None
    i = None
    for index, value in enumerate(datas):
        for data in value.text.split("\n"):
            if data.startswith("MD5"):
                md5_origin = data.split(":")[1].strip()
                i = index
                break
        if md5_origin is not None and i is not None:
            break
    if md5_origin is None and i is None:
        await dl.edit("`ᴛʜᴇʀᴇ ɪꜱ ɴᴏ ᴍᴀᴛᴄʜ ᴠᴇʀꜱɪᴏɴ ᴀᴠᴀɪʟᴀʙʟᴇ...`")
    file_name = URL.split("/")[-2] if URL.endswith("/") else URL.split("/")[-1]
    file_path = ayiin.TEMP_DOWNLOAD_DIRECTORY + file_name
    download = driver.find_elements_by_class_name("download__btn")[i]
    download.click()
    await dl.edit("`ꜱᴛᴀʀᴛɪɴɢ ᴅᴏᴡɴʟᴏᴀᴅ...`")
    file_size = human_to_bytes(download.text.split(None, 2)[-1].strip("()"))
    display_message = None
    complete = False
    start = time.time()
    while not complete:
        if os.path.isfile(file_path + ".crdownload"):
            try:
                downloaded = os.stat(file_path + ".crdownload").st_size
                status = "ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ"
            except OSError:  # Rare case
                await asyncio.sleep(1)
                continue
        elif os.path.isfile(file_path):
            downloaded = os.stat(file_path).st_size
            file_size = downloaded
            status = "ᴄʜᴇᴄᴋɪɴɢ"
        else:
            await asyncio.sleep(0.3)
            continue
        diff = time.time() - start
        percentage = downloaded / file_size * 100
        speed = round(downloaded / diff, 2)
        eta = round((file_size - downloaded) / speed)
        prog_str = "`{0}` | [{1}{2}] `{3}%`".format(
            status,
            "".join("●" for i in range(math.floor(percentage / 10))),
            "".join("○" for i in range(10 - math.floor(percentage / 10))),
            round(percentage, 2),
        )

        current_message = (
            "`[ᴅᴏᴡɴʟᴏᴀᴅ]`\n\n"
            f"`{file_name}`\n"
            f"`ꜱᴛᴀᴛᴜꜱ`\n{prog_str}\n"
            f"`{humanbytes(downloaded)} of {humanbytes(file_size)}"
            f" @ {humanbytes(speed)}`\n"
            f"`ᴇᴛᴀ` -> {time_formatter(eta)}"
        )
        if (
            round(diff % 15.00) == 0
            and display_message != current_message
            or (downloaded == file_size)
        ):
            await dl.edit(current_message)
            display_message = current_message
        if downloaded == file_size:
            if not os.path.isfile(file_path):  # Rare case
                await asyncio.sleep(1)
                continue
            MD5 = await md5(file_path)
            if md5_origin == MD5:
                complete = True
            else:
                await dl.edit("`ᴅᴏᴡɴʟᴏᴀᴅ ᴄᴏʀʀᴜᴘᴛ...`")
                os.remove(file_path)
                driver.quit()
                return
    await dl.respond(f"`{file_name}`\n\n" f"ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ᴛᴏ `{file_path}`.")
    await dl.delete()
    driver.quit()
    return


@ayiinCmd(pattern=r"specs(?: |)([\S]*)(?: |)([\s\S]*)")
async def devices_specifications(request):
    """ᴍᴏʙɪʟᴇ ᴅᴇᴠɪᴄᴇꜱ ꜱᴘᴇᴄɪꜰɪᴄᴀᴛɪᴏɴꜱ"""
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()
    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        return await request.edit("`ᴜꜱᴀɢᴇ: .specs <ʙʀᴀɴᴅ> <ᴅᴇᴠɪᴄᴇ>`")
    all_brands = (
        BeautifulSoup(
            get("https://www.devicespecifications.com/en/brand-more").content,
            "lxml") .find(
            "div",
            {
                "class": "brand-listing-container-news"}) .findAll("a"))
    brand_page_url = None
    try:
        brand_page_url = [
            i["href"] for i in all_brands if brand == i.text.strip().lower()
        ][0]
    except IndexError:
        await request.edit(f"`{brand} ɪꜱ ᴜɴᴋɴᴏᴡɴ ʙʀᴀɴᴅ!`")
    devices = BeautifulSoup(get(brand_page_url).content, "lxml").findAll(
        "div", {"class": "model-listing-container-80"}
    )
    device_page_url = None
    try:
        device_page_url = [
            i.a["href"]
            for i in BeautifulSoup(str(devices), "lxml").findAll("h3")
            if device in i.text.strip().lower()
        ]
    except IndexError:
        await request.edit(f"`ᴄᴀɴ'ᴛ ꜰɪɴᴅ {device}!`")
    if len(device_page_url) > 2:
        device_page_url = device_page_url[:2]
    reply = ""
    for url in device_page_url:
        info = BeautifulSoup(get(url).content, "lxml")
        reply = "\n**" + info.title.text.split("-")[0].strip() + "**\n\n"
        info = info.find("div", {"id": "model-brief-specifications"})
        specifications = re.findall(r"<b>.*?<br/>", str(info))
        for item in specifications:
            title = re.findall(r"<b>(.*?)</b>", item)[0].strip()
            data = (
                re.findall(r"</b>: (.*?)<br/>", item)[0]
                .replace("<b>", "")
                .replace("</b>", "")
                .strip()
            )
            reply += f"**{title}**: {data}\n"
    await request.edit(reply)


@ayiinCmd(pattern=r"twrp(?: |$)(\S*)")
async def twrp(request):
    """ɢᴇᴛ ᴀɴᴅʀᴏɪᴅ ᴅᴇᴠɪᴄᴇ ᴛᴡʀᴘ"""
    textx = await request.get_reply_message()
    device = request.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text.split(" ")[0]
    else:
        return await request.edit("`ᴜꜱᴀɢᴇ: .twrp <ᴄᴏᴅᴇɴᴀᴍᴇ>`")
    url = get(f"https://dl.twrp.me/{device}/")
    if url.status_code == 404:
        reply = f"`ᴄᴏᴜʟᴅɴ'ᴛ ꜰɪɴᴅ ᴛᴡʀᴘ ᴅᴏᴡɴʟᴏᴀᴅꜱ ꜰᴏʀ {device}!`\n"
        return await request.edit(reply)
    page = BeautifulSoup(url.content, "lxml")
    download = page.find("table").find("tr").find("a")
    dl_link = f"https://dl.twrp.me{download['href']}"
    dl_file = download.text
    size = page.find("span", {"class": "filesize"}).text
    date = page.find("em").text.strip()
    reply = (
        f"**ʟᴀᴛᴇꜱᴛ ᴛᴡʀᴘ ꜰᴏʀ {device}:**\n"
        f"[{dl_file}]({dl_link}) - __{size}__\n"
        f"**ᴜᴘᴅᴀᴛᴇᴅ:** __{date}__\n"
    )
    await request.edit(reply)


cmdHelp.update(
    {
        "ᴀɴᴅʀᴏɪᴅ": f"**ᴘʟᴜɢɪɴ : **`ᴀɴᴅʀᴏɪᴅ`\
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}magisk`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴅᴀᴘᴀᴛᴋᴀɴ ʀɪʟɪꜱ ᴍᴀɢɪꜱᴋ ᴛᴇʀʙᴀʀᴜ \
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}device <ᴄᴏᴅᴇɴᴀᴍᴇ>`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴅᴀᴘᴀᴛᴋᴀɴ ɪɴꜰᴏ ᴛᴇɴᴛᴀɴɢ ɴᴀᴍᴀ ᴋᴏᴅᴇ ᴀᴛᴀᴜ ᴍᴏᴅᴇʟ ᴘᴇʀᴀɴɢᴋᴀᴛ ᴀɴᴅʀᴏɪᴅ. \
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}codename <ʙʀᴀɴᴅ> <ᴅᴇᴠɪᴄᴇ>`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴄᴀʀɪ ɴᴀᴍᴀ ᴋᴏᴅᴇ ᴘᴇʀᴀɴɢᴋᴀᴛ ᴀɴᴅʀᴏɪᴅ. \
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}pixeldl` **<download.pixelexperience.org>**\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴜɴᴅᴜʜ ʀᴏᴍ ᴘᴇɴɢᴀʟᴀᴍᴀɴ ᴘɪᴋꜱᴇʟ ᴋᴇ ꜱᴇʀᴠᴇʀ ʙᴏᴛ ᴘᴇɴɢɢᴜɴᴀ ᴀɴᴅᴀ. \
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}specs <ʙʀᴀɴᴅ> <ᴅᴇᴠɪᴄᴇ>`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴅᴀᴘᴀᴛᴋᴀɴ ɪɴꜰᴏ ꜱᴘᴇꜱɪꜰɪᴋᴀꜱɪ ᴘᴇʀᴀɴɢᴋᴀᴛ. \
        \n\n  »  **ᴘᴇʀɪɴᴛᴀʜ :** `{cmd}twrp <ᴄᴏᴅᴇɴᴀᴍᴇ>`\
        \n  »  **ᴋᴇɢᴜɴᴀᴀɴ : **ᴅᴀᴘᴀᴛᴋᴀɴ ᴜɴᴅᴜʜᴀɴ ᴛᴡʀᴘ ᴛᴇʀʙᴀʀᴜ ᴜɴᴛᴜᴋ ᴘᴇʀᴀɴɢᴋᴀᴛ ᴀɴᴅʀᴏɪᴅ. \
    "
    }
)
