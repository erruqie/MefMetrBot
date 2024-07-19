import os
import random
import time
import asyncio
import logging
import sqlite3
import sys
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER, ADMINISTRATOR
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from mephmetrbot.utils import states

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.environ.get('BOT_TOKEN'))
dp = Dispatcher(storage=MemoryStorage())

router = Router()
router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))

conn = sqlite3.connect('mephmetrbot.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, drug_count INTEGER, last_use_time TEXT, is_admin INTEGER, is_banned INTEGER, last_casino TEXT, last_find TEXT, clan_member INTEGER, clan_invite INTEGER)')
cursor.execute('CREATE TABLE IF NOT EXISTS chats (chat_id INTEGER PRIMARY KEY, is_ads_enable INTEGER DEFAULT 1)')
cursor.execute('CREATE TABLE IF NOT EXISTS clans (clan_id INTEGER PRIMARY KEY, clan_name TEXT, clan_owner_id INTEGER, clan_balance INTEGER)')
conn.commit()


@dp.message(Command('start'))
async def start_command(message: Message):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='📢 Канал', url='https://t.me/mefmetrch'),
        InlineKeyboardButton(text='💰 Донат', url='https://t.me/mefmetrch'),
        InlineKeyboardButton(text='💬 Чат', url='https://t.me/mefmetrchat')
    )
    await message.reply("👋 *Здарова шныр*, этот бот сделан для того, чтобы *считать* сколько *грамм мефедрончика* ты снюхал\n🧑‍💻 Бот разработан *powerplantsmoke.t.me*", reply_markup=builder.as_markup(), parse_mode='markdown')


@dp.message(Command('grach'))
async def start_command(message: Message):
    await message.reply("грач хуесос")

@dp.message(Command('rules'))
async def start_command(message: Message):
    await message.reply('''Правила пользования mephmetrbot:
*1) Мультиаккаунтинг - бан навсегда и обнуление всех аккаунтов *
*2) Использование любых уязвимостей бота - бан до исправления и возможное обнуление*
*3) Запрещена реклама через топ кланов и топ юзеров - выговор, после бан с обнулением*
*4) Запрещена продажа валюты между игроками - обнуление и бан*

*Бот не имеет никакого отношения к реальности. Все совпадения случайны. 
Создатели не пропагандируют наркотики и против их распространения и употребления. 
Употребление, хранение и продажа является уголовно наказуемой*
*Сообщить о багах вы можете администраторам* (*команда* `/about`)''', parse_mode='markdown')

@dp.message(Command('admin'))
async def start_command(message: Message):
    await message.reply("🚨 *MONKEY ALARM*", parse_mode='markdown')

@dp.message(Command('getadmin'))
async def start_command(message: Message):
    await message.reply("🚨 *MONKEY ALARM*", parse_mode='markdown')

@dp.message(Command('free'))
async def start_command(message: Message):
    await message.reply("🚨 *MONKEY ALARM*", parse_mode='markdown')

@dp.message(Command('freeadmin'))
async def start_command(message: Message):
    await message.reply("🚨 *MONKEY ALARM*", parse_mode='markdown')

@dp.message(Command('reboot'))
async def start_command(message: Message):
    await message.reply("🚨 *MONKEY ALARM*", parse_mode='markdown')

@dp.message(Command('shop'))
async def start_command(message: Message):
    await message.reply("🚨 *MONKEY ALARM*", parse_mode='markdown')

@dp.message(Command('hack'))
async def start_command(message: Message):
    await message.reply("🚨 *MONKEY ALARM*", parse_mode='markdown')

@dp.message(Command('ban'))
async def start_command(message: Message):
    await message.reply("🚨 *MONKEY ALARM*", parse_mode='markdown')

# @dp.message(Command('casino'))
# async def start_command(message: Message):
#     await message.reply("❌ *Резерв казино закончился. Попробуйте, пожалуйста, позже!*", parse_mode='markdown')


@dp.message(Command('help'))
async def help_command(message: Message):
    await message.reply('''Все команды бота:

`/drug` - *принять мефик*
`/top` - *топ торчей мира*
`/take` - *спиздить мефик у ближнего*
`/give` - *поделиться мефиком*
`/casino` - *казино*
`/find` - *сходить за кладом*
`/about` - *узнать подробнее о боте*
`/clancreate` - *создать клан*
`/deposit` - *пополнить баланс клана*
`/withdraw` - *вывести средства с клана*
`/clantop` - *топ 10 кланов по состоянию баланса*
`/clanbalance` - *баланс клана*
`/claninfo` - *о клане*
`/claninvite` - *пригласить в клан*
`/clankick` - *кикнуть из клана*
`/clanaccept` - *принять приглашение в клан*
`/clandecline` - *отказаться от приглашения в клан*
`/clanleave` - *добровольно выйти из клана*
`/clandisband` - *распустить клан*
    ''', parse_mode='markdown')


@dp.message(Command('profile'))
async def profile_command(message: Message):
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif message.from_user:
        user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_banned = user[4] if user else 0
    if is_banned == 1:
            await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        if user:
            drug_count = user[1]
            is_admin = user[3]
            clan_member = user[7]
            if clan_member:
                cursor.execute('SELECT clan_name FROM clans WHERE clan_id = ?', (clan_member,))
                clan = cursor.fetchone()
                clan_name = clan[0] if clan else 0
            if user_id == message.from_user.id:
                username = message.from_user.username if message.from_user.username else None
                full_name = message.from_user.full_name
            else:
                username = message.reply_to_message.from_user.username if message.reply_to_message.from_user.username else None
                full_name = message.reply_to_message.from_user.full_name

            if is_admin == 1:
                if clan_member:
                    await message.reply(f"👑 *Администратор*\n👤 *Имя:* _{full_name}_\n👥 *Клан:* *{clan_name}*\n👥 *Username пользователя:* @{username}\n🆔 *ID пользователя:* `{user_id}`\n🌿 *Снюхано* _{drug_count}_ грамм.", parse_mode='markdown')
                else:
                    await message.reply(f"👑 *Администратор*\n👤 *Имя:* _{full_name}_\n👥 *Username пользователя:* @{username}\n🆔 *ID пользователя:* `{user_id}`\n🌿 *Снюхано* _{drug_count}_ грамм.", parse_mode='markdown')
            else:
                if clan_member:
                    await message.reply(f"👤 *Имя:* _{full_name}_\n👥 *Клан:* *{clan_name}*\n👥 *Username пользователя:* @{username}\n🆔 *ID пользователя:* `{user_id}`\n🌿 *Снюхано* _{drug_count}_ грамм.", parse_mode='markdown')
                else:
                    await message.reply(f"👤 *Имя:* _{full_name}_\n👥 *Username пользователя:* @{username}\n🆔 *ID пользователя: * `{user_id}`\n🌿 *Снюхано* _{drug_count}_ грамм.", parse_mode='markdown')
        else:
            await message.reply('❌ Профиль не найден')

