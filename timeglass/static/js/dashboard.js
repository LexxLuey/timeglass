/**
 * TimeGlass Dashboard - Main dashboard functionality
 */

class Dashboard {
    constructor() {
        this.currentOffset = 0;
        this.limit = 50;
        this.filters = {};

        this.statsContainer = document.getElementById('stats-cards');
        this.requestsTable = document.getElementById('requests-table');
        this.loadMoreBtn = document.getElementById('load-more');
        this.applyFiltersBtn = document.getElementById('apply-filters');

        this.init();
    }

    init() {
        this.bindEvents();
        this.loadStats();
        this.loadRequests();
    }

    bindEvents() {
        if (this.applyFiltersBtn) {
            this.applyFiltersBtn.addEventListener('click', () => this.applyFilters());
        }

        if (this.loadMoreBtn) {
            this.loadMoreBtn.addEventListener('click', () => this.loadRequests(false));
        }
    }

    async loadStats() {
        try {
            Utils.showLoading(this.statsContainer, 'Loading statistics...');
            const stats = await API.getStats();
            this.renderStats(stats);
        } catch (error) {
            Utils.showError(this.statsContainer, 'Failed to load statistics');
            console.error('Error loading stats:', error);
        }
    }

    renderStats(stats) {
        this.statsContainer.innerHTML = `
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold text-gray-800">Total Requests</h3>
                <p class="text-2xl font-bold text-blue-600">${stats.total_requests.toLocaleString()}</p>
            </div>
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold text-gray-800">Avg Duration</h3>
                <p class="text-2xl font-bold text-green-600">${Utils.formatDuration(stats.avg_duration_ms)}</p>
            </div>
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold text-gray-800">Avg CPU</h3>
                <p class="text-2xl font-bold text-yellow-600">${Utils.formatPercent(stats.avg_cpu_percent)}</p>
            </div>
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold text-gray-800">Avg Memory</h3>
                <p class="text-2xl font-bold text-red-600">${Utils.formatPercent(stats.avg_memory_percent)}</p>
            </div>
        `;
    }

    async loadRequests(reset = true) {
        if (reset) {
            this.currentOffset = 0;
        }

        try {
            const params = {
                limit: this.limit,
                offset: this.currentOffset,
                ...this.filters
            };

            const response = await API.getRequests(params);
            const requests = response.data || response; // Handle different response formats

            if (reset) {
                this.clearRequestsTable();
            }

            this.renderRequests(requests);
            this.updateLoadMoreButton(requests.length);

            if (!reset) {
                this.currentOffset += requests.length;
            }

        } catch (error) {
            console.error('Error loading requests:', error);
            if (reset) {
                const tbody = this.requestsTable.querySelector('tbody');
                Utils.showError(tbody, 'Failed to load requests');
            }
        }
    }

    clearRequestsTable() {
        const tbody = this.requestsTable.querySelector('tbody');
        tbody.innerHTML = '';
    }

    renderRequests(requests) {
        const tbody = this.requestsTable.querySelector('tbody');

        requests.forEach(request => {
            const row = document.createElement('tr');
            row.className = 'hover:bg-gray-50 cursor-pointer transition-colors duration-150';
            row.onclick = () => window.location.href = `/request/${request.request_id}`;

            const startTime = Utils.formatTimestamp(request.start_time);
            const statusClass = Utils.getStatusClass(request.status_code);
            const methodClass = Utils.getMethodClass(request.method);
            const durationClass = Utils.getPerformanceClass(request.duration_ms, 'duration');
            const cpuClass = Utils.getPerformanceClass(request.cpu_usage_percent, 'cpu');
            const memoryClass = Utils.getPerformanceClass(request.memory_usage_percent, 'memory');

            row.innerHTML = `
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${startTime}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <span class="px-2 py-1 rounded text-xs font-medium ${methodClass}">${request.method || '-'}</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 truncate max-w-xs" title="${request.path || ''}">${request.path || '-'}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${statusClass}">
                        ${request.status_code || '-'}
                    </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">
                    <span class="px-2 py-1 rounded text-xs font-medium ${durationClass}">${Utils.formatDuration(request.duration_ms)}</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">
                    <span class="px-2 py-1 rounded text-xs font-medium ${cpuClass}">${Utils.formatPercent(request.cpu_usage_percent)}</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">
                    <span class="px-2 py-1 rounded text-xs font-medium ${memoryClass}">${Utils.formatPercent(request.memory_usage_percent)}</span>
                </td>
            `;

            tbody.appendChild(row);
        });
    }

    updateLoadMoreButton(requestsCount) {
        if (this.loadMoreBtn) {
            if (requestsCount === this.limit) {
                this.loadMoreBtn.classList.remove('hidden');
            } else {
                this.loadMoreBtn.classList.add('hidden');
            }
        }
    }

    applyFilters() {
        // Get filter values
        const pathFilter = document.getElementById('path-filter')?.value.trim() || '';
        const methodFilter = document.getElementById('method-filter')?.value || '';
        const statusFilter = document.getElementById('status-filter')?.value || '';

        // Update filters object
        this.filters = {};
        if (pathFilter) this.filters.path_contains = pathFilter;
        if (methodFilter) this.filters.method = methodFilter;
        if (statusFilter) this.filters.status_code = parseInt(statusFilter) || '';

        // Reload requests with filters
        this.loadRequests(true);
    }
}

// Initialize dashboard when DOM is ready and Utils is available
function initDashboard() {
    if (document.getElementById('stats-cards') && typeof Utils !== 'undefined') {
        new Dashboard();
    } else if (document.getElementById('stats-cards')) {
        // Wait a bit for Utils to load
        setTimeout(initDashboard, 50);
    }
}

document.addEventListener('DOMContentLoaded', initDashboard);
