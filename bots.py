import requests
import time


class UpdateCheckBot:

    BOT_URL = 'https://api.telegram.org/bot'
    BOT_TOKEN = '8353328233:AAEN3S644SlHTuLydFk4HChro6_qL0thto0'
    CAT_API = 'https://api.thecatapi.com/v1/images/search'
    MAX_COUNTER = 100

    offset = -2
    counter = 0
    chat_id: int

    def main(self):
        while self.counter < self.MAX_COUNTER:

            print('attempt =', self.counter)

            updated = requests.get(f'{self.BOT_URL}{self.BOT_TOKEN}/getUpdates?offset={self.offset + 1}').json()
            if updated['result']:
                results = updated['result']
                
                for result in results:
                    message = result['message']
                    first_name = message['from']['first_name']
                    last_name = message['from']['last_name']
                    name = f'{last_name} {first_name}'
                    chat_id = message['chat']['id']

                    r = requests.get(self.CAT_API)
                    if r.status_code == 200:
                        cat_url = r.json()[0]['url']
                        requests.get(f'{self.BOT_URL}{self.BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_url}')

                    else:
                        requests.get(f'{self.BOT_URL}{self.BOT_TOKEN}/sendMessage?chat_id={chat_id}&text=Простите, {name}, но котиков нет :(')

            time.sleep(1)
            self.counter += 1

bot = UpdateCheckBot()
bot.main()

