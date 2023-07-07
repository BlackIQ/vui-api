# import telegram

# import asyncio

import requests as req

bot_token = '6058827294:AAEUcx1fc8quG4py_AVOMLbYYXDLiFmID_s'

# bot = telegram.Bot(token=bot_token)


# async def final_send(message, chatid):
#     await bot.send_message(chat_id=chatid, text=message)


# async def main(message, chatid):
#     await final_send(message, chatid)


# def send(message, chatid):
#     asyncio.run(main(message, chatid))

def send(message, chatid):
    data = {
        "chat_id": chatid,
        "text": message
    }

    req.post(
        f"https://api.telegram.org/bot/{bot_token}/sendMessage", data=data)
