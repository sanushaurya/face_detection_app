const API_BASE = 'http://localhost:5000';
let allRecords = [];

// DOM Elements
const tableBody = document.getElementById('tableBody');
const filterNameInput = document.getElementById('filterName');
const filterDateInput = document.getElementById('filterDate');
const filterBtn = document.getElementById('filterBtn');
const resetBtn = document.getElementById('resetBtn');
const exportBtn = document.getElementById('exportBtn');
const statusMessage = document.getElementById('statusMessage');
const recordCount = document.getElementById('recordCount');

// Load attendance records on page load
document.addEventListener('DOMContentLoaded', () => {
    loadAttendanceRecords();
});

// Event listeners
filterBtn.addEventListener('click', applyFilters);
resetBtn.addEventListener('click', resetFilters);
exportBtn.addEventListener('click', exportToCSV);

async function loadAttendanceRecords() {
    try {
        const response = await fetch(`${API_BASE}/api/attendance`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch attendance records');
        }
        
        allRecords = await response.json();
        displayRecords(allRecords);
        updateRecordCount(allRecords.length);
    } catch (error) {
        console.error('Error loading records:', error);
        showStatus('Error loading attendance records: ' + error.message, 'error');
        tableBody.innerHTML = `
            <tr>
                <td colspan="4" class="empty-state">
                    <p>Error loading records. Please check if the backend is running.</p>
                </td>
            </tr>
        `;
    }
}

function displayRecords(records) {
    if (records.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="4" class="empty-state">
                    <p>No attendance records found.</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tableBody.innerHTML = records.map(record => `
        <tr>
            <td>${escapeHtml(record.name)}</td>
            <td>${formatDateTime(record.timestamp)}</td>
            <td>${(record.confidence * 100).toFixed(2)}%</td>
            <td>
                <button class="delete-btn" onclick="deleteRecord(${record.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

function applyFilters() {
    const name = filterNameInput.value.trim();
    const date = filterDateInput.value;
    
    let filtered = allRecords;
    
    if (name) {
        filtered = filtered.filter(record => 
            record.name.toLowerCase().includes(name.toLowerCase())
        );
    }
    
    if (date) {
        filtered = filtered.filter(record => {
            const recordDate = record.timestamp.split('T')[0];
            return recordDate === date;
        });
    }
    
    displayRecords(filtered);
    updateRecordCount(filtered.length);
    showStatus(`Showing ${filtered.length} record(s)`, 'success');
}

function resetFilters() {
    filterNameInput.value = '';
    filterDateInput.value = '';
    displayRecords(allRecords);
    updateRecordCount(allRecords.length);
    showStatus('Filters reset', 'success');
}

async function deleteRecord(recordId) {
    if (!confirm('Are you sure you want to delete this record?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/attendance/${recordId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete record');
        }
        
        showStatus('Record deleted successfully', 'success');
        loadAttendanceRecords();
    } catch (error) {
        console.error('Error deleting record:', error);
        showStatus('Error deleting record: ' + error.message, 'error');
    }
}

function exportToCSV() {
    if (allRecords.length === 0) {
        showStatus('No records to export', 'error');
        return;
    }
    
    const headers = ['Person Name', 'Timestamp', 'Confidence (%)'];
    const rows = allRecords.map(record => [
        record.name,
        formatDateTime(record.timestamp),
        (record.confidence * 100).toFixed(2)
    ]);
    
    let csv = headers.join(',') + '\n';
    rows.forEach(row => {
        csv += row.map(cell => `"${cell}"`).join(',') + '\n';
    });
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `attendance_${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showStatus('Attendance data exported successfully', 'success');
}

function formatDateTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

function updateRecordCount(count) {
    recordCount.textContent = count;
}

function showStatus(message, type) {
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    
    setTimeout(() => {
        statusMessage.className = 'status-message';
    }, 5000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
