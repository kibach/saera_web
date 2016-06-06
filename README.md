# Установка
1. Обновляем данные из репов (я обновил миграции, если изменяли чето то просто searchres/migrations перекачать)
2. Ставим модули, mysql, все вот это.
   ```sudo apt install mysql-server
   pip install daemonize mysqldb django peewee snowballstemmer langdetect beautifulsoup4```
   MySQL при установке должна была запросить пароль, вспоминаем его.
   ```mysql -u root -p<passwd>
   (внутри)
   CREATE DATABASE saera_search CHARACTER SET utf8 COLLATE utf8_general_ci;```
   saera_search -- имя вашей новой бд.
3. Короче в saera_web/searcheng/settings.py и saera_indexer/saera.cfg прописываем настройки бд, порт и хост без изменений, логин root, пароль тот что ставили на 1 шаге, и имя бд тоже оттуда. Сохраняем.
4. Внутри saera_web
   ```python manage.py migrate```
5. Теперь ищем в коде индексатора все обращения к dict-у settings или self.settings. Все ключи, по которым обращаются, должны быть как одна из строк в таблице searchres_settings. Есть пара ключей, которые я приведу:
   что-то там про b: 0.75
   что-то там про k1: 2
   что-то там про 1_boost: 1
   что-то там про 2_boost: 1000
   что-то типа max_width: 1000
   что-то типа max_depth: 1000
   Там еще есть время паузы, его либо 0.5, либо 1, где-то так.
6. Теперь в seara_web:
   python manage.py runserver
   открываем в браузере http://127.0.0.1:8000/ и там должен быть интерфейс поисковика
   Добавляем урл на индексацию какой нибудь.
7. В saera_indexer: Запускаем python indexer.py -f (-f для того, чтобы он не детачился как демон). Должна пойти индексация

# PS
Черканите на мыло o@0o.rs замечания Янковского по этой лабе, мне интересно, спасибо.
