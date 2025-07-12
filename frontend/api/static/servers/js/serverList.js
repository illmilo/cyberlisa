document.addEventListener('DOMContentLoaded', function() {
    const API_BASE_URL = 'http://localhost:8000/servers'; // FastAPI endpoint
    const serverListContainer = document.querySelector('.list-content');

    if (serverListContainer) {
        loadServers();
    } else {
        console.warn("Server list container not found");
    }

    async function loadServers() {
        try {
            const response = await fetch(`${API_BASE_URL}/`);
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }
            const servers = await response.json();
            renderServerList(servers);
        } catch (error) {
            console.error('Error loading servers:', error);
            serverListContainer.innerHTML = `<div class="no-users">Error loading servers: ${error.message}</div>`;
        }
    }

    function renderServerList(servers) {
        if (!serverListContainer) return;
        serverListContainer.innerHTML = '';
        if (!servers || servers.length === 0 || servers.error) {
            serverListContainer.innerHTML = '<div class="no-users">No servers found</div>';
            return;
        }
        const serverArray = Array.isArray(servers) ? servers : [servers];
        serverArray.forEach(server => {
            const serverElement = document.createElement('div');
            serverElement.className = 'list-item';
            serverElement.innerHTML = `
                <div class="server-info">
                    <h3>${server.name || 'Unnamed Server'}</h3>
                    <p>ID: ${server.id || 'N/A'}</p>
                    <p>IP: ${server.ip || 'N/A'}</p>
                    <p>Port: ${server.port || 'N/A'}</p>
                </div>
            `;
            serverListContainer.appendChild(serverElement);
        });
    }

    const searchInput = document.querySelector('.search-box input');
    if (searchInput && serverListContainer) {
        searchInput.addEventListener('input', function() {
            filterServerList(this.value);
        });
    }

    function filterServerList(query) {
        const items = serverListContainer.querySelectorAll('.list-item');
        const lowerQuery = query.trim().toLowerCase();
        items.forEach(item => {
            // Ищем имя сервера только по h3 внутри .server-info
            const nameElem = item.querySelector('.server-info h3');
            const name = nameElem ? nameElem.textContent.toLowerCase() : '';
            item.style.display = name.includes(lowerQuery) ? '' : 'none';
        });
    }
}); 