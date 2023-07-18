<h1> ПОГОДНИК </h1>
<hr>
Данный проект создан для взаимодействия пользователя с телеграм ботом,
который предоставляет данные о погоде в определенном городе. Для 
взаимодействия с ботом, нужно лишь написать ему необходимый город, он 
в свою очередь предоставит данные о погоде города.

Найти моего бота можно перейдя по [ссылке](https://t.me/KKitTyCaTTbot)

<hr>

<h3>Требования</h3>

Для установки и запуска проекта, необходим Python3.9+

<hr>

<h3>Клонирование репозитория</h3>

Для просмотра исходного кода нужно клонировать репозиторий:

`git clone git@github.com:DanilVolodchenko/weather.git`

<hr>

<h3>Установка зависимостей</h3>

Для работы в первую очередь нужно установить виртуальное окружение:

`python -m venv venv`

Далее активируем виртуальное окружение:

`source venv/Scripts/activate`

Устанавливаем зависимости, находящиеся в файле requirements.txt

`pip install -r requirements.txt`

<hr>

<h3>Настройка переменных окружения</h3>

В директории `./Weather/weather/` настраиваем переменные окружения, для этого создаем файл .env

`touch .env`, где будут храниться API ключ для получения данных о погоде и телеграм токен

[Здесь](https://www.weatherapi.com) можно получить API ключа

[Тут](https://t.me/BotFather) создать бота и получить телеграм токен

Файл .env должен содержать следующие данные:

    API_KEY=ВАШ API КЛЮЧ
    TELEGRAM_TOKEN=ВАШ ТЕЛЕГРАМ ТОКЕН

<hr>

<h3>ГОТОВО!</h3>

Переходим в директорию проекта weather `./Weather/weather/` и запускаема код:

`python main.py` и наслаждаемся. 

Если есть какие-либо предложения по улучшению кода или тестов, связаться можно со мной в [телеграме](https://t.me/VolodchenkoDanil)