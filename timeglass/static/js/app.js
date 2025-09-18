/**
 * TimeGlass Dashboard - Base JavaScript functionality
 */

// Global error handler
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    // Could send to error tracking service
});

// Global utility functions
const Utils = {
    /**
     * Format duration in milliseconds
     */
    formatDuration: function(ms) {
        if (!ms) return 'N/A';
        if (ms < 1000) return `${ms.toFixed(2)}ms`;
        return `${(ms / 1000).toFixed(2)}s`;
    },

    /**
     * Format bytes
     */
    formatBytes: function(bytes) {
        if (!bytes) return 'N/A';
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        return `${(bytes / Math.pow(1024, i)).toFixed(2)} ${sizes[i]}`;
    },

    /**
     * Format percentage
     */
    formatPercent: function(value) {
        if (value === null || value === undefined) return 'N/A';
        return `${value.toFixed(1)}%`;
    },

    /**
     * Get status code CSS class
     */
    getStatusClass: function(statusCode) {
        if (!statusCode) return 'status-code-default';
        if (statusCode >= 200 && statusCode < 300) return 'status-code-2xx';
        if (statusCode >= 300 && statusCode < 400) return 'status-code-3xx';
        if (statusCode >= 400 && statusCode < 500) return 'status-code-4xx';
        if (statusCode >= 500) return 'status-code-5xx';
        return 'status-code-default';
    },

    /**
     * Get HTTP method CSS class
     */
    getMethodClass: function(method) {
        if (!method) return 'method-default';
        switch (method.toUpperCase()) {
            case 'GET': return 'method-get';
            case 'POST': return 'method-post';
            case 'PUT': return 'method-put';
            case 'DELETE': return 'method-delete';
            default: return 'method-default';
        }
    },

    /**
     * Get performance metric CSS class
     */
    getPerformanceClass: function(value, type) {
        if (value === null || value === undefined) return 'perf-neutral';

        switch (type) {
            case 'duration':
                if (value < 100) return 'perf-good';
                else if (value < 500) return 'perf-warning';
                else return 'perf-critical';

            case 'cpu':
                if (value < 50) return 'perf-good';
                else if (value < 80) return 'perf-warning';
                else return 'perf-critical';

            case 'memory':
                if (value < 60) return 'perf-good';
                else if (value < 85) return 'perf-warning';
                else return 'perf-critical';

            default:
                return 'perf-neutral';
        }
    },

    /**
     * Format timestamp
     */
    formatTimestamp: function(isoString) {
        if (!isoString) return 'N/A';
        try {
            return new Date(isoString).toLocaleString();
        } catch (e) {
            return isoString;
        }
    },

    /**
     * Show loading state
     */
    showLoading: function(element, message = 'Loading...') {
        element.innerHTML = `
            <div class="flex items-center justify-center py-12">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <span class="ml-2 text-gray-600">${message}</span>
            </div>
        `;
    },

    /**
     * Show error state
     */
    showError: function(element, message = 'An error occurred') {
        element.innerHTML = `
            <div class="text-center py-12">
                <div class="text-red-500 mb-4">
                    <svg class="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                    </svg>
                </div>
                <h3 class="text-lg font-medium text-gray-900 mb-2">Error</h3>
                <p class="text-gray-600">${message}</p>
            </div>
        `;
    }
};

// API client
const API = {
    baseURL: '',

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`API Error (${endpoint}):`, error);
            throw error;
        }
    },

    async getStats() {
        return this.request('/api/stats');
    },

    async getRequests(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.request(`/api/requests?${queryString}`);
    },

    async getSystemMetrics(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.request(`/api/system-metrics?${queryString}`);
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('TimeGlass Dashboard initialized');
});
