# Установка
1. `git clone https://github.com/troshchiy/EvoSoft_Web_Reverse_Engineer_test_task.git`
2. `cd EvoSoft_Web_Reverse_Engineer_test_task`
3. `python3 -m venv venv`
4. `source venv/bin/activate`(Linux) или `venv\Scripts\activate`(Windows)
5. `pip install -r requirements.txt`

# Парсер данных через Selenuim

Алгоритм:
1. Зайти на https://www.nseindia.com
2. Навестись (hover) на MARKET DATA
3. Кликнуть на Pre-Open Market
4. Спарсить данные Final Price по всем позициям на странице и вывести их в csv файл.
Имя;цена После этого сымитировать небольшой пользовательский сценарий
использования сайта. Здесь по своему желанию, но как пример:
   1. Зайти на главную страницу
   2. Пролистать вниз до графика
   3. Выбрать график "NIFTY BANK"
   4. Нажать “View all” под "TOP 5 STOCKS - NIFTY BANK"
   5. Выбрать в селекторе “NIFTY ALPHA 50”
   6. Пролистать таблицу до конца

```commandline
python3 nseindia_parser.py
```
```commandline
cat pre_open_market_data.csv
```

# Парсинг твитов Elon Musk

Используя HTTP-запросы получить список 10 твитов Илона Маска .
Вывести в лог только текст (если есть) твитов. Действия должны повторять
пользовательский путь, официальное API Twitter в задаче не должно быть использовано.
Обязательные условия:
- Не использовать selenium
- Не использовать сторонние библиотеки (nitter, twitty, rss и т.д.)
- Использовать для задания любой http клиент, использовать только запросы Twitter

```commandline
python3 twitter_parser.py
```
