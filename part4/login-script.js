document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const url = 'http://127.0.0.1:6010/api/v1/auths/login';

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password }),
                });

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/`;
                    window.location.href = 'index.html';
                } else {
                    const error = await response.json();
                    console.error('Error response:', error);
                    alert('Login failed: ' + (error.message || response.statusText));
                }
            } catch (error) {
                console.error('Fetch failed:', error);
                alert('An unexpected error occurred. Check the console for details.');
            }
        });
    }
});