document.querySelector('button').onclick = myClick;

function myClick(){
    let surname = document.querySelector('.surname').value; 
    let name = document.querySelector('.name').value; 
    let login = document.querySelector('.login').value;
    let password = document.querySelector('.password').value;
    let password_conf = document.querySelector('.password_conf').value;
    
    let flag = 0;
    
    if (surname == '')
        {
            alert("Введите фамилию")
            document.getElementsByClassName('surname')[0].style= "border-color: red";
            flag = 1;
        }
    
    if (name == '')
        {
            alert("Введите имя");
            document.getElementsByClassName('name')[0].style= "border-color: red";
            flag = 1;
        }
    
    if (login.length < 6)
        {
            alert("Логин должен содержать не менее 6 символов");
            document.getElementsByClassName('login')[0].style= "border-color: red";
            flag = 1;
        }
    
    if (password.length < 6)
        {
            alert("Пароль должен содержать не менее 6 символов");
            document.getElementsByClassName('password')[0].style= "border-color: red";
            flag = 1;
        }    
    
    if (password_conf != password)
        {
            alert("Введенные пароли не совпадают");
            document.getElementsByClassName('password_conf')[0].style= "border-color: red";
            flag = 1;
        }
    
    if (flag != 1)
        {
            alert("Регистрация успешно пройдена!");
        }
}