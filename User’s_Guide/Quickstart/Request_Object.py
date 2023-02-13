# The Request Object (Объект запроса)

# Объект запроса описан в разделе API, и мы не будем подробно описывать его здесь (см. Запрос).
# Вот общий обзор некоторых из наиболее распространенных операций. Прежде всего, вы должны
# импортировать его из модуля flask:
from flask import Flask, render_template
from flask import request

# Текущий метод запроса доступен с помощью атрибута метода. Для доступа к данным формы (данным,
# передаваемым в запросе POST или PUT) вы можете использовать атрибут формы. Вот полный
# пример двух атрибутов, упомянутых выше:
app = Flask(__name__)


def valid_login(param, param1):
    pass


def log_the_user_in(param):
    pass


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
# the code below is executed if the request method was GET or the credentials were invalid
# приведенный ниже код выполняется, если метод запроса был GET или учетные данные недействительны.
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5005)

# Что произойдет, если ключ не существует в атрибуте формы? В этом случае возникает
# специальный KeyError. Вы можете перехватить его как стандартную ошибку KeyError, но если
# вы этого не сделаете, вместо этого будет показана страница ошибки HTTP 400 Bad Request.
# Поэтому во многих ситуациях вам не нужно решать эту проблему.
#
# Чтобы получить доступ к параметрам, представленным в URL-адресе (?key=value), вы можете
# использовать атрибут args:
searchword = request.args.get('key', '')

# Мы рекомендуем получать доступ к параметрам URL-адреса с помощью get или путем перехвата
# KeyError, потому что пользователи могут изменить URL-адрес и представить им страницу с
# неверным запросом 400 в этом случае, неудобную для пользователя.
# Полный список методов и атрибутов объекта запроса см. в документации по запросу.
