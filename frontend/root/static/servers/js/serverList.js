
document.addEventListener('DOMContentLoaded', function() {
    const API_BASE_URL = 'http://localhost:8000/servers'; // FastAPI endpoint
    const form = document.getElementById('server-form');
    const serverListContainer = document.querySelector('.list-content');
    const searchInput = document.querySelector('.search-box input');
async function populateServerDropdown() {
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        if (!response.ok) throw new Error('Failed to fetch servers');
        
        const servers = await response.json();
        const select = document.getElementById('server_id');
        
        // Clear existing options
        select.innerHTML = '';
        
        // Add default option
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = 'Select a server';
        defaultOption.disabled = true;
        defaultOption.selected = true;
        select.appendChild(defaultOption);
        
        // Add server options
        servers.forEach(server => {
            const option = document.createElement('option');
            option.value = server.id;
            option.textContent = server.name || `Server ${server.id}`;
            select.appendChild(option);
        });
        
    } catch (error) {
        console.error('Error loading servers for dropdown:', error);
    }
}
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
            const serverId = event.target.closest('[data-server-id]')?.dataset.serverId;
            if (!serverId) return;
            
            if (event.target.classList.contains('delete-btn')) {
                await deleteServer(serverId);
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
            const nameElem = item.querySelector('.server-info h3');
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
            console.error('Error loading servers:', error);
            alert(`Error loading servers: ${error.message}`);
        }
    }

    function renderServersList(servers) {
        if (!serverListContainer) {
            console.warn("Cannot render servers list: container not found");
            return;
        }
        
        // Clear existing content
        serverListContainer.innerHTML = '';
        
        if (!servers || servers.length === 0) {
            serverListContainer.innerHTML = '<div class="no-servers">No servers found</div>';
            return;
        }
        
        const serverArray = Array.isArray(servers) ? servers : [servers];
        
        serverArray.forEach(server => {
            const serverElement = document.createElement('div');
            serverElement.className = 'list-item';
            serverElement.dataset.serverId = server.id;
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

    async function deleteServer(serverId) {
        if (!confirm(`Delete server ${serverId}?`)) return;
        
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
            alert(result.message || `Server ${serverId} deleted successfully`);
            loadServers();
        } catch (error) {
            console.error('Error deleting server:', error);
            alert(`Error deleting server: ${error.message}`);
        }
    }

    if (document.getElementById('server_id')) {
        populateServerDropdown();
    }
});