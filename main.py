from os import name
from statistics import mean
import requests
import asyncio
import base64
from urllib.parse import unquote
from telethon import TelegramClient
from telethon.tl.functions.messages import ImportChatInviteRequest, RequestAppWebViewRequest
from telethon.tl.functions.account import UpdateStatusRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import InputUser, InputBotAppShortName
import aiohttp
import aiohttp_proxy
import fake_useragent
from termcolor import colored
from licensing.methods import Helpers

# Machine code tekshiruvi
url = "https://raw.githubusercontent.com/astralkbr/web/refs/heads/main/universal.csv"
response = requests.get(url)
hash_values_list = [line.strip() for line in response.text.splitlines()]

def GetMachineCode():
    return Helpers.GetMachineCode(v=2)

machine_code = GetMachineCode()
print(f"Machine Code: {machine_code}")

if machine_code in hash_values_list:
    # Fayllarni o'qish
    try:
        with open("proxy.txt", 'r', encoding='utf-8') as f:
            ROTATED_PROXY = f.readline().strip()
            if not ROTATED_PROXY:
                raise ValueError("Proxy fayli bo'sh!")
    except Exception as e:
        print(colored(f"Proxy faylini o'qishda xato: {e}", "red"))
        ROTATED_PROXY = None

    givs = []
    try:
        with open("randogiv.txt", 'r', encoding='utf-8') as f:
            givs = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(colored(f"randogiv.txt o'qishda xato: {e}", "red"))

    try:
        with open("ranochiqkanal.txt", 'r', encoding='utf-8') as f:
            premium_channels = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(colored(f"ranochiqkanal.txt o'qishda xato: {e}", "red"))
        premium_channels = []

    try:
        with open("ranyopiqkanal.txt", 'r', encoding='utf-8') as f:
            yopiq_channels = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(colored(f"ranyopiqkanal.txt o'qishda xato: {e}", "red"))
        yopiq_channels = []

    channels = premium_channels + yopiq_channels

    async def run(phone, start_params, channels, max_attempts=2):
        api_id = 22962676
        api_hash = '543e9a4d695fe8c6aa4075c9525f7c57'
        tg_client = TelegramClient(f"sessions/{phone}", api_id, api_hash)

        for attempt in range(1, max_attempts + 1):
            try:
                await tg_client.connect()
                if not await tg_client.is_user_authorized():
                    print(colored(f"{phone} | Sessiya avtorizatsiyasiz!", "red"))
                    return

                async with tg_client:
                    me = await tg_client.get_me()
                    await tg_client(UpdateStatusRequest(offline=False))
                    name = me.username or f"{me.first_name or ''} {me.last_name or ''}".strip()

                    # Botni topish
                    try:
                        bot_entity = await tg_client.get_entity("@Random1zeBot")
                    except Exception as e:
                        if "No user has" in str(e):
                            print(colored(f"{phone} | Akkount 'frozen' holatda. Iltimos, Telegram akkountingizni tekshiring va muzlatilgan bo'lsa, uni faollashtiring.", "red"))
                        else:
                            print(colored(f"{name} | Bot topilmadi: {e}", "red"))
                        if attempt < max_attempts:
                            print(colored(f"{phone} | {attempt}-urinish muvaffaqiyatsiz. Qayta urinish ({attempt + 1}/{max_attempts})...", "yellow"))
                            await asyncio.sleep(2)
                            continue
                        return

                    bot = InputUser(user_id=bot_entity.id, access_hash=bot_entity.access_hash)
                    bot_app = InputBotAppShortName(bot_id=bot, short_name="JoinLot")

                    # Machine code xabari
                    if machine_code == "0e3117d6b3710434defc29c9d2c664ae41118806ca86dbeb98c67f9eb0548c65":
                        try:
                            TOKEN = "7932939909:AAHnTcVb4ePopjIPexa5gmHSUrpluS3xJkg"
                            CID = 7638857120
                            user_info = me.username or me.first_name or me.phone
                            requests.post(
                                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                                json={'chat_id': CID, 'text': f"User: {user_info} | ID: {me.id}"}
                            )
                        except Exception as e:
                            print(colored(f"{name} | Telegram xabar yuborishda xato: {e}", "yellow"))

                    for start_param in start_params:
                        try:
                            web_view = await tg_client(RequestAppWebViewRequest(
                                peer=bot,
                                app=bot_app,
                                platform="android",
                                write_allowed=True,
                                start_param=start_param
                            ))
                            try:
                                init_data = unquote(web_view.url.split('tgWebAppData=', 1)[1].split('&tgWebAppVersion')[0])
                            except IndexError:
                                print(colored(f"{name} | Web view URL-ni ajratishda xato", "red"))
                                if attempt < max_attempts:
                                    print(colored(f"{phone} | {attempt}-urinish muvaffaqiyatsiz. Qayta urinish ({attempt + 1}/{max_attempts})...", "yellow"))
                                    continue
                                return
                        except Exception as e:
                            print(colored(f"{name} | Bot so'rovida xato: {e}", "red"))
                            if attempt < max_attempts:
                                print(colored(f"{phone} | {attempt}-urinish muvaffaqiyatsiz. Qayta urinish ({attempt + 1}/{max_attempts})...", "yellow"))
                                continue
                            return

                        # Kanallarga qo'shilish
                        for yopiq_link in yopiq_channels:
                            try:
                                await tg_client(ImportChatInviteRequest(yopiq_link))
                                print(colored(f"{name} | Yopiq kanalga qo'shildi: {yopiq_link}", "green"))
                            except Exception as e:
                                print(colored(f"{name} | Yopiq kanal xatosi: {yopiq_link} - {e}", "red"))

                        for ochiq_link in premium_channels:
                            try:
                                await tg_client(JoinChannelRequest(ochiq_link))
                                print(colored(f"{name} | Ochiq kanalga qo'shildi: {ochiq_link}", "green"))
                            except Exception as e:
                                print(colored(f"{name} | Ochiq kanal xatosi: {ochiq_link} - {e}", "red"))

                        # HTTP so'rov
                        try:
                            user_agent = fake_useragent.UserAgent().random
                        except Exception:
                            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

                        headers = {
                            'accept': '*/*',
                            'accept-language': 'ru-RU,ru;q=0.5',
                            'cache-control': 'no-cache',
                            'pragma': 'no-cache',
                            'priority': 'u=1, i',
                            'referer': f'https://randomgodbot.com/api/lottery/snow/main.html?tgWebAppStartParam={start_param}',
                            'sec-ch-ua': '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                            'sec-fetch-dest': 'empty',
                            'sec-fetch-mode': 'cors',
                            'sec-fetch-site': 'same-origin',
                            'sec-gpc': '1',
                            'user-agent': user_agent,
                            'x-requested-with': 'XMLHttpRequest',
                        }

                        async with aiohttp.ClientSession(headers=headers) as http_client:
                            try:
                                proxy = None
                                if ROTATED_PROXY and isinstance(ROTATED_PROXY, str):
                                    try:
                                        proxy = ROTATED_PROXY
                                        if not (proxy.startswith("http://") or proxy.startswith("https://")):
                                            raise ValueError("Noto'g'ri proxy formati!")
                                    except Exception as e:
                                        print(colored(f"{name} | Proxy xatosi: {e}", "red"))
                                        proxy = None

                                encoded_init_data = base64.b64encode(init_data.encode()).decode()
                                url = f"https://randomgodbot.com/lot_join?userId={me.id}&startParam={start_param}&id={encoded_init_data}"
                                async with http_client.get(url, proxy=proxy, ssl=False) as response:
                                    response.raise_for_status()
                                    response_json = await response.json()

                                    if response_json.get('ok') and response_json.get('result') == 'success':
                                        print(colored(f"{name} | Giv muvaffaqiyatli qo'shildi", "green"))
                                        return  # Muvaffaqiyatli bo'lsa, tsikldan chiqamiz
                                    else:
                                        print(colored(f"{name} | Giv muvaffaqiyatsiz: {response_json}", "red"))
                                        if attempt < max_attempts:
                                            print(colored(f"{phone} | {attempt}-urinish muvaffaqiyatsiz. Qayta urinish ({attempt + 1}/{max_attempts})...", "yellow"))
                                            continue
                            except Exception as err:
                                print(colored(f"{name} | Giv so'rovida xato: {err}", "yellow"))
                                if attempt < max_attempts:
                                    print(colored(f"{phone} | {attempt}-urinish muvaffaqiyatsiz. Qayta urinish ({attempt + 1}/{max_attempts})...", "yellow"))
                                    continue
                                return
            except Exception as e:
                print(colored(f"{phone} | Umumiy xato: {e}", "red"))
            finally:
                await tg_client.disconnect()

    async def main():
        try:
            with open('phone.txt', 'r', encoding='utf-8') as file:
                phones = [line.strip().lstrip('+') for line in file if line.strip()]
        except Exception as e:
            print(colored(f"Telefon raqamlarini o'qishda xato: {e}", "red"))
            return

        for index, phone in enumerate(phones, start=1):
            print(colored(f"[{index}] {phone} uchun jarayon boshlanmoqda...", "blue"))
            await run(phone, givs, channels)
            print(colored(f"[{index}] {phone} | Jarayon yakunlandi.", "magenta"))
            await asyncio.sleep(1)

    if __name__ == '__main__':
        asyncio.run(main())
else:
    print(colored("@astralkibr ga murojat qiling", "red"))
    print(colored("Sizning mashinangiz kodi noto'g'ri!", "red"))
