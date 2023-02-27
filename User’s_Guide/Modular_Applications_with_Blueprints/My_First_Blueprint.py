# My First Blueprint

# Вот как выглядит очень простой план. В этом случае мы хотим реализовать план, который
# выполняет простой рендеринг статических шаблонов:

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

simple_page = Blueprint('simple_page', __name__, template_folder='templates')

# теперь в этой схеме, вместо экземпляра приложения 'app' используем экземпляр `Blueprint`
# с именем `simple_page`. Связываем URL со схемой `simple_page`


@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show(page):
    try:
        return render_template(f'pages/{page}.html')
    except TemplateNotFound:
        abort(404)

# Когда функция show() привязывается с помощью декоратора @simple_page.route(), то Blueprint
# регистрирует ее как представление в приложении. Кроме того, перед маршрутом, переданным
# в @simple_page.route() будет стоять префикс с именем, который был передан конструктору
# Blueprint (в данном случае это simple_page). Таким образом, фактически страницы в примере
# будут работать по маршрутам /simple_page/index и /simple_page/<page>. В общем, название
# схемы blueprint не изменяет весь URL, а изменяет только конечную точку маршрута.
