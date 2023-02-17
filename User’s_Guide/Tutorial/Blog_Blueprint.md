Blog Blueprint (План блога)

Вы будете использовать те же методы, которые вы узнали при написании схемы аутентификации,
чтобы написать схему блога. В блоге должны быть перечислены все сообщения, разрешено вошедшим
в систему пользователям создавать сообщения и разрешено автору сообщения редактировать или
удалять его.
При реализации каждого представления не выключайте сервер разработки. Когда вы сохраните
изменения, попробуйте перейти по URL-адресу в браузере и протестировать их.

The Blueprint (План)

Определите схему и зарегистрируйте ее в фабрике приложений.
flaskr/blog.py

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
bp = Blueprint('blog', __name__)

Импортируйте и зарегистрируйте чертеж с завода с помощью app.register_blueprint(). Поместите
новый код в конец заводской функции перед возвратом приложения.
flaskr/__init__.py

def create_app():
    app = ...
    # existing code omitted (существующий код опущен)
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    return app

В отличие от схемы авторизации, схема блога не имеет префикса url_prefix. Таким образом,
представление индекса будет находиться в /, представление создания — в /create и так далее.
Блог — это основная функция Flaskr, поэтому имеет смысл, что индекс блога будет основным
индексом.
Однако конечной точкой для представления индекса, определенного ниже, будет blog.index.
Некоторые из представлений аутентификации ссылались на конечную точку простого индекса.
app.add_url_rule() связывает имя конечной точки 'index' с URL-адресом /, так что
url_for('index') или url_for('blog.index') будут работать, создавая один и тот же URL-адрес
/ в любом случае.
В другом приложении вы можете указать план блога с префиксом url и определить отдельное
представление индекса в фабрике приложений, аналогичное представлению приветствия. Тогда
конечные точки и URL-адреса index и blog.index будут другими.

Index (Индекс)

В индексе будут отображаться все сообщения, начиная с самых последних. JOIN используется для
того, чтобы информация об авторе из пользовательской таблицы была доступна в результате.
flaskr/blog.py

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

flaskr/templates/blog/index.html

{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}Posts{% endblock %}</h1>
  {% if g.user %}
    <a class="action" href="{{ url_for('blog.create') }}">New</a>
  {% endif %}
{% endblock %}

{% block content %}
  {% for post in posts %}
    <article class="post">
      <header>
        <div>
          <h1>{{ post['title'] }}</h1>
          <div class="about">by {{ post['username'] }} on {{ post['created'].strftime('%Y-%m-%d') }}</div>
        </div>
        {% if g.user['id'] == post['author_id'] %}
          <a class="action" href="{{ url_for('blog.update', id=post['id']) }}">Edit</a>
        {% endif %}
      </header>
      <p class="body">{{ post['body'] }}</p>
    </article>
    {% if not loop.last %}
      <hr>
    {% endif %}
  {% endfor %}
{% endblock %}

Когда пользователь входит в систему, блок заголовка добавляет ссылку на представление
создания. Когда пользователь является автором сообщения, он увидит ссылку «Редактировать»
для просмотра обновления для этого сообщения. loop.last — это специальная переменная,
доступная внутри Jinja для циклов. Он используется для отображения строки после каждого
поста, кроме последнего, для их визуального разделения.

Create (Создавать)

Представление создания работает так же, как представление регистрации авторизации. Либо
отображается форма, либо публикуемые данные проверяются и запись добавляется в базу данных,
либо отображается ошибка.
Декоратор login_required, который вы написали ранее, используется в представлениях блога.
Пользователь должен войти в систему, чтобы посетить эти представления, в противном случае
они будут перенаправлены на страницу входа.
flaskr/blog.py

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')

flaskr/templates/blog/create.html

{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}New Post{% endblock %}</h1>
{% endblock %}

{% block content %}
  <form method="post">
    <label for="title">Title</label>
    <input name="title" id="title" value="{{ request.form['title'] }}" required>
    <label for="body">Body</label>
    <textarea name="body" id="body">{{ request.form['body'] }}</textarea>
    <input type="submit" value="Save">
  </form>
{% endblock %}

