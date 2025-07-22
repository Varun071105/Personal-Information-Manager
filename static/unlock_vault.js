document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('unlock-btn').addEventListener('click', function() {
        const password = document.getElementById('password').value;
        
        if (!password) {
            showError('Please enter your master password');
            return;
        }

        fetch('/unlock-vault', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = '/vault';
            } else {
                showError(data.message || 'Invalid password');
            }
        })
        .catch(error => {
            showError('An error occurred. Please try again.');
        });
    });

    function showError(message) {
        const errorEl = document.getElementById('error-message');
        errorEl.textContent = message;
        errorEl.style.display = 'block';
    }
});