@dp.message(Command('drug'))
async def drug_command(message: Message, state: FSMContext):
    format = '%Y-%m-%d %H:%M:%S.%f'
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    drug_count = user[1] if user else 0
    last_use_time = user[2] if user else 0
    is_admin = user[3] if user else 0
    is_banned = user[4] if user else 0
    use_time = datetime.strptime(last_use_time, format) if user else 0
    if is_banned == 1:
        await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        if last_use_time and (datetime.now() - use_time) < timedelta(hours=1):
            remaining_time = timedelta(hours=1) - (datetime.now() - use_time)
            await message.reply(f"❌ *{message.from_user.first_name}*, _ты уже нюхал(-а)!_\n\n🌿 Всего снюхано `{drug_count} грамм` мефедрона\n\n⏳ Следующий занюх доступен через `1 час.`", parse_mode='markdown')
        elif random.randint(0,100) < 20:
            if last_use_time and (datetime.now() - use_time) < timedelta(hours=1):
                remaining_time = timedelta(hours=1) - (datetime.now() - use_time)
                await message.reply(f"🧂 *{message.from_user.first_name}*, _ты просыпал(-а) весь мефчик!_\n\n🌿 Всего снюхано `{drug_count}` грамм мефедрона\n\n⏳ Следующий занюх доступен через `1 час.`", parse_mode='markdown')
                cursor.execute('UPDATE users SET last_use_time = ? WHERE id = ?', (datetime.now(), user_id))
                conn.commit()
        else:
            count = random.randint(1, 10)
            if user:
                cursor.execute('UPDATE users SET drug_count = drug_count + ? WHERE id = ?', (count, user_id))
            else:
                cursor.execute('INSERT INTO users (id, drug_count, is_admin, is_banned) VALUES (?, ?, 0, 0)', (user_id, count))
            cursor.execute('UPDATE users SET last_use_time = ? WHERE id = ?', (datetime.now(), user_id))
            conn.commit()
            await message.reply(f"👍 *{message.from_user.first_name}*, _ты занюхнул(-а) {count} грамм мефчика!_\n\n🌿 Всего снюхано `{drug_count+count}` грамм мефедрона\n\n⏳ Следующий занюх доступен через `1 час.`", parse_mode='markdown')
  
