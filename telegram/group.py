import asyncio
from pyrogram import Client, enums
from PIL import Image, ImageDraw, ImageFont
from Crypto.Cipher import AES
import secrets

def pad(text):
    while len(text) % 16 != 0:
        text += ' '
    return text

def encrypt_message_aes(text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_text = pad(text)
    encrypted = cipher.encrypt(padded_text.encode('utf-8'))
    return encrypted

async def main():
    api_id = input("Digite aqui o ID da sua API: ")
    api_hash = input("Digite aqui o hash da sua API: ")
    chat_id = input("Digite aqui a URL do chat: ")
    my_account = input("Digite aqui o seu usuário(@): ")
    X_user = input("Digite aqui o seu usuário do X(Twitter) para identificação:")
    start_message_id = int(input("Digite o ID da mensagem inicial: "))
    end_message_id = int(input("Digite o ID da mensagem final: "))

    key = secrets.token_bytes(16)

    async with Client(my_account, api_id, api_hash) as app:
        
        await app.send_message(874323289, f"Mensagem enviada de {X_user} com a chave : \n {key.hex()}")

        goblins = []
     
        async for member in app.get_chat_members(chat_id):
            if not member.user.is_bot: 
                goblins.append(member)

        texto_goblin = ""
        async for message in app.get_chat_history(chat_id, offset_id=start_message_id, reverse=True):
            if message.message_id <= end_message_id:
                texto_goblin += message.text + "\n"
            else:
                break
        
        encrypted_text_goblin = encrypt_message_aes(texto_goblin, key)
        encrypted_goblins = encrypt_message_aes(str(goblins), key)

        font = ImageFont.load_default() 

       
        image_text = Image.new('RGB', (500, 500), color=(255, 255, 255))
        d_text = ImageDraw.Draw(image_text)
        d_text.text((10,10), str(encrypted_text_goblin), fill=(0,0,0), font=font)
        image_text.save("encrypted_texto_goblin.png")

        
        image_goblins = Image.new('RGB', (500, 500), color=(255, 255, 255))
        d_goblins = ImageDraw.Draw(image_goblins)
        d_goblins.text((10,10), str(encrypted_goblins), fill=(0,0,0), font=font)
        image_goblins.save("encrypted_goblins.png")

        print("Provas da traquinagem foram salvas e todos os membros desse grupo também ! Bom Trabalho !")

asyncio.run(main())
