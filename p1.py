#-*-coding:utf8-*-
from flask import Flask
from flask import render_template
from flask import request
import os
import sys
from subprocess import call
import subprocess
import time
import app_preset

# call(["ls", "-l"])
#http://stackoverflow.com/questions/8382847/how-to-ssh-connect-through-python-paramiko-with-public-key

app = Flask(__name__)

app.static_folder = 'static' # подключаем bootstrap
CURR_PATH = sys.argv[0].replace(sys.argv[0].split('/')[-1],'')[:-1] # уточняем путь к директории модуля

@app.route('/bootapp/', methods=['GET', 'POST'])
@app.route('/bootapp/<name>', methods=['GET', 'POST'])
def bootstrap_app_me(name='Anonimous'):
    if request.method == 'GET':
        return render_template('bootstrap_hello.html', name=name)
    elif request.method == 'POST':
        # достаём из запроса
        r_duration, r_platform, r_vast_url, r_xml_name, r_order, r_slot = \
            request.form['duration'], request.form['platform'], request.form['vast_url'], request.form['xml_name'].replace('.xml',''), str(app_preset.order[request.form['slot']]), str(request.form['slot'])
         # удаляем все прошлые выходные файлы
        map(lambda i: os.remove('{}/output/{}'.format(CURR_PATH, i) ), os.listdir('{}/output'.format(CURR_PATH) ))
        # генерируем ссылки на созданные РМ
        test_placement_link,  test_order_link = \
                    app_preset.test_placement_link.replace('{{ xml_name }}',r_xml_name), \
                    app_preset.test_order_link.replace('{{ test_order }}',r_order)
        # если нужно создавать XML - создаём файлик и пуляем его на сервер
        if app_preset.template[ r_platform ]:
            create_xml(r_xml_name, r_duration, r_vast_url, app_preset.template[ r_platform ] )
            # os.system("bash {}/output/push_to_ftp.sh".format(CURR_PATH))
        return render_template('bootstrap_hello.html',  # Отрисовка шаблона
                                vast_url = r_vast_url, 
                                platform = r_platform, 
                                duration = r_duration,
                                test_order =  test_order_link,
                                test_placement =  test_placement_link,
                                name_draft = "mraid",
                                slot = r_slot  )

def create_xml(r_xml_name, r_duration, r_vast_url, template_name):
    '''
        Генерируем и размещаем XML
    '''
    with open('{}/templates/{}.xml'.format(CURR_PATH,template_name), 'r') as f:
        xml_template = f.read().replace('{{ adv_dur }}', r_duration).replace('{{ adv_url }}', r_vast_url)
        with open('{}/output/{}.xml'.format(CURR_PATH,r_xml_name), 'w') as of:
            of.write(xml_template)
    create_copyscript(r_xml_name) # создаём скрипт копирования файлов


def create_copyscript(r_xml_name):
    with open('{}/templates/push_to_ftp.sh'.format(CURR_PATH), 'r') as t:
        push_template = t.read().replace('{{ file_name }}', r_xml_name+'.xml')
        with open('{}/output/push_to_ftp.sh'.format(CURR_PATH), 'w') as of:
            of.write(push_template)

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
