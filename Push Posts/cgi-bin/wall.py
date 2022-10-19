#!/usr/bin/env python3

import cgi

from util import Util

form = cgi.FieldStorage()
action = form.getfirst("action")

login = form.getfirst("login")
password = form.getfirst("password")

posts = form.getfirst("posts")

util = Util()

online = util.get_data(util.ONLINE)
user = online[0] if len(online) else None

error = False
message = ''

if action == "login":
    if util.login(login, password):
        user = login
    else:
        error = True
        message = '<p>Такой пользователь не зарегистрирован</p>'
elif action == "register":
    util.register(login, password)
    message = '<p>Вы зарегистрированы и уже авторизованы</p>'
elif action == "logout":
    util.logout(user)
    message = "<p>Вы вышли из системы</p>"
elif not action:
    if not util.is_online(user):
        action = "logout"
elif action == "posting":
    util.set_post(user, posts)


if action == "logout" or error:
    form = '''
        <h1>Авторизуйтесь</h1>
        <form method="post" action="wall.py">
            Логин: <input type="text" name="login">
            Пароль: <input type="password" name="password">
            <input type="hidden" name="action" value="login">
            <input type="submit">
        </form>
        <h1>Еще не зарегистрированы?</h1>
        <form method="post" action="wall.py">
            Логин: <input type="text" name="login">
            Пароль: <input type="password" name="password">
            <input type="hidden" name="action" value="register">
            <input type="submit">
        </form>
    '''
else:
    form = '''
        <form action="wall.py">
            <input type="hidden" name="action" value="logout">
            <input type="submit" value="Выйти">
        </form>
        <form action="wall.py">
            <h3>Добавить новый пост</h3>
            <textarea name="post"></textarea>
            <br>
            <input type="hidden" name="action" value="set_post">
            <input type="submit">
        </form>
    '''
    for i in util.get_posts(user):
        form += f'<p>{i}</p>'

pattern = f'''
<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Wall</title>
</head>
<body>
    {form}

    {message}
    
    {posts}
</body>
</html>
'''

print('Content-type: text/html\n')
print(pattern.format(form=form, message=message))
