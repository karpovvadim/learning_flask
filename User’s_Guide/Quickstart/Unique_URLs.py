# Unique URLs / Redirection Behavior (Уникальные URL-адреса/поведение при перенаправлении)

# Следующие два правила отличаются использованием косой черты в конце.

from flask import Flask

app = Flask(__name__)


@app.route('/projects/')
def projects():
    return 'The project page'


@app.route('/about')
def about():
    return 'The about page'


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5005)

# Канонический URL-адрес конечной точки проекта имеет косую черту в конце. Это похоже
# на папку в файловой системе. Если вы обращаетесь к URL-адресу без завершающей
# косой черты (/projects), Flask перенаправляет вас на канонический URL-адрес с
# завершающей косой чертой (/projects/).

# Канонический URL-адрес конечной точки about не имеет завершающей косой черты. Это
# похоже на путь к файлу. При доступе к URL-адресу с завершающей косой чертой (/about/)
# возникает ошибка 404 «Не найдено». Это помогает сохранить уникальные URL-адреса для
# этих ресурсов, что помогает поисковым системам избежать повторного индексирования
# одной и той же страницы.
