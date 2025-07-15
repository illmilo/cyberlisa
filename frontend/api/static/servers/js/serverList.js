document.addEventListener('DOMContentLoaded', function() {
    const API_BASE_URL = 'http://localhost:8000/servers'; // FastAPI endpoint
    const form = document.getElementById('server-form');
    const serverListContainer = document.querySelector('.list-content');
    const searchInput = document.querySelector('.search-box input');

    // Only initialize if elements exist
    if (form) {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            await createServer();
        });
    }

    if (serverListContainer) {
        // Initialize
        loadServers();
        
        // Event delegation for action buttons
        serverListContainer.addEventListener('click', async (event) => {
            const userId = event.target.closest('[data-server-id]')?.dataset.serverId;
            if (!userId) return;
            
            if (event.target.classList.contains('delete-btn')) {
                await deleteServer(userId);
            }
        });
    } else {
        console.warn("SErver list container not found");
    }

    if (searchInput && serverListContainer) {
        searchInput.addEventListener('input', function() {
            filterServerList(this.value);
        });
    }

    function filterServerList(query) {
        const items = serverListContainer.querySelectorAll('.list-item');
        const lowerQuery = query.trim().toLowerCase();
        items.forEach(item => {
            // Ищем имя пользователя только по h3 внутри .user-info
            const nameElem = item.querySelector('.user-info h3');
            const name = nameElem ? nameElem.textContent.toLowerCase() : '';
            item.style.display = name.includes(lowerQuery) ? '' : 'none';
        });
    }

    // Load servers from API
    async function loadServers() {
        try {
            const response = await fetch(`${API_BASE_URL}/`);
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }
            
            // Handle empty response
            if (response.status === 204) {
                renderServersList([]);
                return;
            }
            
            const servers = await response.json();
            renderServersList(servers);
        } catch (error) {
            console.error('Error loading users:', error);
            alert(`Error loading users: ${error.message}`);
        }
    }

    // Render user list safely
    function renderServersList(servers) {
        if (!serverListContainer) {
            console.warn("Cannot render servers list: container not found");
            return;
        }
        
        // Clear existing content
        serverListContainer.innerHTML = '';
        
        // Handle empty user list
        if (!servers || servers.length === 0) {
            serverListContainer.innerHTML = '<div class="no-servers">No servers found</div>';
            return;
        }
        
        // Handle both single user and array responses
        const serverArray = Array.isArray(servers) ? servers : [servers];
        
        serverArray.forEach(server => {
            const serverElement = document.createElement('div');
            serverElement.className = 'list-item';
            serverElement.dataset.userId = server.id;
            serverElement.innerHTML = `
                <div class="server-info">
                    <h3>${server.name || 'Unnamed Server'}</h3>
                    <p>ID: ${server.id || 'N/A'}</p>
                    <p>IP: ${server.ip || 'N/A'}</p>
                    <p>PORT: ${server.port || 'N/A'}</p>
                </div>
                <div class="server-actions">
                    <button class="btn delete-btn">Delete</button>
                </div>
            `;
            serverListContainer.appendChild(serverElement);
        });
    }

    // Create new user with better error handling
    async function createServer() {
        try {
            const formData = {
                name: document.getElementById('server_name').value,
                ip: document.getElementById('address').value,
                port: document.getElementById('port').value
            };

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

            const newServer = await response.json();
            alert(`Server created successfully! ID: ${newServer.id}`);
            if (form) form.reset();
            loadServers();
        } catch (error) {
            console.error('Error creating server:', error);
            alert(`Error creating server: ${error.message}`);
        }
    }

    // Delete user with better error handling
    async function deleteServer(serverId) {
        if (!confirm(`Delete user ${serverId}?`)) return;
        
        try {
            const response = await fetch(`${API_BASE_URL}/${serverId}/`, {
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
            alert(result.message || `User ${serverId} deleted successfully`);
            loadServers();
        } catch (error) {
            console.error('Error deleting server:', error);
            alert(`Error deleting server: ${error.message}`);
        }
    }
});