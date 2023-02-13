# Cookies (Печенье)
#
# Для доступа к файлам cookie вы можете использовать атрибут cookie. Чтобы установить файлы
# cookie, вы можете использовать метод set_cookie объектов ответа. Атрибут cookie объектов
# запроса представляет собой словарь со всеми cookie-файлами, которые передает клиент. Если вы
# хотите использовать сеансы, не используйте файлы cookie напрямую, а вместо этого используйте
# сеансы во Flask, которые добавляют вам некоторую безопасность поверх файлов cookie.
# Reading cookies:
from flask import Flask
from flask import request, render_template, make_response

app = Flask(__name__)


@app.route('/')
def index():
    username = request.cookies.get('username')
    # use cookies.get(key) instead of cookies[key] to not get a
    # KeyError if the cookie is missing.
    # используйте cookies.get(key) вместо cookies[key], чтобы не получить KeyError,
    # если файл cookie отсутствует.


# Storing cookies (Хранение файлов cookie):

@app.route('/')
def index1():
    resp = make_response(render_template(...))
    resp.set_cookie('username', 'the username')
    return resp


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5005)

# Обратите внимание, что файлы cookie устанавливаются для объектов ответа. Поскольку обычно
# вы просто возвращаете строки из функций представления, Flask преобразует их в объекты
# ответа для вас. Если вы явно хотите сделать это, вы можете использовать функцию
# make_response(), а затем изменить ее.

# Иногда вам может понадобиться установить cookie в точке, где объект ответа еще не существует.
# Это возможно благодаря использованию шаблона Deferred Request Callbacks
# (обратных вызовов отложенных запросов).
# Для этого также см. About Responses (Об ответах).
