Test Coverage (Тестовое покрытие)

Написание модульных тестов для вашего приложения позволяет вам убедиться, что написанный вами
код работает так, как вы ожидаете. Flask предоставляет тестовый клиент, который имитирует
запросы к приложению и возвращает данные ответа.
Вы должны протестировать как можно больше своего кода. Код в функциях запускается только при
вызове функции, а код в ветвях, таких как блоки if, запускается только при выполнении условия.
Вы хотите убедиться, что каждая функция тестируется с данными, которые охватывают каждую ветвь.
Чем ближе вы подходите к 100% охвату, тем комфортнее вы можете быть уверены, что внесение
изменений не приведет к неожиданному изменению другого поведения. Однако 100% охват не
гарантирует отсутствие ошибок в вашем приложении. В частности, он не проверяет, как
пользователь взаимодействует с приложением в браузере. Несмотря на это, тестовое покрытие 
является важным инструментом, который можно использовать во время разработки.
    Примечание
Это будет представлено в конце учебника, но в ваших будущих проектах вы должны тестировать их
по мере разработки.
Вы будете использовать pytest и coverage (покрытие) для тестирования и измерения кода.
Установите их оба:
                        $ pip install pytest coverage

Setup and Fixtures (Настройка и приспособления)

Код теста находится в папке с тестами. Этот каталог находится рядом с пакетом flaskr, а не
внутри него. Файл test/conftest.py содержит функции настройки, называемые фикстурами, которые
будут использоваться каждым тестом. Тесты находятся в модулях Python, которые начинаются с
test_, и каждая тестовая функция в этих модулях также начинается с test_.
Каждый тест будет создавать новый временный файл базы данных и заполнять некоторые данные,
которые будут использоваться в тестах. Напишите файл SQL для вставки этих данных.

tests/data.sql

INSERT INTO user (username, password)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO post (title, body, author_id, created)
VALUES
  ('test title', 'test' || x'0a' || 'body', 1, '2018-01-01 00:00:00');

Фикстура приложения вызовет фабрику и передаст test_config, чтобы настроить приложение и базу
данных для тестирования вместо использования вашей локальной конфигурации разработки.
tests/conftest.py

import os
import tempfile
import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)
    yield app
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

tempfile.mkstemp() создает и открывает временный файл, возвращая дескриптор файла и путь к 
нему. Путь DATABASE переопределяется, поэтому он указывает на этот временный путь, а не на 
папку экземпляра. После установки пути создаются таблицы базы данных и вставляются тестовые
данные. После завершения теста временный файл закрывается и удаляется.

TESTING сообщает Flask, что приложение находится в тестовом режиме. Flask изменяет некоторое 
внутреннее поведение, чтобы его было легче тестировать, и другие расширения также могут 
использовать этот флаг, чтобы упростить их тестирование.

Фикстура клиента вызывает app.test_client() с объектом приложения, созданным фикстурой 
приложения. Тесты будут использовать клиент для выполнения запросов к приложению без запуска
сервера.
Крепление бегунка аналогично клиенту. app.test_cli_runner() создает бегун, который может
вызывать команды Click, зарегистрированные в приложении.

Pytest использует фикстуры, сопоставляя имена их функций с именами аргументов в тестовых
функциях. Например, функция test_hello, которую вы напишете дальше, принимает аргумент клиента.
Pytest сопоставляет это с функцией фиксации клиента, вызывает ее и передает возвращаемое
значение тестовой функции.

Factory (Фабрика)

На самой фабрике особо нечего тестировать. Большая часть кода будет выполняться уже для 
каждого теста поэтому если что-то пойдет не так, это заметят другие тесты.

Единственное поведение, которое может измениться, — это прохождение тестовой конфигурации.
Если конфигурация не передана, должна быть какая-то конфигурация по умолчанию, в противном 
случае конфигурация должна быть переопределена.
tests/test_factory.py

from flaskr import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'

Вы добавили маршрут hello в качестве примера при написании фабрики в начале руководства.
Он возвращает «Hello, World!», поэтому тест проверяет совпадение данных ответа.

Database (База данных)

В контексте приложения get_db должен возвращать одно и то же соединение при каждом вызове. 
После контекста соединение должно быть закрыто.
tests/test_db.py

import sqlite3
import pytest
from flaskr.db import get_db

def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')
    assert 'closed' in str(e.value)

Команда init-db должна вызывать функцию init_db и выводить сообщение.
tests/test_db.py

def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False
    def fake_init_db():
        Recorder.called = True
    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called

Этот тест использует фикстуру Monkeypatch от Pytest, чтобы заменить функцию init_db на ту,
которая записывает, что она была вызвана. Приспособление бегуна, которое вы написали выше,
используется для вызова команды init-db по имени.

Authentication (Аутентификация)

Для большинства представлений пользователь должен войти в систему. Самый простой способ 
сделать это в тестах — сделать POST-запрос к представлению входа в систему с клиентом.
Вместо того чтобы писать это каждый раз, вы можете написать класс с методами для этого и 
использовать фикстуру для передачи его клиенту для каждого теста.
tests/conftest.py