@dp.message(Command('top'))
async def top_command(message: Message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_banned = user[4] if user else 0
    if is_banned == 1:
        await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        cursor.execute('SELECT id, drug_count FROM users ORDER BY drug_count DESC LIMIT 10')
        top_users = cursor.fetchall()
        if top_users:
            response = "🔝ТОП 10 ЛЮТЫХ МЕФЕДРОНЩИКОВ В МИРЕ🔝:\n"
            counter = 1
            for user in top_users:
                user_id = user[0]
                if user_id == 7266772626:
                    continue
                drug_count = user[1]
                user_info = await bot.get_chat(user_id)
                response += f"{counter}) *{user_info.full_name}*: `{drug_count} гр. мефа`\n"
                counter += 1
            await message.reply(response, parse_mode='markdown')
        else:
            await message.reply('Никто еще не принимал меф.')


@dp.message(Command('take'))
async def take_command(message: Message, state: FSMContext):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_banned = user[4] if user else 0
    if is_banned == 1:
        await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        reply_msg = message.reply_to_message
        if reply_msg and reply_msg.from_user.id == 7266772626:
            await message.reply(f'❌ Вы не можете забрать меф у бота')
            return
        elif reply_msg and reply_msg.from_user.id != message.from_user.id:
            user_id = reply_msg.from_user.id
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            your_user_id = message.from_user.id
            cursor.execute('SELECT * FROM users WHERE id = ?', (your_user_id,))
            your_user = cursor.fetchone()
            if user and your_user:
                drug_count = user[1]
                your_drug_count = your_user[1]
                if drug_count > 1 and your_drug_count > 1:
                    last_time = await state.get_data()
                    if last_time and (datetime.now() - last_time['time']) < timedelta(days=1):
                        remaining_time = timedelta(days=1) - (datetime.now() - last_time['time'])
                        await message.reply(f"❌ Нельзя пиздить меф так часто! Ты сможешь спиздить меф через 1 день.")
                    else:
                        variables = ['noticed', 'hit', 'pass']
                        randomed = random.choice(variables)
                        if randomed == 'noticed':
                            cursor.execute('UPDATE users SET drug_count = drug_count - 1 WHERE id = ?', (your_user_id,))
                            conn.commit()
                            await message.reply('❌ *Жертва тебя заметила*, и ты решил убежать. Спиздить меф не получилось. Пока ты бежал, *ты потерял* `1 гр.`', parse_mode='markdown')
                        elif randomed == 'hit':
                            cursor.execute('UPDATE users SET drug_count = drug_count - 1 WHERE id = ?', (your_user_id,))
                            conn.commit()
                            await message.reply('❌ *Жертва тебя заметила*, и пизданула тебя бутылкой по башке бля. Спиздить меф не получилось. *Жертва достала из твоего кармана* `1 гр.`', parse_mode='markdown')
                            
                        elif randomed == 'pass':
                            cursor.execute('UPDATE users SET drug_count = drug_count - 1 WHERE id = ?', (user_id,))
                            cursor.execute('UPDATE users SET drug_count = drug_count + 1 WHERE id = ?', (your_user_id,))
                            conn.commit()
                            if reply_msg.from_user.username:
                                username = reply_msg.from_user.username
                            else:
                                username = f'[{reply_msg.from_user.first_name}](tg://user?id={reply_msg.from_user.id})'
                            await message.reply(f"✅ [{message.from_user.first_name}](tg://user?id={message.from_user.id}) _спиздил(-а) один грам мефа у_ @{username}!", parse_mode='markdown')
                        await state.set_data({'time': datetime.now()})
                elif drug_count < 1:
                    await message.reply('❌ У жертвы недостаточно снюханного мефа для того чтобы его спиздить')
                elif your_drug_count < 1:
                    await message.reply('❌ У тебя недостаточно снюханного мефа для того пойти искать жертву')
            else:
                await message.reply('❌ Этот пользователь еще не нюхал меф')
        else:
            await message.reply('❌ Ответьте на сообщение пользователя, у которого хотите спиздить мефедрон.')
            
@dp.message(Command('casino'))
async def casino(message: Message, command: CommandObject):
    args = command.args
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    drug_count = user[1] if user else 0
    last_used = user[5] if user else 0
    is_banned = user[4] if user else 0
    if is_banned == 1:
        await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        if args:
            try:
                args = args.split(" ", maxsplit=1)[0]
                bet = int(args)
            except ValueError:
                await message.reply(f"🛑 Нужно указать целое число!", parse_mode='markdown')
                return
            if bet < 1:
                await message.reply(f"🛑 Ставка должна быть больше `1` гр.", parse_mode='markdown')
            else:
                if bet > drug_count:
                    await message.reply(f"🛑 Твоя ставка больше твоего баланса!", parse_mode='markdown')
                elif bet <= drug_count:
                    if last_used is not None and (datetime.now() - datetime.fromisoformat(last_used)).total_seconds() < 30:
                        await message.reply('⏳ Ты только что *крутил казик*, солевая обезьяна, *подожди 30 секунд по братски.*', parse_mode='markdown')
                        return
                    else:
                        randomed = random.randint(1,100)
                        multipliers = [2, 1.5, 1.25, 1.1, 0]
                        weights = [1, 2, 3, 4, 5]
                        multiplier = random.choices(multipliers, weights, k=1)[0]
                        if multiplier > 0:
                            cursor.execute('UPDATE users SET drug_count = ? WHERE id = ?', (drug_count - bet, user_id,))
                            conn.commit()
                            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
                            user = cursor.fetchone()
                            drug_count = user[1]
                            bet *= multiplier
                            roundedbet = round(bet, 1)
                            newbalance = round(drug_count+roundedbet, 1)
                            cursor.execute('UPDATE users SET last_casino = ? WHERE id = ?', (datetime.now().isoformat(), user_id,))
                            cursor.execute('UPDATE users SET drug_count = ? WHERE id = ?', (newbalance, user_id,))
                            conn.commit()
                            await bot.send_message(os.environ.get('LOGS_CHAT_ID'), f"#CASINO\n\nfirst_name: <code>{message.from_user.first_name}</code>\nuserid: <code>{user_id}</code>\nbet: <code>{roundedbet}</code>\nmultiplier: <code>{multiplier}</code>\ndrug_count: <code>{drug_count+roundedbet}</code>\n\n<a href='tg://user?id={user_id}'>mention</a>", parse_mode='html')
                            await message.reply(f'🤑 *Ебать тебе повезло!* Твоя ставка *умножилось* на `{multiplier}`. Твой выйгрыш: `{roundedbet}` гр.\nТвой баланс: `{newbalance}` гр.', parse_mode='markdown')
                        elif multiplier == 0:
                            cursor.execute('SELECT drug_count FROM users WHERE id = ?', (7266772626,))
                            botbalance = cursor.fetchone()[0]
                            cursor.execute('UPDATE users SET last_casino = ? WHERE id = ?', (datetime.now().isoformat(), user_id,))
                            cursor.execute('UPDATE users SET drug_count = ? WHERE id = ?', (drug_count-bet, user_id,))
                            cursor.execute('UPDATE users SET drug_count = ? WHERE id = ?', (botbalance+bet, 7266772626,))
                            conn.commit()
                            await bot.send_message(os.environ.get('LOGS_CHAT_ID'), f"#CASINO\n\nfirst_name: `{message.from_user.first_name}`\nuserid: `{user_id}`\nbet: `{bet}`\nmupltiplier: `{multiplier}`\ndrug_count: `{drug_count-bet}`\n\n[mention](tg://user?id={user_id})", parse_mode='markdown')
                            await message.reply('😔 *Ты проебал* свою ставку, *нехуй было* крутить казик.', parse_mode='markdown')
        else:
            await message.reply(f"🛑 Укажи сумму, на которую ты бы хотел сыграть! Пример:\n`/casino 40`", parse_mode='markdown')

@dp.message(Command('give'))
async def give_command(message: Message, state: FSMContext, command: CommandObject):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_banned = user[4] if user else 0
    if is_banned == 1:
        await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        args = command.args.split(' ', maxsplit=1)
        if args:
            try:
                value = int(args[0])
            except ValueError:
                await message.reply(f'❌ Введи целое число')
            reply_msg = message.reply_to_message
            if reply_msg and reply_msg.from_user.id == 7266772626:
                await message.reply(f'❌ Вы не можете передать средства боту')
                return
            elif reply_msg and reply_msg.from_user.id != message.from_user.id:
                user_id = reply_msg.from_user.id
                cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
                user = cursor.fetchone()
                your_user_id = message.from_user.id
                cursor.execute('SELECT * FROM users WHERE id = ?', (your_user_id,))
                your_user = cursor.fetchone()
                if user and your_user:
                    drug_count = your_user[1]
                    last_time = await state.get_data()
                    if value < 0:
                        await message.reply(f'❌ Значение не может быть отрицательным')
                    elif value == 0:
                        await message.reply(f'❌ Значение не может быть равным нулю')
                    elif drug_count >= value and value != 0 and value > 0:
                        commission = round(value * 0.10) 
                        net_value = value - commission 
                        cursor.execute('SELECT drug_count FROM users WHERE id = ?', (7266772626,))
                        botbalance = cursor.fetchone()[0]
                        cursor.execute('UPDATE users SET drug_count = drug_count + ? WHERE id = ?', (net_value, user_id))
                        cursor.execute('UPDATE users SET drug_count = drug_count - ? WHERE id = ?', (value, your_user_id))
                        cursor.execute('UPDATE users SET drug_count = ? WHERE id = ?', (botbalance+commission, 7266772626))
                        conn.commit()
                        await bot.send_message(os.environ.get('LOGS_CHAT_ID'), f"#GIVE\n\nfirst_name: `{message.from_user.first_name}`\nuserid: `{user_id}`\nto: `{reply_msg.from_user.first_name}`\nvalue: `{net_value}`", parse_mode='markdown')
                        if reply_msg.from_user.username:
                            await message.reply(f"✅ [{message.from_user.first_name}](tg://user?id={message.from_user.id}) _подарил(-а) {value} гр. мефа_ [{reply_msg.from_user.first_name}](tg://user?id={reply_msg.from_user.id})!\nКомиссия: `{commission}` гр. мефа\nПолучено `{net_value}` гр. мефа.", parse_mode='markdown')
                        else:
                            await message.reply(f"✅ [{message.from_user.first_name}](tg://user?id={message.from_user.id}) _подарил(-а) {value} гр. мефа_ [{reply_msg.from_user.first_name}](tg://user?id={reply_msg.from_user.id})!\nКомиссия: `{commission}` гр. мефа\nКомиссия: `{commission}` гр. мефа\nПолучено `{net_value}` гр. мефа.", parse_mode='markdown')
                        await state.set_data({'time': datetime.now()})
                    elif drug_count < value:
                        await message.reply(f'❌ Недостаточно граммов мефа для того чтобы их передать')

@dp.message(Command('clancreate'))
async def create_clan(message: Message, command: CommandObject):
    args = command.args
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_banned = user[4] if user else 0
    if is_banned == 1:
        await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        if args:
            args = command.args.split(' ', maxsplit=1)[0]
            clan_name = args
            cursor.execute('SELECT * FROM clans WHERE clan_name = ?', (clan_name,))
            clanexist = cursor.fetchone()
            if clanexist:
                await message.reply('🛑 Клан с таким названием уже существует')
            else:
                clan_id = random.randint(100000, 999999)
                user_id = message.from_user.id
                cursor.execute('SELECT clan_member, drug_count FROM users WHERE id = ?', (user_id,))
                user = cursor.fetchone()
                drug_count = user[1]
                if user[0] is not None:
                    await message.reply(f"🛑 Вы уже состоите в клане.", parse_mode='markdown')
                else:
                    if drug_count >= 100:
                        cursor.execute('INSERT INTO clans (clan_id, clan_name, clan_owner_id, clan_balance) VALUES (?, ?, ?, ?)', (clan_id, clan_name, user_id, 0))
                        cursor.execute('UPDATE users SET clan_member = ? WHERE id = ?', (clan_id, user_id))
                        cursor.execute('UPDATE users SET drug_count = ? WHERE id = ?', (drug_count - 100, user_id))
                        conn.commit()
                        await bot.send_message(os.environ.get('LOGS_CHAT_ID'), f"#NEWCLAN\n\nclanid: `{clan_id}`\nclanname: `{clan_name}`\nclanownerid: `{user_id}`", parse_mode='markdown')
                        await message.reply(f"✅ Клан *{clan_name}* успешно создан.\nВаш идентификатор клана: `{clan_id}`\nС вашего баланса списано `100` гр.",parse_mode='markdown')
                    else:
                        await message.reply(f"🛑 Недостаточно средств.\nСтоимость создания клана: `100` гр.", parse_mode='markdown')
        else:
            await message.reply(f"🛑 Укажи название клана\nПример:\n`/clancreate КрУтЫе_ПеРцЫ`\nСтоимость создания клана: `100` гр.", parse_mode='markdown')

@dp.message(Command('deposit'))
async def deposit(message: Message, command: CommandObject):
    args = command.args.split(' ', maxsplit=1)[0]
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_banned = user[4] if user else 0
    if is_banned == 1:
        await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        if args:
            try:
                cost = int(args)
            except ValueError:
                await message.reply(f'❌ Введи целое число')
                return
            user_id = message.from_user.id
            cursor.execute('SELECT drug_count, clan_member FROM users WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            user_balance = int(user[0])
            clan_id = user[1]
            if clan_id == 0:
                await message.reply(f"🛑 Вы не состоите в клане", parse_mode='markdown')
            elif clan_id > 0:
                cursor.execute('SELECT * FROM clans WHERE clan_id = ?', (clan_id,))
                clan = cursor.fetchone()
                clan_balance = clan[3]
                clan_name = clan[1]
                clan_owner_id = clan[2]
                if cost < 0:
                    await message.reply(f'❌ Значение не может быть отрицательным')
                    return
                elif cost == 0:
                    await message.reply(f'❌ Значение не может быть равным нулю')
                    return
                elif cost > user_balance:
                    await message.reply(f"🛑 Недостаточно средств. Ваш баланс: `{user_balance}` гр.", parse_mode='markdown')
                elif cost <= user_balance and cost != 0:
                    cursor.execute('UPDATE users SET drug_count = ? WHERE id = ?', (user_balance - cost, user_id,))
                    conn.commit()
                    newbalance = clan_balance+cost
                    cursor.execute('UPDATE clans SET clan_balance = ? WHERE clan_owner_id = ?', (newbalance, clan_owner_id,))
                    conn.commit()
                    await message.reply(f"✅ Вы успешно пополнили баланс клана `{clan_name}` на `{cost}` гр.", parse_mode='markdown')
                    await bot.send_message(os.environ.get('LOGS_CHAT_ID'), f"#DEPOSIT\n\nclanname: `{clan_name}`\namount: `{cost}`\nuserid: `{user_id}`\nfirstname: {message.from_user.first_name}\n\n[mention](tg://user?id={user_id})", parse_mode='markdown')
        else:
            await message.reply(f"🛑 Вы не указали сумму. Пример:\n`/deposit 100`", parse_mode='markdown')

@dp.message(Command('withdraw'))
async def withdraw(message: Message, command: CommandObject):
    args = command.args.split(' ', maxsplit=1)[0]
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_banned = user[4] if user else 0
    if is_banned == 1:
        await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        if args:
            try:
                cost = int(args)
            except ValueError:
                await message.reply(f'❌ Введи целое число')
            user_id = message.from_user.id
            cursor.execute('SELECT drug_count, clan_member FROM users WHERE id = ?', (user_id,))
            user = cursor.fetchone()
            user_balance = int(user[0])
            clan_id = user[1]
            if clan_id == 0:
                await message.reply(f"🛑 Вы не состоите в клане", parse_mode='markdown')
            elif clan_id > 0:
                cursor.execute('SELECT * FROM clans WHERE clan_id = ?', (clan_id,))
                clan = cursor.fetchone()
                clan_balance = clan[3]
                clan_name = clan[1]
                clan_owner_id = clan[2]
                if user_id != clan_owner_id:
                    await message.reply(f"🛑 Снимать деньги со счёта клана может только его владелец.", parse_mode='markdown')
                else:
                    if cost < 0:
                        await message.reply(f'❌ Значение не может быть отрицательным')
                        return
                    elif cost == 0:
                        await message.reply(f'❌ Значение не может быть равным нулю')
                        return
                    elif cost > clan_balance:
                        await message.reply(f"🛑 Недостаточно средств. Баланс клана: `{clan_balance}` гр.", parse_mode='markdown')
                    elif cost <= clan_balance and cost != 0:
                        cursor.execute('UPDATE clans SET clan_balance = ? WHERE clan_owner_id = ?', (clan_balance - cost, user_id,))
                        cursor.execute('UPDATE users SET drug_count = ? WHERE id = ?', (user_balance + cost, user_id,))
                        conn.commit()
                        await message.reply(f"✅ Вы успешно сняли `{cost}` гр. мефа с баланса клана `{clan_name}`", parse_mode='markdown')
                        await bot.send_message(os.environ.get('LOGS_CHAT_ID'), f"#WITHDRAW\n\namount: `{cost}`\nclanname: `{clan_name}`\nuserid: {user_id}\n\n[mention](tg://user?id={user_id})", parse_mode='markdown')
        else:
            await message.reply(f"🛑 Вы не указали сумму. Пример:\n`/withdraw 100`", parse_mode='markdown')


@dp.message(Command('clantop'))
async def clan_top(message: Message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_banned = user[4] if user else 0
    if is_banned == 1:
        await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        cursor.execute('SELECT clan_name, clan_balance FROM clans ORDER BY clan_balance DESC LIMIT 10')
        top_clans = cursor.fetchall()
        if top_clans:
            response = "🔝ТОП 10 МЕФЕДРОНОВЫХ КАРТЕЛЕЙ В МИРЕ🔝:\n"
            counter = 1
            for clan in top_clans:
                clan_name = clan[0]
                clan_balance = clan[1]
                response += f"{counter}) *{clan_name}*  `{clan_balance} гр. мефа`\n"
                counter += 1
            await message.reply(response, parse_mode='markdown')
        else:
            await message.reply('🛑 Ещё ни один клан не пополнил свой баланс.')

@dp.message(Command('clanbalance'))
async def clanbalance(message: Message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_banned = user[4] if user else 0
    clan_id = user[7] if user else 0
    cursor.execute('SELECT clan_balance, clan_name FROM clans WHERE clan_id = ?', (clan_id,))
    clan = cursor.fetchone()
    if is_banned == 1:
        await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        if clan_id == 0:
             await message.reply(f"🛑 Вы не состоите в клане", parse_mode='markdown')
        elif clan_id > 0:
            clan_balance = clan[0]
            clan_name = clan[1]
            await message.reply(f'✅ Баланс клана *{clan_name}* - `{clan_balance}` гр.', parse_mode='markdown')

@dp.message(Command('clanwar'))
async def clanwar(message: Message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_banned = user[4] if user else 0
    clan_id = user[7] if user else 0
    if is_banned == 1:
        await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        if clan_id == 0:
            await message.reply(f"🛑 *Вы не состоите в клане*", parse_mode='markdown')
        elif clan_id > 0:
            cursor.execute('SELECT clan_name, clan_owner_id FROM clans WHERE clan_id = ?', (clan_id,))
            clan = cursor.fetchone()
            clan_name = clan[0]
            clan_owner_id = clan[1]
            if user_id != clan_owner_id:
                await message.reply(f"🛑 *Вы не являетесь владельцем клана*", parse_mode='markdown')
                return
            if len(message.text.split()) < 2:
                await message.reply(f"🛑 *Вы не указали идентификатор клана для начала войны*", parse_mode='markdown')
                return
            target_clan_id = message.text.split()[1]
            cursor.execute('SELECT clan_name FROM clans WHERE clan_id = ?', (target_clan_id,))
            target_clan = cursor.fetchone()
            if not target_clan:
                await message.reply(f"🛑 *Не удалось найти клан с указанным идентификатором*", parse_mode='markdown')
                return
            target_clan_name = target_clan[0]
            await message.reply(f"*Клан {clan_name} начал войну с {target_clan_name}!*", parse_mode='markdown')
            
            cursor.execute('SELECT chat_id FROM chats')
            chats = cursor.fetchall()
            for chat_id in chats:
                try:
                    await bot.send_message(chat_id[0], f"*Клан {clan_name} начал войну с {target_clan_name}!*", parse_mode='markdown')
                except Exception as e:
                    print(f"Ошибка отправки сообщения в {chat_id}: {e}")

@dp.message(Command('clanowner'))
async def clan_owner(message: Message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_banned = user[4] if user else 0
    clan_id = user[7] if user else 0
    if is_banned == 1:
        await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        if clan_id == 0:
            await message.reply(f"🛑 *Вы не состоите в клане*", parse_mode='markdown')
        elif clan_id > 0:
            cursor.execute('SELECT clan_owner_id FROM clans WHERE clan_id = ?', (clan_id,))
            current_owner_id = cursor.fetchone()[0]
            if user_id != current_owner_id:
                await message.reply(f"🛑 *Вы не являетесь владельцем клана*", parse_mode='markdown')
                return

            if message.reply_to_message:
                new_owner_id = message.reply_to_message.from_user.id
            elif len(message.text.split()) >= 2:
                new_owner_id = int(message.text.split()[1])
            else:
                await message.reply(f"🛑 *Вы не указали нового владельца клана*", parse_mode='markdown')
                return
            
            cursor.execute('SELECT * FROM users WHERE id = ?', (new_owner_id,))
            new_owner = cursor.fetchone()
            if not new_owner:
                await message.reply(f"🛑 *Не удалось найти пользователя с указанным идентификатором*", parse_mode='markdown')
                return
            cursor.execute('UPDATE clans SET clan_owner_id = ? WHERE clan_id = ?', (new_owner_id, clan_id))
            conn.commit()
            await message.reply(f"✅ *Вы передали владельца клана!*", parse_mode='markdown')


@dp.message(Command('claninfo'))
async def claninfo(message: Message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_banned = user[4] if user else 0
    clan_id = user[7] if user else 0
    cursor.execute('SELECT clan_balance, clan_name, clan_owner_id FROM clans WHERE clan_id = ?', (clan_id,))
    clan = cursor.fetchone()
    if is_banned == 1:
        await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        if clan_id == 0:
             await message.reply(f"🛑 Вы не состоите в клане", parse_mode='markdown')
        elif clan_id > 0:
            clan_balance = clan[0]
            clan_name = clan[1]
            clan_owner_id = clan[2]
            clan_owner = await bot.get_chat(clan_owner_id)
            await message.reply(f"👥 Клан: `{clan_name}`\n👑 Владелец клана: [{clan_owner.first_name}](tg://user?id={clan_owner_id})\n🌿 Баланс клана `{clan_balance}` гр.", parse_mode='markdown')   

@dp.message(Command('clanmembers'))
async def clanmembers(message: Message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_banned = user[4] if user else 0

    if is_banned == 1:
        await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        clan_id = user[7] if user else 0
        cursor.execute('SELECT * FROM users WHERE clan_member = ?', (clan_id,))
        clan_members = cursor.fetchall()
        cursor.execute('SELECT clan_name, clan_owner_id FROM clans WHERE clan_id = ?', (clan_id,))
        clan = cursor.fetchone()
        if clan:
            clan_name = clan[0]
            clan_owner_id = clan[1]
            if clan_id > 0:
                if clan_members:
                    response = f"👥 Список участников клана *{clan_name}*:\n"
                    counter = 1
                    clan_owner = None
                    for member in clan_members:
                        if member[0] == clan_owner_id:
                            clan_owner = member
                            break
                    if clan_owner:
                        user_info = await bot.get_chat(clan_owner[0])
                        response += f"{counter}) *{user_info.full_name}* 👑\n"
                        counter += 1
                    for member in clan_members:
                        if member[0] != clan_owner_id:
                            user_info = await bot.get_chat(member[0])
                            response += f"{counter}) {user_info.full_name}\n"
                            counter += 1
                    await message.reply(response, parse_mode='markdown')
        else:
            await message.reply(f"🛑 Вы не состоите в клане", parse_mode='markdown')

@dp.message(Command('claninvite'))
async def claninvite(message: Message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_banned = user[4] if user else 0
    clan_id = user[7] if user else 0
    cursor.execute('SELECT clan_balance, clan_name, clan_owner_id FROM clans WHERE clan_id = ?', (clan_id,))
    clan = cursor.fetchone()
    if is_banned == 1:
        await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        if clan:
            clan_name = clan[1]
            clan_owner_id = clan[2]
            if user_id == clan_owner_id:
                reply_msg = message.reply_to_message
                if reply_msg and reply_msg.from_user.id == 7266772626:
                    await message.reply(f'❌ Вы не можете пригласить бота в клан')
                    return
                elif reply_msg:
                    user_id = reply_msg.from_user.id
                    cursor.execute('SELECT clan_member, clan_invite FROM users WHERE id = ?', (user_id,))
                    user = cursor.fetchone()
                    clan_member = user[0]
                    clan_invite = user[1]
                    try:
                        cursor.execute('INSERT INTO users (id, drug_count, is_admin, is_banned, clan_member, clan_invite) VALUES (?, 0, 0, 0, 0, 0)', (user_id,))
                        conn.commit()
                        cursor.execute('SELECT clan_member, clan_invite FROM users WHERE id = ?', (user_id,))
                        user = cursor.fetchone()
                        clan_member = user[0]
                        clan_invite = user[1]
                    except:
                        pass
     
                    if clan_member == 0 and clan_invite == 0:
                        if user:
                            cursor.execute('UPDATE users SET clan_invite = ? WHERE id = ?', (clan_id, user_id))
                        else:
                            cursor.execute('INSERT INTO users (id, drug_count, is_admin, is_banned, clan_member, clan_invite) VALUES (?, 0, 0, 0, 0, ?)', (user_id, clan_id))
                        conn.commit()
                        await message.reply(f'✅ Пользователь {reply_msg.from_user.first_name} *приглашён в клан {clan_name}* пользователем {message.from_user.first_name}\nДля того чтобы принять приглашение, *введите команду* `/clanaccept`\nДля того чтобы отказаться от приглашения, *введите команду* `/clandecline`', parse_mode='markdown')
                    
                         
                    elif clan_member is None and clan_invite is None:
                        if user:
                            cursor.execute('UPDATE users SET clan_invite = ? WHERE id = ?', (clan_id, user_id))
                        else:
                            cursor.execute('INSERT INTO users (id, drug_count, is_admin, is_banned, clan_member, clan_invite) VALUES (?, 0, 0, 0, 0, ?)', (user_id, clan_id))
                        conn.commit()
                        await message.reply(f'✅ Пользователь {reply_msg.from_user.first_name} *приглашён в клан {clan_name}* пользователем {message.from_user.first_name}\nДля того чтобы принять приглашение, *введите команду* `/clanaccept`\nДля того чтобы отказаться от приглашения, *введите команду* `/clandecline`', parse_mode='markdown')
                    
                    
                    elif clan_invite > 0:
                        await message.reply(f"🛑 Этот пользователь уже имеет активное приглашение", parse_mode='markdown')
                    elif clan_member > 0:
                        await message.reply(f"🛑 Этот пользователь уже в клане", parse_mode='markdown')
            elif user_id != clan_owner_id:
                await message.reply(f"🛑 Приглашать в клан может только создатель", parse_mode='markdown')
        else:
            await message.reply(f"🛑 {sys.exc_info()[0]}")

@dp.message(Command('clankick'))
async def clankick(message: Message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_banned = user[4] if user else 0
    clan_id = user[7] if user else 0
    cursor.execute('SELECT clan_balance, clan_name, clan_owner_id FROM clans WHERE clan_id = ?', (clan_id,))
    clan = cursor.fetchone()
    clan_name = clan[1]
    clan_owner_id = int(clan[2])
    if is_banned == 1:
        await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        if clan_id == 0:
            await message.reply(f"🛑 Вы не состоите в клане", parse_mode='markdown')
        elif clan_id > 0 and user_id == clan_owner_id:
            reply_msg = message.reply_to_message
            if reply_msg:
                user_id = reply_msg.from_user.id
                username = reply_msg.from_user.username
                usernameinviter = message.from_user.username.replace('_', '\n')
                cursor.execute('UPDATE users SET clan_member = ? WHERE id = ?', (0, user_id))
                conn.commit()
                await message.reply(f'✅ Пользователь @{username} *исключен из клана {clan_name}* пользователем @{usernameinviter}', parse_mode='markdown')
        elif clan_id > 0 and user_id != clan_owner_id:
            await message.reply(f"🛑 Исключать из клана может только создатель", parse_mode='markdown')

@dp.message(Command('clanleave'))
async def clanleave(message: Message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_banned = user[4] if user else 0
    clan_id = user[7] if user else 0
    cursor.execute('SELECT clan_balance, clan_name, clan_owner_id FROM clans WHERE clan_id = ?', (clan_id,))
    clan = cursor.fetchone()
    clan_name = clan[1]
    clan_owner_id = int(clan[2])
    if is_banned == 1:
        await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        if clan_id == 0:
            await message.reply(f"🛑 Вы не состоите в клане", parse_mode='markdown')
        elif clan_id > 0 and user_id != clan_owner_id:
            cursor.execute('UPDATE users SET clan_member = ? WHERE id = ?', (0, user_id))
            conn.commit()
            await message.reply(f'✅ *Вы покинули* клан *{clan_name}*', parse_mode='markdown')
        elif clan_id > 0 and user_id == clan_owner_id:
            await message.reply(f"🛑 Создатель клана не может его покинуть", parse_mode='markdown')

@dp.message(Command('clandisband'))
async def clandisband(message: Message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_banned = user[4] if user else 0
    clan_id = user[7] if user else 0
    cursor.execute('SELECT clan_owner_id, clan_name FROM clans WHERE clan_id = ?', (clan_id,))
    clan = cursor.fetchone()

    if is_banned == 1:
        await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        try:
            clan_owner_id = clan[0]
            clan_name = clan[1]
        except:
            await message.reply(f"🛑 Вы не состоите в клане", parse_mode='markdown')
        if clan_id > 0 and user_id == clan_owner_id:
            cursor.execute('DELETE FROM clans WHERE clan_id = ?', (clan_id,))
            cursor.execute('UPDATE users SET clan_member = 0 WHERE clan_member = ?', (clan_id,))
            cursor.execute('UPDATE users SET clan_invite = 0 WHERE clan_invite = ?', (clan_id,))
            conn.commit()
            await message.reply(f'✅ Вы распустили клан `{clan_name}`', parse_mode='markdown')
        elif clan_id > 0 and user_id != clan_owner_id:
            await message.reply(f"🛑 Вы не владелец клана!", parse_mode='markdown')

@dp.message(Command('clanaccept'))
async def clanaccept(message: Message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_banned = user[4] if user else 0
    clan_invite = user[8] if user else 0
    if is_banned == 1:
        await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        if clan_invite:
            if clan_invite != 0:
                cursor.execute('SELECT clan_name FROM clans WHERE clan_id = ?', (clan_invite,))
                clan = cursor.fetchone()
                clan_name = clan[0]
                cursor.execute('UPDATE users SET clan_member = ? WHERE id = ?', (clan_invite, user_id))
                cursor.execute('UPDATE users SET clan_invite = 0 WHERE id = ?', (user_id,))
                conn.commit()
                await message.reply(f'✅ *Вы приняли* приглашение в клан *{clan_name}*', parse_mode='markdown')
        else:
            await message.reply('🛑 Вы ещё не получали приглашений в клан')
        
@dp.message(Command('clandecline'))
async def clandecline(message: Message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_banned = user[4] if user else 0
    clan_invite = user[8] if user else 0
    if is_banned == 1:
        await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        if clan_invite:
            if clan_invite != 0:
                cursor.execute('SELECT clan_name FROM clans WHERE clan_id = ?', (clan_invite,))
                clan = cursor.fetchone()
                clan_name = clan[0]
                cursor.execute('UPDATE users SET clan_invite = 0 WHERE id = ?', (user_id,))
                conn.commit()
                await message.reply(f'❌ *Вы отклонили* приглашение в клан *{clan_name}*', parse_mode='markdown')
        else:
            await message.reply('🛑 Вы ещё не получали приглашений в клан')
        


@dp.message(Command('find'))
async def drug_command(message: Message, state: FSMContext):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    drug_count = user[1] if user else 0
    last_time = await state.get_data()
    last_used = user[6] if user else '2021-02-14 16:04:04.465506'
    is_banned = user[4] if user else 0
    if is_banned == 1:
        await message.reply('🛑 Вы заблокированы в боте!')
    elif is_banned == 0:
        if last_used is not None and (datetime.now() - datetime.fromisoformat(last_used)).total_seconds() < 43200:
            await message.reply('⏳ Ты недавно *ходил за кладом, подожди 12 часов.*', parse_mode='markdown')
            return
        else:
            if random.randint(1,100) > 50:
                count = random.randint(1, 10)
                if user:
                    cursor.execute('UPDATE users SET drug_count = ? WHERE id = ?', (drug_count + count, user_id))
                else:
                    cursor.execute('INSERT INTO users (id, drug_count, is_admin, is_banned, clan_member, clan_invite) VALUES (?, ?, ?, ?, ?, ?)', (user_id, count, 0, 0, 0, 0))
                cursor.execute('UPDATE users SET last_use_time = ? WHERE id = ?', ('2006-02-20 12:45:37.666666', user_id,))
                cursor.execute('UPDATE users SET last_find = ? WHERE id = ?', (datetime.now().isoformat(), user_id,))
                conn.commit()
                await bot.send_message(os.environ.get('LOGS_CHAT_ID'), f"#FIND #WIN\n\nfirst_name: `{message.from_user.first_name}`\ncount: `{count}`\ndrug_count: `{drug_count+count}`\n\n[mention](tg://user?id={user_id})", parse_mode='markdown')
                await message.reply(f"👍 {message.from_user.first_name}, ты пошёл в лес и *нашел клад*, там лежало `{count} гр.` мефчика!\n🌿 Твое время команды /drug обновлено", parse_mode='markdown')
            elif random.randint(1,100) <= 50:
                count = random.randint(1, round(drug_count))
                cursor.execute('UPDATE users SET drug_count = ? WHERE id = ?', (drug_count - count, user_id,))
                conn.commit()
                await bot.send_message(os.environ.get('LOGS_CHAT_ID'), f"#FIND #LOSE\n\nfirst_name: `{message.from_user.first_name}`\ncount: `{count}`\ndrug_count: `{drug_count-count}`\n\n[mention](tg://user?id={user_id})", parse_mode='markdown')
                await message.reply(f"❌ *{message.from_user.first_name}*, тебя *спалил мент* и *дал тебе по ебалу*\n🌿 Тебе нужно откупиться, мент предложил взятку в размере `{count} гр.`\n⏳ Следующая попытка доступна через *12 часов.*", parse_mode='markdown')
                


@dp.message(Command('banuser'))
async def banuser_command(message: Message, command: CommandObject):
    args = command.args.split(' ', maxsplit=1)[0]
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_admin = user[3]
    if is_admin == 1:
        reply_msg = message.reply_to_message
        if reply_msg and reply_msg.from_user.id != message.from_user.id:
            bann_user_id = reply_msg.from_user.id
            cursor.execute('UPDATE users SET is_banned = 1 WHERE id = ?', (bann_user_id,))
            conn.commit()
        elif args:
            bann_user_id = int(args)
            cursor.execute('UPDATE users SET is_banned = 1 WHERE id = ?', (bann_user_id,))
            conn.commit()
        await message.reply(f"🛑 Пользователь с ID: `{bann_user_id}` заблокирован", parse_mode='markdown')
        await bot.send_message(os.environ.get('LOGS_CHAT_ID'), f"#BAN\n\nid: {bann_user_id}")
    elif is_admin == 0:
        await message.reply('🚨 MONKEY ALARM')

@dp.message(Command('unbanuser'))
async def unbanuser_command(message: Message, command: CommandObject):
    args = command.args.split(' ', maxsplit=1)[0]
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_admin = user[3]
    if is_admin == 1:
        reply_msg = message.reply_to_message
        if reply_msg and reply_msg.from_user.id != message.from_user.id:
            bann_user_id = reply_msg.from_user.id
            cursor.execute('UPDATE users SET is_banned = 0 WHERE id = ?', (bann_user_id,))
            conn.commit()
        elif args:
            bann_user_id = int(args)
            cursor.execute('UPDATE users SET is_banned = 0 WHERE id = ?', (bann_user_id,))
            conn.commit()
        else:
            bann_user_id = None
        if bann_user_id is not None:
            await message.reply(f"🛑 Пользователь с ID: `{bann_user_id}` разблокирован", parse_mode='markdown')
            await bot.send_message(os.environ.get('LOGS_CHAT_ID'), f"#UNBAN\n\nid: {bann_user_id}")
    elif is_admin == 0:
        await message.reply('🚨 MONKEY ALARM')


@dp.message(Command('about'))
async def about_command(message: Message):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    channel_button = InlineKeyboardButton('📢 Канал', url='https://t.me/mefmetrch')
    donate_button = InlineKeyboardButton('💰 Донат', url='https://t.me/mefmetrch')
    chat_button = InlineKeyboardButton('💬 Чат', url='https://t.me/mefmetrchat')
    keyboard.row(channel_button, donate_button, chat_button)
    await message.reply("🧑‍💻 Бот разработан xanaxnotforfree.t.me", reply_markup=keyboard)

@dp.message(Command('setdrugs'))
async def setdrugs_command(message: Message, command: CommandObject):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_admin = user[3]
    if is_admin == 1:
        args = command.args.split(' ', maxsplit=1)
        cursor.execute('UPDATE users SET drug_count = ? WHERE id = ?', (args[1],args[0]))
        conn.commit()
        await message.reply('✅')
    elif is_admin == 0:
        await message.reply('🚨 MONKEY ALARM')

@dp.message(Command('usercount'))
async def usercount(message: Message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_admin = user[3]
    cursor.execute('SELECT COUNT(id) FROM users')
    user = cursor.fetchone()[0]
    if is_admin == 1:
        await message.reply(f'Количество пользователей в боте: {user}')
    else:
        await message.reply('🚨 MONKEY ALARM')

@dp.message(Command('broadcast'))
async def cmd_broadcast_start(message: Message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    is_admin = user[3]
    cursor.execute('SELECT COUNT(id) FROM users')
    user = cursor.fetchone()[0]
    reply = message.reply_to_messageos.environ.get('LOGS_CHAT_ID')
    result = cursor.execute('SELECT * FROM chats')
    if is_admin == 1:
        if reply:
            if reply.photo:
                if reply.caption:
                    await message.reply('Начинаю рассылку')
                    for row in result:
                        try:
                            chat_id = row[0]
                            await bot.send_photo(chat_id, reply.photo[-1].file_id, caption=f"{reply.caption}", parse_mode='markdown')
                        except:
                            await bot.send_message(os.environ.get('LOGS_CHAT_ID'), f"#SENDERROR\n\nchatid: {chat_id}\nerror: {sys.exc_info()[0]}")
                            continue
                else:
                    await message.reply('Начинаю рассылку')
                    for row in result:
                        try:
                            chat_id = row[0]
                            await bot.send_photo(chat_id, reply.photo[-1].file_id)
                        except:
                            await bot.send_message(os.environ.get('LOGS_CHAT_ID'), f"#SENDERROR\n\nchatid: {chat_id}\nerror: {sys.exc_info()[0]}")
                            continue
            elif reply.text:
                await message.reply('Начинаю рассылку')
                for row in result:
                    try:
                        chat_id = row[0]
                        await bot.send_message(chat_id, f"{reply.text}", parse_mode='markdown')
                    except:
                        await bot.send_message(os.environ.get('LOGS_CHAT_ID'), f"#SENDERROR\n\nchatid: {chat_id}\nerror: {sys.exc_info()[0]}")
                        continue
        else:
            await message.reply('Ответь на сообщение с текстом или фото для рассылки')
    else:
        await message.reply('🚨 MONKEY ALARM')

@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=IS_NOT_MEMBER >> MEMBER
    )
)
async def add_chat(event: ChatMemberUpdated):
    bot_obj = await bot.get_me()
    bot_id = bot_obj.id
    cursor.execute('INSERT INTO chats (chat_id, is_ads_enable) VALUES (?, ?)', (event.chat.id, 1))
    conn.commit()
    await bot.send_message(os.environ.get('LOGS_CHAT_ID'), f"#NEWCHAT\n\nchatid: `{event.chat.id}`", parse_mode='markdown')

async def run():
    await dp.start_polling(bot)

def main():
    asyncio.run(run())

if __name__ == "__main__":
    main()