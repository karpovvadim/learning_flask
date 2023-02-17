Static Files (Статические файлы)

Представления и шаблоны аутентификации работают, но сейчас они выглядят очень просто. Можно
добавить немного CSS, чтобы добавить стиль к созданному вами HTML-макету. Стиль не изменится,
поэтому это статический файл, а не шаблон.
Flask автоматически добавляет статическое представление, которое берет путь относительно
каталога flaskr/static и обслуживает его. В шаблоне base.html уже есть ссылка на файл
style.css:
{{ url_for('статический', имя_файла='style.css') }}

Помимо CSS, другие типы статических файлов могут быть файлами с функциями JavaScript или
изображением логотипа. Все они размещены в каталоге flaskr/static и ссылаются на них с помощью
url_for('static', filename='...').
Это руководство не посвящено тому, как писать CSS, поэтому вы можете просто скопировать
следующее в файл flaskr/static/style.css:
flaskr/static/style.css

html { font-family: sans-serif; background: #eee; padding: 1rem; }
body { max-width: 960px; margin: 0 auto; background: white; }
h1 { font-family: serif; color: #377ba8; margin: 1rem 0; }
a { color: #377ba8; }
hr { border: none; border-top: 1px solid lightgray; }
nav { background: lightgray; display: flex; align-items: center; padding: 0 0.5rem; }
nav h1 { flex: auto; margin: 0; }
nav h1 a { text-decoration: none; padding: 0.25rem 0.5rem; }
nav ul  { display: flex; list-style: none; margin: 0; padding: 0; }
nav ul li a, nav ul li span, header .action { display: block; padding: 0.5rem; }
.content { padding: 0 1rem 1rem; }
.content > header { border-bottom: 1px solid lightgray; display: flex; align-items: flex-end; }
.content > header h1 { flex: auto; margin: 1rem 0 0.25rem 0; }
.flash { margin: 1em 0; padding: 1em; background: #cae6f6; border: 1px solid #377ba8; }
.post > header { display: flex; align-items: flex-end; font-size: 0.85em; }
.post > header > div:first-of-type { flex: auto; }
.post > header h1 { font-size: 1.5em; margin-bottom: 0; }
.post .about { color: slategray; font-style: italic; }
.post .body { white-space: pre-line; }
.content:last-child { margin-bottom: 0; }
.content form { margin: 1em 0; display: flex; flex-direction: column; }
.content label { font-weight: bold; margin-bottom: 0.5em; }
.content input, .content textarea { margin-bottom: 1em; }
.content textarea { min-height: 12em; resize: vertical; }
input.danger { color: #cc2f2e; }
input[type=submit] { align-self: start; min-width: 10em; }

Вы можете найти менее компактную версию style.css в примере кода.
Перейдите по адресу http://127.0.0.1:5000/auth/login, и страница должна выглядеть, как на
скриншоте ниже.

Flaskr                                          Register Log In
Register
Username_______________________________________________________
_______________________________________________________________
Password_______________________________________________________
_______________________________________________________________
    Register

Continue to Blog Blueprint.