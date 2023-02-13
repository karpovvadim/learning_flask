# Variable Rules (Правила для переменной части)

# Вы можете добавить переменные разделы в URL-адрес, пометив разделы <имя_переменной>.
# Затем ваша функция получает <имя_переменной> в качестве аргумента ключевого слова.
# При желании вы можете использовать преобразователь, чтобы указать тип аргумента,
# например <converter:variable_name>.

from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user (показать профиль пользователя
    # для этого пользователя)
    return f'User {escape(username)}'


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer (показать сообщение с
    # заданным идентификатором, идентификатор является целым числом)
    return f'Post {post_id}'


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/ (показать подпуть после /path/)
    return f'Subpath {escape(subpath)}'


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5005)

# Существуют следующие конвертеры:
# string    (по умолчанию) принимает любой текст без косой черты
# int 	    принимает положительные целые числа
# float 	принимает положительные значения с плавающей запятой
# path 	    как строка, но также принимает косые черты
# uuid      принимает строки UUID