Update (Обновлять)

Как в представлении обновления, так и в представлении удаления необходимо будет получить
сообщение по идентификатору и проверить, соответствует ли автор авторизованному пользователю.
Чтобы избежать дублирования кода, вы можете написать функцию для получения публикации и
вызова ее из каждого представления.
flaskr/blog.py

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    return post

abort() вызывает специальное исключение, которое возвращает код состояния HTTP. Для
отображения ошибки требуется необязательное сообщение, в противном случае используется
сообщение по умолчанию. 404 означает «Не найдено», а 403 означает «Запрещено». (401 означает
«Неавторизовано», но вы перенаправляете на страницу входа вместо возврата этого статуса.)
Аргумент check_author определен так, чтобы функцию можно было использовать для получения
поста без проверки автора. Это было бы полезно, если бы вы написали представление для
отображения отдельного сообщения на странице, где пользователь не имеет значения, поскольку
он не изменяет сообщение.
flaskr/blog.py

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)

В отличие от представлений, которые вы написали до сих пор, функция обновления принимает
аргумент id. Это соответствует <int:id> в маршруте. Настоящий URL-адрес будет выглядеть как
/1/update. Flask захватит 1, убедится, что это целое число, и передаст его в качестве
аргумента id. Если вы не укажете int: и вместо этого сделаете <id>, это будет строка. Чтобы
сгенерировать URL-адрес страницы обновления, url_for() необходимо передать идентификатор,
чтобы он знал, что заполнять: url_for('blog.update', id=post['id']). Это также находится в
файле index.html выше.
Представления создания и обновления выглядят очень похоже. Основное отличие состоит в том,
что в представлении обновления используется объект публикации и запрос UPDATE вместо INSERT.
При грамотном рефакторинге вы могли бы использовать одно представление и шаблон для обоих
действий, но для учебника будет понятнее держать их отдельно.
flaskr/templates/blog/update.html

{% extends 'base.html' %}
{% block header %}
  <h1>{% block title %}Edit "{{ post['title'] }}"{% endblock %}</h1>
{% endblock %}
{% block content %}
  <form method="post">
    <label for="title">Title</label>
    <input name="title" id="title"
      value="{{ request.form['title'] or post['title'] }}" required>
    <label for="body">Body</label>
    <textarea name="body" id="body">{{ request.form['body'] or post['body'] }}</textarea>
    <input type="submit" value="Save">
  </form>
  <hr>
  <form action="{{ url_for('blog.delete', id=post['id']) }}" method="post">
    <input class="danger" type="submit" value="Delete" onclick="return confirm('Are you sure?');">
  </form>
{% endblock %}

Этот шаблон имеет две формы. Первый отправляет отредактированные данные на текущую страницу
(/<id>/update). Другая форма содержит только кнопку и указывает атрибут действия, который
вместо этого отправляет сообщение в представление удаления. Кнопка использует JavaScript для
отображения диалогового окна подтверждения перед отправкой.
Шаблон {{ request.form['title'] или post['title'] }} используется для выбора данных,
отображаемых в форме. Когда форма не была отправлена, появляются исходные данные сообщения,
но если были отправлены недопустимые данные формы, вы хотите отобразить их, чтобы
пользователь мог исправить ошибку, поэтому вместо этого используется request.form.
request — еще одна переменная, которая автоматически доступна в шаблонах.

Delete (Удалить)

Представление удаления не имеет собственного шаблона, кнопка удаления является частью
update.html и публикуется по URL-адресу /<id>/delete. Поскольку шаблона нет, он будет
обрабатывать только метод POST, а затем перенаправлять в представление индекса.
flaskr/blog.py

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

Поздравляем, вы закончили писать приложение! Потратьте некоторое время, чтобы попробовать 
все в браузере. Однако до завершения проекта еще многое предстоит сделать.

Продолжать Make the Project Installable (Сделайте проект устанавливаемым).