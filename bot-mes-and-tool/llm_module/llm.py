from characterai import aiocai
import asyncio
import threading

class LLM:
    def __init__(self, admin_account, char_id):
        self.admin_account = admin_account
        self.char_id = char_id
        self.new_response = ""
        self.output = False
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.thread = threading.Thread(target=self.run_async_main)
        self.thread.start()

    def run_async_main(self):
        self.loop.run_until_complete(self.main())

    async def main(self):
        client = aiocai.Client(self.admin_account)
        me = await client.get_me()
        while True:
            try:
                    
                chat = await client.connect()
                async with chat:
                    new, _ = await chat.new_chat(self.char_id, me.id)
                    while True:
                        if self.new_response != "":
                            self.output = await chat.send_message(self.char_id, new.chat_id, self.new_response)
                            self.new_response = ""
                        await asyncio.sleep(0.1)
                
            except Exception as e:
                print(f"đã có lỗi: {e}")
                continue

    def predict(self, txt):
        self.new_response = txt
        while not self.output:
            continue
        output = self.output.text
        self.output = False
        return output