Blueprints and Views (Чертежи (схемы) и представления)

Функция просмотра — это код, который вы пишете для ответа на запросы к вашему приложению.
Flask использует шаблоны для сопоставления URL-адреса входящего запроса с представлением,
которое должно его обрабатывать. Представление возвращает данные, которые Flask превращает
в исходящий ответ. Flask также может пойти в другом направлении и сгенерировать URL-адрес
представления на основе его имени и аргументов.

Create a Blueprint (Создать план)

Blueprint — это способ организации группы связанных представлений и другого кода. Вместо того
чтобы регистрировать представления и другой код непосредственно в приложении, они
регистрируются с помощью Blueprint (схемы). Затем схема регистрируется в приложении, когда
она доступна в фабричной функции.

Flaskr будет иметь две схемы: одну для функций аутентификации и одну для функций сообщений в
блогах. Код для каждого чертежа будет находиться в отдельном модуле. Поскольку блог должен
знать об аутентификации, вы сначала напишете аутентификацию.
flaskr/auth.py

import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

Это создает Blueprint с именем «auth» (авторизация). Как и объект приложения, схема должна
знать, где она определена, поэтому __name__ передается в качестве второго аргумента. Префикс
url_prefix будет добавляться ко всем URL-адресам, связанным с планом.

Импортируйте и зарегистрируйте чертеж с завода с помощью app.register_blueprint(). Поместите
новый код в конец заводской функции перед возвратом приложения.
flaskr/__init__.py

def create_app():
    app = ...
    # existing code omitted
    from . import auth
    app.register_blueprint(auth.bp)
    return app

План аутентификации будет иметь представления для регистрации новых пользователей,
а также для входа и выхода из системы.

The First View: Register (Первый просмотр: зарегистрироваться)

Когда пользователь посещает URL-адрес /auth/register, представление регистрации возвращает
HTML с формой для заполнения. Когда они отправят форму, она проверит их ввод и либо снова 
покажет форму с сообщением об ошибке, либо создаст нового пользователя и перейдет на 
страницу входа.

Сейчас вы просто напишете код представления. На следующей странице вы напишете шаблоны для
создания HTML-формы.
flaskr/auth.py

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template('auth/register.html')

Вот что делает функция просмотра регистра:
     1. @bp.route связывает URL-адрес /register с функцией просмотра реестра. Когда Flask
получает запрос к /auth/register, он вызывает представление регистра и использует
возвращаемое значение в качестве ответа.
     2. Если пользователь отправил форму, request.method будет «POST». В этом случае начните
проверку ввода.
     3. request.form — это специальный тип сопоставления dict представленных ключей и 
значений формы. Пользователь вводит свое имя пользователя и пароль.
     4. Убедитесь, что имя пользователя и пароль не пусты.
     5. Если проверка прошла успешно, вставьте новые пользовательские данные в базу данных.
         * db.execute принимает SQL-запрос с ? заполнители для любого пользовательского ввода
        и кортеж значений для замены заполнителей. Библиотека базы данных позаботится об
        экранировании значений, чтобы вы не были уязвимы для атаки с внедрением SQL.
         * В целях безопасности пароли никогда не должны храниться непосредственно в базе
        данных. Вместо этого для безопасного хеширования пароля используется
        generate_password_hash(), и этот хэш сохраняется. Поскольку этот запрос изменяет
        данные, после этого необходимо вызвать db.commit(), чтобы сохранить изменения.
         * sqlite3.IntegrityError произойдет, если имя пользователя уже существует, что
        должно быть показано пользователю как еще одна ошибка проверки.
     6. После сохранения пользователя они перенаправляются на страницу входа. url_for()
генерирует URL-адрес для входа в систему на основе его имени. Это предпочтительнее, чем 
писать URL-адрес напрямую, поскольку позволяет изменить URL-адрес позже, не изменяя весь код,
который ссылается на него. redirect() генерирует ответ перенаправления на сгенерированный URL.
     7. Если проверка не пройдена, пользователю показывается ошибка. flash() хранит сообщения,
которые можно получить при рендеринге шаблона.
     8. Когда пользователь впервые переходит к авторизации/регистрации или произошла ошибка
проверки, должна отображаться HTML-страница с регистрационной формой. render_template()
отобразит шаблон, содержащий HTML, который вы напишете на следующем этапе руководства.

Login (Авторизоваться)

Это представление следует той же схеме, что и представление регистра выше.
flaskr/auth.py

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')

Есть несколько отличий от представления реестра:
     1. Пользователь опрашивается первым и сохраняется в переменной для последующего 
использования.
     fetchone() возвращает одну строку из запроса. Если запрос не дал результатов, он
возвращает None. Позже будет использоваться fetchall(), которая возвращает список всех 
результатов.
     2. check_password_hash() хеширует отправленный пароль так же, как сохраненный хеш,
и безопасно сравнивает их. Если они совпадают, пароль действителен.
     3. session — это dict, в котором хранятся данные по запросам. Когда проверка проходит
успешно, идентификатор пользователя сохраняется в новом сеансе. Данные хранятся в файле
cookie, который отправляется в браузер, а затем браузер отправляет их обратно с последующими
запросами. Flask надежно подписывает данные, чтобы их нельзя было подделать.

Теперь, когда идентификатор пользователя хранится в сеансе, он будет доступен при
последующих запросах. В начале каждого запроса, если пользователь вошел в систему, его
информация должна быть загружена и доступна для других представлений.
flaskr/auth.py

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.before_app_request() регистрирует функцию, которая запускается перед функцией просмотра,
независимо от того, какой URL запрашивается. load_logged_in_user проверяет, сохранен ли
идентификатор пользователя в сеансе, и получает данные этого пользователя из базы данных,
сохраняя их в g.user, который длится на протяжении всего запроса. Если идентификатор
пользователя отсутствует или если идентификатор не существует, g.user будет None.

Logout (Выйти)

Чтобы выйти из системы, вам нужно удалить идентификатор пользователя из сеанса. Тогда
load_logged_in_user не будет загружать пользователя при последующих запросах.
flaskr/auth.py

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

Require Authentication in Other Views (Требовать аутентификацию в других представлениях)

Создание, редактирование и удаление сообщений в блоге потребует от пользователя входа в
систему. Можно использовать декоратор, чтобы проверить это для каждого представления, к
которому он применяется.

flaskr/auth.py

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

Этот декоратор возвращает новую функцию представления, обертывающую исходное представление,
к которому оно было применено. Новая функция проверяет, загружен ли пользователь, и в 
противном случае перенаправляет на страницу входа. Если пользователь загружен, исходное
представление вызывается и продолжается нормально. Вы будете использовать этот декоратор при
написании просмотров блога.

Endpoints and URLs (Конечные точки и URL-адреса)

Функция url_for() генерирует URL-адрес представления на основе имени и аргументов. Имя,
связанное с представлением, также называется конечной точкой, и по умолчанию оно совпадает с
именем функции представления.
Например, представление hello(), которое было добавлено в фабрику приложений ранее в этом
руководстве, имеет имя hello и может быть связано с url_for('hello'). Если бы он принимал
аргумент, как вы увидите позже, он был бы связан с использованием
url_for('hello', who='World').
При использовании схемы имя схемы добавляется к имени функции, поэтому конечной точкой для
функции входа в систему, которую вы написали выше, является «auth.login», поскольку вы
добавили ее в схему «auth».

Continue to Templates.