document.addEventListener('DOMContentLoaded', () => {

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const errorBlock = document.getElementById('error-message');

            const response = await fetch('/users/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                window.location.href = '/auth';
            } else {
                const errorData = await response.json();
                errorBlock.innerText = errorData.detail || 'Ошибка входа';
            }
        });
    }


    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password1').value;
            const passwordConfirm = document.getElementById('password2').value;
            const errorBlock = document.getElementById('server-error');

          
            if (password !== passwordConfirm) {
                errorBlock.innerText = 'Пароли не совпадают!';
                return;
            }

            const response = await fetch('/users/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                alert('Регистрация прошла успешно!');
                window.location.href = '/auth/login_page'; 
            } else {
                const errorData = await response.json();
                errorBlock.innerText = errorData.detail || 'Ошибка регистрации';
            }
        });
    }
});