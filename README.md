WeatherBot (Telegram Bot на Aiogram 3)

Участники проекта: 
- Черток Герман Константинович
474391 
- Застенская Анастасия Романовна 
474288

Ссылка на бота: 
- @ItmoWeather_bot

WeatherBot — это телеграм-бот, позволяющий пользователям быстро получать актуальную информацию о погоде в любом городе мира.
Проект реализован на библиотеке aiogram 3 и поддерживает:

- локализацию на русском и английском языках
- инлайн-меню с callback-обработкой
- взаимодействие с внешним API погоды (OpenWeatherMap)
- кэширование данных
- FSM (машину состояний) для ввода города
- антиспам middleware
- админ-панель (статистика, рассылка, бан пользователей)
- хранение пользователей и избранных городов в users.json
- логирование в logs/bot.log
- основные команды /start, /help, /weather, /favorites, /language

Запуск бота: 
1. git clone  .. / cd ..
2. python -m venv 
3. venv source venv/bin/activate  /  venv\Scripts\activate  (MacOs/Windows)
4. pip install -r requirements.txt
5. Для использования админ-панели внесите свой Id в .env 

Структура проекта: 
weather_bot/
├── bot.py                       
├── config/
│   ├── __init__.py
│   └── settings.py              
├── routers/
│   ├── __init__.py
│   └── handlers/
│       ├── __init__.py
│       ├── main.py                
│       └── admin.py             
├── keyboards/
│   ├── __init__.py
│   └── menu.py                    
├── services/
│   ├── __init__.py
│   └── api_client.py            
├── storage/
│   ├── __init__.py
│   └── user_data.py              
├── states/
│   ├── __init__.py
│   ├── weather_states.py
│   └── admin_states.py
├── middlewares/
│   ├── __init__.py
│   └── throttling.py            
├── filters/
│   ├── __init__.py
│   ├── admin_filter.py
│   └── length_filter.py
├── locales/
│   ├── __init__.py
│   ├── loader.py               
│   ├── en.json
│   └── ru.json
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   └── formatters.py            
├── logs/
│   └── bot.log                
├── storage/
│   └── users.json             
├── requirements.txt
└── README.md
