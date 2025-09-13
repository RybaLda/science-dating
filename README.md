# 🔬 Science Dating

Telegram Mini App для знакомств среди ученых и исследователей.

## 🚀 Быстрый старт

### Деплой на Render

#### 1. Static Site (WebApp)
- **Type**: Static Site
- **Name**: `science-dating-web`
- **Publish Directory**: `web`
- **URL**: `https://science-dating-web.onrender.com` (станет WEBAPP_URL)

#### 2. Web Service (Bot)
- **Type**: Web Service
- **Name**: `science-dating-bot`
- **Environment**: Python
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn bot.main:app --host 0.0.0.0 --port $PORT`

#### 3. Environment Variables
Настройте следующие переменные окружения для бота:

```
BOT_TOKEN=your_telegram_bot_token
WEBAPP_URL=https://science-dating-web.onrender.com
PUBLIC_URL=https://science-dating-bot.onrender.com
```

**Важно**: Сначала оставьте `PUBLIC_URL` пустым, после первого деплоя скопируйте External URL и установите как `PUBLIC_URL`, затем сделайте redeploy.

## 🔧 Локальная разработка

### Требования
- Python 3.11+
- Telegram Bot Token

### Установка
```bash
cd science-dating
pip install -r requirements.txt
```

### Запуск
```bash
# Установите переменные окружения
export BOT_TOKEN=your_bot_token
export WEBAPP_URL=http://localhost:3000  # для локального тестирования

# Запустите бота
cd bot
python main.py
```

## 📱 Функции WebApp

### Основные экраны
1. **Лендинг** - главное меню с кнопками навигации
2. **Лента/Свайпы** - просмотр профилей с фильтрацией
3. **Матч** - оверлей при совпадении интересов
4. **Чат** - общение с матчами
5. **Профиль** - создание и редактирование профиля
6. **Панель персонажей** - управление демо-данными

### Особенности
- ✅ Мобильный UI 9:16 с темной темой
- ✅ Интеграция с Telegram WebApp SDK
- ✅ Автоматическая синхронизация темы
- ✅ Автологин через Telegram данные
- ✅ Локальное хранение данных (localStorage)
- ✅ Генерация аватаров по инициалам
- ✅ Экспорт/импорт данных

## 🤖 Функции бота

### Команды
- `/start` - главное меню с кнопкой WebApp
- `/demo` - демо-режим с готовыми профилями
- `/help` - справка по использованию

### Особенности
- ✅ Webhook для production
- ✅ Polling для development
- ✅ Menu Button WebApp
- ✅ Обработка всех типов сообщений

## ✅ Проверка работы

### WebApp
1. Откройте `WEBAPP_URL` в браузере
2. Пройдите age-gate (18+)
3. Нажмите "Быстрый демо-режим"
4. Протестируйте свайпы, фильтры, матчи
5. Проверьте чат и создание профиля
6. Используйте панель персонажей

### Telegram Bot
1. Найдите бота в Telegram
2. Отправьте `/start`, `/demo`, `/help`
3. Проверьте, что приходят кнопки WebApp
4. В меню чата должна быть кнопка "Science Dating"

### Webhook (Production)
```bash
curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo
```
Должно показать:
- `url`: `PUBLIC_URL/webhook/<TOKEN>`
- `last_error_date`: отсутствует
- `last_error_message`: отсутствует

## 🛠 Технические детали

### Frontend
- Чистый HTML/CSS/JavaScript
- Telegram WebApp SDK
- localStorage для данных
- Canvas для генерации аватаров
- Responsive дизайн

### Backend
- Python 3.11+
- aiogram v3 для Telegram Bot API
- FastAPI для webhook
- uvicorn для ASGI сервера

### Деплой
- Render.com для хостинга
- Static Site для WebApp
- Web Service для бота
- Environment variables для конфигурации

## 📁 Структура проекта

```
science-dating/
├── web/
│   └── index.html          # WebApp (одностраничное приложение)
├── bot/
│   └── main.py             # Telegram бот + FastAPI
├── requirements.txt        # Python зависимости
├── render.yaml            # Blueprint для Render
└── README.md              # Документация
```

## 🐛 Устранение неполадок

### WebApp не открывается в Telegram
- Проверьте, что WEBAPP_URL доступен
- Убедитесь, что бот имеет права на WebApp

### Webhook не работает
- Проверьте PUBLIC_URL в переменных окружения
- Убедитесь, что URL доступен извне
- Проверьте логи бота на ошибки

### Локальная разработка
- Используйте ngrok для туннелирования
- Установите PUBLIC_URL на ngrok URL
- Перезапустите бота после изменения переменных

## 📄 Лицензия

MIT License - используйте свободно для своих проектов.
