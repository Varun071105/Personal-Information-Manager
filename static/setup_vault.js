document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('setup-btn').addEventListener('click', function() {
        const password = document.getElementById('password').value;
        const confirm = document.getElementById('confirm').value;
        
        if (!password || !confirm) {
            showError('Please enter and confirm your password');
            return;
        }

        if (password !== confirm) {
            showError('Passwords do not match');
            return;
        }

        if (password.length < 8) {
            showError('Password must be at least 8 characters');
            return;
        }

        fetch('/setup-vault', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ password, confirm })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = '/vault';
            } else {
                showError(data.message || 'Error setting up vault');
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