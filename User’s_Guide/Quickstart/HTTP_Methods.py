# HTTP Methods (HTTP-методы)

# Веб-приложения используют различные методы HTTP при доступе к URL-адресам. Вы должны
# ознакомиться с методами HTTP при работе с Flask. По умолчанию маршрут отвечает только
# на запросы GET. Вы можете использовать аргумент методов декоратора route() для обработки
# различных методов HTTP.

from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return "do_the_login()"
    else:
        return "show_the_login_form()"


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5005)

# В приведенном выше примере все методы маршрута хранятся в одной функции, что может
# быть полезно, если каждая часть использует некоторые общие данные.

# Вы также можете разделить представления для разных методов на разные функции.
# Flask предоставляет ярлык для украшения таких маршрутов с помощью get(), post()
# и т. д. для каждого распространенного метода HTTP.
"""
@app.get('/login')
def login_get():
    return show_the_login_form()  показать форму входа (показать логин)

@app.post('/login')
def login_post():
    return do_the_login()  авторизоваться
"""
# Если присутствует GET, Flask автоматически добавляет поддержку метода HEAD и
# обрабатывает запросы HEAD в соответствии с HTTP RFC. Точно так же OPTIONS
# автоматически внедряются для вас.
