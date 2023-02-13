# APIs with JSON (API с JSON)

# Обычный формат ответа при написании API — JSON. С помощью Flask легко начать писать такой
# API. Если вы вернете словарь или список из представления, он будет преобразован в ответ JSON.
from flask import Flask, url_for

app = Flask(__name__)


def get_current_user():
    pass


@app.route("/me")
def me_api(user=None):
    get_current_user()
    return {
        "username": user.username,
        "theme": user.theme,
        "image": url_for("user_image", filename=user.image),
    }


def get_all_users():
    pass


@app.route("/users")
def users_api(users=None):
    get_all_users()
    return [user.to_json() for user in users]

# Это ярлык для передачи данных в функцию jsonify(), которая сериализует любой поддерживаемый
# тип данных JSON. Это означает, что все данные в словаре или списке должны быть
# сериализуемыми в формате JSON.

# Для сложных типов, таких как модели базы данных, вам нужно будет использовать библиотеку
# сериализации, чтобы сначала преобразовать данные в допустимые типы JSON. Существует
# множество библиотек сериализации и расширений API Flask, поддерживаемых сообществом,
# которые поддерживают более сложные приложения.
