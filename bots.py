import requests
import time
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from aiogram import F
import random

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

# bot = UpdateCheckBot()
# bot.main()

class EchoBot:

    BOT_TOKEN = '8353328233:AAEN3S644SlHTuLydFk4HChro6_qL0thto0'

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    @staticmethod
    async def process_start_command(message: Message):
        await message.answer("Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь")

    @staticmethod
    async def process_help_command(message: Message):
        await message.answer(
            'Напиши мне что-нибудь и в ответ '
            'я пришлю тебе твое сообщение'
        )

    @staticmethod
    async def send_photo_echo(message: Message):
        await message.reply_photo(photo=message.photo[0].file_id)

    @staticmethod
    async def send_sticker_echo(message: Message):
        await message.reply_sticker(sticker=message.sticker.file_id)

    @staticmethod
    async def send_audio_echo(message: Message):
        await message.reply_audio(audio=message.audio.file_id)

    @staticmethod
    async def send_document_echo(message: Message):
        await message.reply_document(document=message.document.file_id)

    @staticmethod
    async def send_echo(message: Message):
        try:
            await message.send_copy(chat_id=message.chat.id)
        except TypeError:
            await message.reply("text='Данный тип апдейтов не поддерживается методом send_copy")


    dp.message.register(process_start_command, Command(commands="start"))
    dp.message.register(process_help_command, Command(commands="help"))
    # dp.message.register(send_photo_echo, F.photo)
    # dp.message.register(send_sticker_echo, F.sticker)
    # dp.message.register(send_audio_echo, F.audio)
    # dp.message.register(send_document_echo, F.document)
    dp.message.register(send_echo)


BOT_TOKEN = '8353328233:AAEN3S644SlHTuLydFk4HChro6_qL0thto0'

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

user = {
    'in_game': False,
    'attempt': 0,
    'number': random.randint(1, 10),
    'total_games': 0,
    'wins': 0,
}

def check_casino_succes():
    if user['total_games'] == 0:
        return None
    if user['wins']/user['total_games'] > 0.5:
        return 'С вами удача, быстрее в казино играть!'
    else:
        return 'Вам в казино противопоказано ха!'

@staticmethod
async def process_start_command(message: Message):
    await message.answer(
        "Привет!\nМеня зовут Рандом-бот!\nДавай сыграем в игру 'Угадай число'. Ты можешь узнать все команды, набрав /help"
                         )

@staticmethod
@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer('Список команд: \n1)/help Поможем, чем сможем \n2)/play играаа\n3)/cancel прекратить игру\n4)/stat ваша статистика')

@staticmethod
@dp.message(Command(commands='stat'))
async def process_help_command(message: Message):
    await message.answer(f'Твое кол-во попыток испытать удач: {user["total_games"]}\nКол-во удачных игр: {user['wins']}\n'
                         f'{check_casino_succes()}'
    )

@staticmethod
@dp.message(Command(commands='play'))
async def process_help_command(message: Message):
    await message.answer('О, крутяк, давай начнем играть. Отправляй мне числа от 1 до 10')


@staticmethod
@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра',
                            'играть', 'хочу играть']))
async def procces_user_agree(message: Message):
    if user['in_game']:
        await message.answer('Давай числа говори уже, а не дакай тут')
    else:
        user['in_game'] = True
        user['attempt'] += 1
        user['total_games'] += 1
        await message.answer('Крутяк, я загадал число. Давай гадай теперь')

@staticmethod
@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def procces_user_not_agree(message: Message):
    if not user['in_game']:
        await message.answer('Такой ответ не принимаю, пиши ответ ДА')
    else:
        await message.answer('Поздновато, мы уже играем. Но если тебе так лень, то можешь написать /cancel')

@staticmethod
@dp.message(lambda x: x.text and x.text.isdigit() and 0 <= int(x.text) <= 100)
async def procces_user_not_agree(message: Message):
    number = int(message.text)
    user_succes_number = user['number']

    if user['attempt'] > 2 and user_succes_number != number:
        await message.answer(f'Сорян, ваше число попыток исчерпано. Секретное число: {user['number']}\n Предлагаю заново испытать удачу. Будем играть?')
        new_succes_number = random.randint(1, 10)
        user['in_game'] = False
        user['attempt'] = 0
        user['number'] = new_succes_number

    else:
        if number == user_succes_number:
            new_succes_number = random.randint(1, 10)
            user['in_game'] = False
            user['attempt'] = 0
            user['number'] = new_succes_number
            user['wins'] += 1
            await message.answer(
                'Иди в казино играй, а не со мной. \nЧисло угадано, круто.. \n'
                'А давай еще раз сыграем, а?'
                )
        elif number < user_succes_number:
            user['attempt'] += 1
            await message.answer(
                f'Хаха, не угадали, давай-ка снова пиши число. Оно больше, чем {number} \n'
                )
        else:
            user['attempt'] += 1
            await message.answer(
                f'Хаха, не угадали, давай-ка снова пиши число. Оно меньше, чем {number} \n'
                )

@dp.message()
async def process_other_answers(message: Message):
    if user['in_game']:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?'
        ) 

     

if __name__ == "__main__":
    dp.run_polling(bot)
    