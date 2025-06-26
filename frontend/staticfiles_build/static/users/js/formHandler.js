document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('create-user-form');
    form.addEventListener('submit', handleFormSubmit);
    
    function handleFormSubmit(event) {
        event.preventDefault();
        
        // Get selected actions
        const actionCheckboxes = document.querySelectorAll('#actions-container input[type="checkbox"]:checked');
        const actions = Array.from(actionCheckboxes).map(cb => cb.value);
        
        // Get selected servers
        const serverCheckboxes = document.querySelectorAll('#servers-container input[type="checkbox"]:checked');
        const servers = Array.from(serverCheckboxes).map(cb => cb.value);
        
        // Prepare form data
        const formData = {
            username: document.getElementById('username').value,
            role: document.getElementById('role').value,
            actions: actions,
            servers: servers
        };
        
        // Send to API
        fetch(window.location.origin + '/users/api/users/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            return response.json().then(err => Promise.reject(err));
        })
        .then(data => {
            alert('User created successfully!');
            form.reset();
            // Refresh user list (you'll implement this later)
        })
        .catch(error => {
            console.error('Error:', error);
            alert(`Error creating user: ${error.detail || JSON.stringify(error)}`);
        });
    }
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Initialize dropdowns
    document.querySelectorAll('.dropdown-check-list').forEach(dropdown => {
        dropdown.addEventListener('click', function() {
            this.classList.toggle('active');
        });
    });
});