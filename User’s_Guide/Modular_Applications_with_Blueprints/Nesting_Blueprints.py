# Nesting Blueprints (Вложение чертежей).

# Возможна регистрация чертежа на другом чертеже.

from flask import Flask, Blueprint, url_for

app = Flask(__name__)

parent = Blueprint('parent', __name__, url_prefix='/parent')
child = Blueprint('child', __name__, url_prefix='/child')

parent.register_blueprint(child)
app.register_blueprint(parent)

# Дочерний план получит имя родителя в качестве префикса к своему имени, а дочерние
# URL-адреса будут иметь префикс родительского URL-адреса.
"""
url_for('parent.child.create')
# /parent/child/create
"""
# Специфичные для blueprint функции перед запросом и т. д., зарегистрированные у родителя,
# будут запускаться для дочернего элемента. Если у дочернего элемента нет обработчика ошибок,
# способного обработать данное исключение, то будет произведена попытка запуска обработчика
# ошибок родителя.
