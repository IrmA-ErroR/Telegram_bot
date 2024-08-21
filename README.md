# Telegram_bot
First and test telegram bot

Name: d4i1y_weather_bot


Настройка виртуального окружения: 
```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt install python3.10-venv
python3 -m venv .venv

source .venv/bin/activate # Активация виртуального окружения

# Установка Telegram Bot API
sudo apt-get install make git zlib1g-dev libssl-dev gperf cmake clang-14 libc++-14-dev libc++abi-14-dev
git clone --recursive https://github.com/tdlib/telegram-bot-api.git
cd telegram-bot-api
rm -rf build
mkdir build
cd build
CXXFLAGS="-stdlib=libc++" CC=/usr/bin/clang-14 CXX=/usr/bin/clang++-14 cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX:PATH=/usr/local ..
sudo cmake --build . --target install
cd ../..
ls -l /usr/local/bin/telegram-bot-api*
```

Проверяем, что работает: 
```bash
telegram-bot-api
````