class AuthActions(object):
    def __init__(self, client):
        self._client = client
    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )
    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)

С фикстурой auth вы можете вызвать auth.login() в тесте, чтобы войти в систему как тестовый
пользователь, который был вставлен как часть тестовых данных в фикстуру приложения.
Представление регистра должно успешно отображаться при GET. При POST с действительными 
данными формы он должен перенаправлять на URL-адрес входа, а данные пользователя должны быть
в базе данных. Неверные данные должны отображать сообщения об ошибках.
tests/test_auth.py

import pytest
from flask import g, session
from flaskr.db import get_db

def test_register(client, app):
    assert client.get('/auth/register').status_code == 200   (утверждать)
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert response.headers["Location"] == "/auth/login"
    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data

client.get() делает запрос GET и возвращает объект Response, возвращенный Flask. Точно так же
client.post() делает запрос POST, преобразуя данные dict в данные формы.
Чтобы проверить, что страница отображается успешно, делается простой запрос и проверяется код
состояния 200 OK. В случае сбоя рендеринга Flask вернет код 500 Internal Server Error.

headers (заголовки) будут иметь заголовок Location с URL-адресом входа, когда представление
регистрации перенаправляется на представление входа.

data содержит тело ответа в виде байтов. Если вы ожидаете, что определенное значение будет 
отображаться на странице, убедитесь, что оно находится в данных. Байты должны сравниваться 
с байтами. Если вы хотите сравнить текст, используйте get_data(as_text=True).

pytest.mark.parametrize указывает Pytest запустить одну и ту же тестовую функцию с разными
аргументами. Вы используете его здесь для проверки различных неверных входных данных и 
сообщений об ошибках без написания одного и того же кода три раза.
Тесты для login (входа) в систему очень похожи на тесты для register (регистрации). Вместо
того чтобы тестировать данные в базе данных, session (сеанс) должен иметь установленный
user_id после входа в систему.
tests/test_auth.py

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"
    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

Использование client в блоке with позволяет получить доступ к переменным контекста, таким как
session (сеанс), после возврата ответа. Обычно доступ к сеансу вне запроса вызывает ошибку.

Тестирование logout (выхода) из системы противоположно login (входу) в систему. session
не должен содержать user_id после выхода из системы.
tests/test_auth.py

def test_logout(client, auth):
    auth.login()
    with client:
        auth.logout()
        assert 'user_id' not in session

Blog (Блог)

Все представления блога используют auth fixture (авторизацию), которую вы написали ранее.
Вызов auth.login() и последующие запросы от клиента будут зарегистрированы как тестовый 
пользователь.
В представлении индекса должна отображаться информация о публикации, которая была добавлена
с тестовыми данными. При входе в качестве автора должна быть ссылка на редактирование поста.
Вы также можете протестировать некоторые другие способы проверки подлинности при тестировании
представления index (индекса). Если вы не вошли в систему, на каждой странице отображаются
ссылки для входа или регистрации. При входе есть ссылка для выхода.
tests/test_blog.py

import pytest
from flaskr.db import get_db

def test_index(client, auth):
    response = client.get('/')
    assert b"Log In" in response.data
    assert b"Register" in response.data
    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2018-01-01' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data

Пользователь должен войти в систему, чтобы получить доступ к create, update, and delete
(созданию, обновлению и удалению) представлений. Вошедший в систему пользователь должен быть
автором сообщения, чтобы получить доступ к update and delete (обновлению и удалению), в
противном случае возвращается статус 403 Forbidden. Если post (сообщение) с данным 
идентификатором не существует, обновление и удаление должны вернуть 404 Not Found.
tests/test_blog.py

@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"

def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()
    auth.login()
    # current user can't modify other user's post
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get('/').data

@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404

Представления создания и обновления должны отображать и возвращать статус 200 OK для запроса
GET. Когда действительные данные отправляются в запросе POST, create должен вставить новые
данные сообщения в базу данных, а update должен изменить существующие данные. На обеих
страницах должно отображаться сообщение об ошибке при недопустимых данных.
tests/test_blog.py

def test_create(client, auth, app):
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'title': 'created', 'body': ''})
    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM post').fetchone()[0]
        assert count == 2

def test_update(client, auth, app):
    auth.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'title': 'updated', 'body': ''})
    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post['title'] == 'updated'

@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data

Представление delete (удаления) должно перенаправлять на URL-адрес индекса, а сообщение
больше не должно существовать в базе данных.
tests/test_blog.py¶

def test_delete(client, auth, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers["Location"] == "/"
    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post is None

Running the Tests (Запуск тестов)

Некоторая дополнительная конфигурация, которая не требуется, но делает выполнение тестов с
менее подробным покрытием, может быть добавлена в файл проекта setup.cfg.
setup.cfg

[tool:pytest]
testpaths = tests

[coverage:run]
branch = True
source =
    flaskr

