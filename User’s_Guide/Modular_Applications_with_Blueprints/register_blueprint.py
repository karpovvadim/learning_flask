# Registering Blueprints (Регистрация чертежей)

# Так как же зарегистрировать этот план? Так:

from flask import Flask
from My_First_Blueprint import *

app = Flask(__name__)
# app.register_blueprint(simple_page)
#
# # Если вы проверите правила, зарегистрированные в приложении, вы найдете следующее:
#
# print(app.url_map)
"""
Map([<Rule '/static/<filename>' (HEAD, GET, OPTIONS) -> static>,
 <Rule '/' (HEAD, GET, OPTIONS) -> simple_page.show>,
 <Rule '/<page>' (HEAD, GET, OPTIONS) -> simple_page.show>])
"""

# Первый URL '/static/<filename>', очевидно, из самого приложения для статических файлов.
# Два других предназначены для функции show() схемы simple_page. Как видите, они также имеют
# префикс с названием схемы и разделены точкой (.).
# Однако чертежи также моут быть установлены в разных местах:


app.register_blueprint(simple_page, url_prefix='/pages')

# Смотрим сгенерированные правила:

print(app.url_map)
"""
Map([<Rule '/static/<filename>' (OPTIONS, GET, HEAD) -> static>,
 <Rule '/pages/' (OPTIONS, GET, HEAD) -> simple_page.show>,
 <Rule '/pages/<page>' (OPTIONS, GET, HEAD) -> simple_page.show>])
"""
# Кроме того, вы можете регистрировать чертежи несколько раз, хотя не каждый чертеж может
# правильно реагировать на это. На самом деле это зависит от того, как реализован план, если
# его можно смонтировать более одного раза.
