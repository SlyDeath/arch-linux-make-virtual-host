#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'SlyDeath'


# Добавить строку в httpd.conf
# IncludeOptional conf/extra/vhosts/*.conf

import os
import sys

if not os.geteuid() == 0:
    sys.exit('Необходимы права суперпользователя! (Можно ввести "sudo !!" для запуска предыдущей команды от рута)')

print('Введите полный путь к папке сайта, например /home/user/projects/mysite')
print('Если таковой папки нет, скрипт попробует её создать')
DocumentRoot = input('DocumentRoot: ')

if os.path.exists(DocumentRoot) and os.path.isdir(DocumentRoot):
    print('Папка существует, всё окей')
else:
    try:
        print('Пробуем создать папку ' + DocumentRoot)
        os.makedirs(DocumentRoot)
    except OSError:
        raise

VhostsDir = '/etc/httpd/conf/extra/vhosts'

if os.path.exists(VhostsDir) and os.path.isdir(VhostsDir):
    print('Папка с виртуальными хостами существует, всё окей')
else:
    try:
        print('Пробуем создать папку для виртуальных хостов ' + VhostsDir)
        os.makedirs(VhostsDir)
    except OSError:
        raise

print('Введите адрес по которому будет доступен сайт, например mysite.loc')
ServerName = input('ServerName: ')

print('Введите почтовый адрес администратора, например admin@mysite.loc')
ServerAdmin = input('ServerAdmin: ')

defaultConfig = '''
<VirtualHost ''' + ServerName + ''':80>
    ServerAdmin ''' + ServerAdmin + '''
    DocumentRoot "''' + DocumentRoot + '''"
    ServerName ''' + ServerName + '''
    ServerAlias ''' + ServerName + '''

    <Directory "''' + DocumentRoot + '''">
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>'''

ConfFile = VhostsDir + '/' + ServerName + '.conf'

with open(ConfFile, 'w+') as configFile:
    if os.path.exists(VhostsDir) and os.path.isfile(ConfFile):
        configFile.write(defaultConfig)
        print('Виртуальный хост сохранён')
    else:
        print('Файл ' + ConfFile + ' не создан')

print('Делаю бэкап файла /etc/hosts в /etc/hosts.backup')
os.system('cp /etc/hosts /etc/hosts.backup')

with open('/etc/hosts', 'a') as hostsFile:
    if os.path.exists('/etc/hosts') and os.path.isfile('/etc/hosts'):
        hostsFile.write('127.0.0.1        ' + ServerName + '\n')
    else:
        print('Файл /etc/hosts не существует')

print('Перезапускаем Апач')
os.system('systemctl restart httpd')

print('Всё готово!!! :) Ваш виртуальный сайт доступен по адресу http://' + ServerName)
