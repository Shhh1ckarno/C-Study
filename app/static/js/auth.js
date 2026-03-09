document.addEventListener('DOMContentLoaded', () => {

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            const errorBlock = document.getElementById('error-message');

            try {
                const response = await fetch('/users/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    window.location.href = '/auth';
                } else {
                    const errorData = await response.json();
                    const msg = Array.isArray(errorData.detail) ? errorData.detail[0].msg : errorData.detail;
                    errorBlock.innerText = msg || 'Ошибка входа';
                    errorBlock.style.display = 'block';
                }
            } catch (err) {
                errorBlock.innerText = 'Сервер недоступен';
                errorBlock.style.display = 'block';
            }
        });
    }

    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        const pass1 = document.getElementById('password1');
        const pass2 = document.getElementById('password2');
        const errorText = document.getElementById('password-error') || document.querySelector('.password_input_block:last-of-type .field-message h5');

        const toggleError = (show, message = '') => {
            if (errorText) {
                errorText.style.display = show ? 'block' : 'none';
                if (message) errorText.innerText = message;
            }
        };

        [pass1, pass2].forEach(input => {
            input.addEventListener('input', () => {
                if (pass1.value === pass2.value) {
                    toggleError(false);
                }
            });
        });

        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value.trim();
            const password = pass1.value;
            const passwordConfirm = pass2.value;

            if (password !== passwordConfirm) {
                toggleError(true, 'Пароли не совпадают!');
                return;
            }

            try {
                const response = await fetch('/users/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password }) 
                });

                if (response.ok) {
                    window.location.href = `/auth/login_page?email=${encodeURIComponent(email)}`;
                } else {
                    const errorData = await response.json();
                    const msg = Array.isArray(errorData.detail) ? errorData.detail[0].msg : errorData.detail;
                    toggleError(true, msg || 'Ошибка регистрации');
                }
            } catch (err) {
                toggleError(true, 'Ошибка сети');
            }
        });
    }
});