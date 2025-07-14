document.addEventListener('DOMContentLoaded', function() {
    const API_BASE_URL = 'http://localhost:8000/agents'; // FastAPI endpoint
    const form = document.getElementById('create-user-form');
    const userListContainer = document.querySelector('.list-content');
    const searchInput = document.querySelector('.search-box input');

    // Only initialize if elements exist
    if (form) {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            await createUser();
        });
    }

    if (userListContainer) {
        // Initialize
        loadUsers();
        
        // Event delegation for action buttons
        userListContainer.addEventListener('click', async (event) => {
            const userId = event.target.closest('[data-user-id]')?.dataset.userId;
            if (!userId) return;
            
            if (event.target.classList.contains('delete-btn')) {
                await deleteUser(userId);
            }
        });
    } else {
        console.warn("User list container not found");
    }

    if (searchInput && userListContainer) {
        searchInput.addEventListener('input', function() {
            filterUserList(this.value);
        });
    }

    function filterUserList(query) {
        const items = userListContainer.querySelectorAll('.list-item');
        const lowerQuery = query.trim().toLowerCase();
        items.forEach(item => {
            // Ищем имя пользователя только по h3 внутри .user-info
            const nameElem = item.querySelector('.user-info h3');
            const name = nameElem ? nameElem.textContent.toLowerCase() : '';
            item.style.display = name.includes(lowerQuery) ? '' : 'none';
        });
    }

    // Load users from API
    async function loadUsers() {
        try {
            const response = await fetch(`${API_BASE_URL}/`);
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }
            
            // Handle empty response
            if (response.status === 204) {
                renderUserList([]);
                return;
            }
            
            const users = await response.json();
            renderUserList(users);
        } catch (error) {
            console.error('Error loading users:', error);
            alert(`Error loading users: ${error.message}`);
        }
    }

    // Render user list safely
    function renderUserList(users) {
        if (!userListContainer) {
            console.warn("Cannot render user list: container not found");
            return;
        }
        
        // Clear existing content
        userListContainer.innerHTML = '';
        
        // Handle empty user list
        if (!users || users.length === 0) {
            userListContainer.innerHTML = '<div class="no-users">No users found</div>';
            return;
        }
        
        // Handle both single user and array responses
        const userArray = Array.isArray(users) ? users : [users];
        
        userArray.forEach(user => {
            const userElement = document.createElement('div');
            userElement.className = 'list-item';
            userElement.dataset.userId = user.id;
            userElement.innerHTML = `
                <div class="user-info">
                    <h3>${user.name || 'Unnamed User'}</h3>
                    <p>ID: ${user.id || 'N/A'}</p>
                    <p>Role: ${user.role || 'N/A'}</p>
                    <p>OS: ${user.os || 'N/A'}</p>
                    <p>Activity Rate: ${user.activity_rate || 0}%</p>
                </div>
                <div class="user-actions">
                    <button class="btn delete-btn">Delete</button>
                </div>
            `;
            userListContainer.appendChild(userElement);
        });
    }

    // Create new user with better error handling
    async function createUser() {
        try {
            const formData = {
                name: document.getElementById('user_name').value,
                role: document.getElementById('role').value,
                os: document.getElementById('os').value,
                activity_rate: parseInt(document.getElementById('activity_rate').value) || 0,
                online: false,
                work_start_time: "09:00",
                work_end_time: "17:00"
            };
            
            // Add activity_now if available
            const activitySelect = document.getElementById('activity');
            if (activitySelect) {
                formData.activity_now = activitySelect.value === 'word' ? 1 : 2;
            }

            console.log("Sending data:", formData);
            
            const response = await fetch(`${API_BASE_URL}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                let errorMessage = `HTTP ${response.status}`;
                
                try {
                    const errorData = await response.json();
                    if (errorData.detail) {
                        errorMessage += `: ${errorData.detail}`;
                    } else if (errorData.error) {
                        errorMessage += `: ${errorData.error}`;
                    }
                } catch (e) {
                    // Couldn't parse JSON error
                    const text = await response.text();
                    errorMessage += `: ${text}`;
                }
                
                throw new Error(errorMessage);
            }

            const newUser = await response.json();
            alert(`User created successfully! ID: ${newUser.id}`);
            if (form) form.reset();
            loadUsers();
        } catch (error) {
            console.error('Error creating user:', error);
            alert(`Error creating user: ${error.message}`);
        }
    }

    // Delete user with better error handling
    async function deleteUser(userId) {
        if (!confirm(`Delete user ${userId}?`)) return;
        
        try {
            const response = await fetch(`${API_BASE_URL}/${userId}/`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                let errorMessage = `HTTP ${response.status}`;
                
                try {
                    const errorData = await response.json();
                    if (errorData.detail) {
                        errorMessage += `: ${errorData.detail}`;
                    } else if (errorData.error) {
                        errorMessage += `: ${errorData.error}`;
                    }
                } catch (e) {
                    // Couldn't parse JSON error
                    const text = await response.text();
                    errorMessage += `: ${text}`;
                }
                
                throw new Error(errorMessage);
            }
            
            const result = await response.json();
            alert(result.message || `User ${userId} deleted successfully`);
            loadUsers();
        } catch (error) {
            console.error('Error deleting user:', error);
            alert(`Error deleting user: ${error.message}`);
        }
    }

    // Helper function to get CSRF token (if needed)
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
});