Данное приложение осуществляет настраиваемуюю генерацию математических заданий. Пока что имеются обычные арифметические примеры и уравнения, в будущем планируется расширить функционал путём добавления неравенств и задач. Приложение использует следующие технологии:
1. ЯП python 3.12
2. Вебфреймворк flask и некоторые плагины для него
3. ORM sqlalchemy
4. База данных sqlite

Вы можете посмотреть демонстрацию функционала в файле демонстрация-функционала.mp4, лежащем в корне проекта.

Для того, чтобы собрать и запустить приложение, Вам необходимо сделать следующее:
1. Скачайте и установите python версии 3.12 (https://www.python.org/downloads/release/python-3124/) (обязательно при установке нажмите на галочку "add Python to PATH", без этого будет сложнее работать)
2. Скачайте этот репозиторий. Для этого на главной странице нажмите на зелёную кнопку Code и выберите пункт "Download ZIP". Скачайте и распакуйте в любое удобное для Вас место.
3. Откройте командную строку и пропишите следующую команду: "pip install -r <путь до файла requirements.txt из этого проекта, который Вы предваритель скачали>". Это установит все зависимости.
4. Открой командную строку и пропишите "py <путь до файла app.py из этого проекта>". Это запустит приложение.
5. Откройте в браузере страницу 127.0.0.1:5000, это переместит вас на главную страницу приложения
