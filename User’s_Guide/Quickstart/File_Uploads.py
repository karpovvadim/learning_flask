# File Uploads (Загрузка файлов)

# Вы можете легко обрабатывать загруженные файлы с помощью Flask. Только не забудьте
# установить атрибут enctype="multipart/form-data" в HTML-форме, иначе браузер вообще
# не будет передавать ваши файлы.

# Загруженные файлы хранятся в памяти или во временном месте файловой системы. Вы можете
# получить доступ к этим файлам, просмотрев атрибут файлов в объекте запроса. Каждый
# загруженный файл хранится в этом словаре. Он ведет себя так же, как стандартный файловый
# объект Python, но также имеет метод save(), позволяющий сохранить этот файл в файловой
# системе сервера. Вот простой пример, показывающий, как это работает:

from flask import Flask, request


app = Flask(__name__)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')
        return f
    else:
        return "/var/www/uploads/uploaded_file.txt"


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5005)

# Если вы хотите узнать, как файл был назван на клиенте до того, как он был загружен в ваше
# приложение, вы можете получить доступ к атрибуту имени файла. Однако имейте в виду, что это
# значение может быть подделано, поэтому никогда не доверяйте этому значению. Если вы хотите
# использовать имя файла клиента для хранения файла на сервере, передайте его через функцию
# secure_filename(), которую Werkzeug предоставляет вам:
""""
from werkzeug.utils import secure_filename

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['the_file']
        file.save(f"/var/www/uploads/{secure_filename(file.filename)}")
    ...
"""
# Некоторые лучшие примеры см. в разделе Uploading Files (Загрузка файлов).
