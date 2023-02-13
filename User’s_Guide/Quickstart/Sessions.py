# Sessions (Сессии)

# В дополнение к объекту запроса существует также второй объект, называемый сеансом, который
# позволяет вам хранить информацию, относящуюся к пользователю, от одного запроса к другому.
# Это реализовано для вас поверх файлов cookie и криптографически подписывает файлы cookie.
# Это означает, что пользователь может просматривать содержимое вашего файла cookie, но не
# изменять его, если только он не знает секретный ключ, используемый для подписи.

# Чтобы использовать сеансы, вы должны установить секретный ключ. Вот как работают сеансы:


from flask import Flask, session, url_for, request, redirect

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'    # вы не авторизованы


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    # удалить имя пользователя из сеанса, если оно есть
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5005)


# Как генерировать хорошие секретные ключи

# Секретный ключ должен быть как можно более случайным. В вашей операционной системе есть
# способы генерировать довольно случайные данные на основе криптографического генератора
# случайных чисел. Используйте следующую команду, чтобы быстро сгенерировать значение для
# Flask.secret_key (или SECRET_KEY):
"""
$ python -c 'импортировать секреты; печать (secrets.token_hex())'
'192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
"""
# Примечание о сеансах на основе файлов cookie: Flask примет значения, которые вы поместили в
# объект сеанса, и сериализует их в файл cookie. Если вы обнаружите, что некоторые значения
# не сохраняются между запросами, файлы cookie действительно включены, и вы не получаете
# четкого сообщения об ошибке, сравните размер файла cookie в ответах на странице с размером,
# поддерживаемым веб-браузерами.

# Помимо сеансов на стороне клиента по умолчанию, если вы хотите вместо этого обрабатывать
# сеансы на стороне сервера, есть несколько расширений Flask, которые поддерживают это.
