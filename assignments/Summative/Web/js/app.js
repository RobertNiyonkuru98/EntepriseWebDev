const API_BASE_URL = "http://127.0.0.1:5001/api";
let tripChart; // Global variable to hold the chart instance

async function updateDashboard() {
    const boroughFilter = document.getElementById('boroughFilter');
    if (!boroughFilter) return; // Exit if not on dashboard page

    const borough = boroughFilter.value;
    const totalTripsEl = document.getElementById('totalTrips');
    const avgSpeedEl = document.getElementById('avgSpeed');
    const avgFareEl = document.getElementById('avgFare');

    // Show loading state
    totalTripsEl.innerText = "Loading...";

    try {
        // Increase limit from 5 to 100 to get a better average
        const response = await fetch(`${API_BASE_URL}/trips?borough=${borough}&limit=100`);
        const data = await response.json();

        if (data.length > 0) {
            // 1. Update KPI Cards
            totalTripsEl.innerText = data.length.toLocaleString();

            // Calculate averages from the current view
            const avgSpeed = data.reduce((acc, row) => acc + (row.avg_speed_kmh || 0), 0) / data.length;
            const avgFare = data.reduce((acc, row) => acc + (row.fare_amount || 0), 0) / data.length;

            avgSpeedEl.innerText = avgSpeed.toFixed(1) + " km/h";
            avgFareEl.innerText = "$" + avgFare.toFixed(2);

            // 2. Trigger Chart Update
            renderChart(data);
        } else {
            totalTripsEl.innerText = "0";
            avgSpeedEl.innerText = "--";
            avgFareEl.innerText = "--";
        }
    } catch (error) {
        console.error("Dashboard Update Failed:", error);
        totalTripsEl.innerText = "Error";
    }
}

// Function removed to be integrated into event listener


function renderChart(data) {
    const ctx = document.getElementById('tripChart').getContext('2d');

    // Destroy previous chart if it exists to prevent overlapping
    if (tripChart) { tripChart.destroy(); }

    // Aggregate data for the chart (e.g., trips by pickup hour)
    const hourCounts = {};
    data.forEach(trip => {
        const hour = trip.pickup_hour;
        hourCounts[hour] = (hourCounts[hour] || 0) + 1;
    });

    tripChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(hourCounts).sort((a, b) => a - b),
            datasets: [{
                label: 'Number of Trips',
                data: Object.values(hourCounts),
                backgroundColor: 'rgba(0, 0, 0, 0.1)',
                borderColor: 'rgba(0, 0, 0, 1)',
                borderWidth: 1
            }]
        },
        options: { responsive: true, scales: { y: { beginAtZero: true } } }
    });
}

// Single Event Listener Hub
document.addEventListener('DOMContentLoaded', () => {
    // Initialize Dashboard
    updateDashboard();

    const applyBtn = document.getElementById('applyFilters');
    if (applyBtn) {
        applyBtn.addEventListener('click', updateDashboard);
    }

    // Logic for Algorithm Page
    const algoBtn = document.getElementById('loadAlgorithmData');
    if (algoBtn) {
        algoBtn.addEventListener('click', async () => {
            const boroughEl = document.getElementById('boroughFilter');
            const borough = boroughEl ? boroughEl.value : 'Manhattan';
            const response = await fetch(`${API_BASE_URL}/top_fares?borough=${borough}`);
            const data = await response.json();
            const tbody = document.getElementById('algorithmResults');
            tbody.innerHTML = data.map(trip => `
                <tr>
                    <td>${trip.pickup_borough}</td>
                    <td>${trip.dropoff_borough}</td>
                    <td>$${trip.fare_amount.toFixed(2)}</td>
                </tr>
            `).join('');
        });
    }

    // Logic for Spatial Map
    if (document.getElementById('map')) {
        const map = L.map('map').setView([40.7128, -74.0060], 11);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

        fetch('../assets/taxi_zones.json')
            .then(res => res.json())
            .then(geojsonData => {
                L.geoJSON(geojsonData, {
                    style: { color: "black", weight: 1, fillOpacity: 0.1 }
                }).addTo(map);
            });
    }

    // Logic for Trips Explorer
    const tripContainer = document.getElementById('tripListContainer');
    if (tripContainer) {
        let currentPage = 0;
        const searchInput = document.getElementById('tripSearch');
        const searchBtn = document.getElementById('searchBtn'); // New button reference
        const prevBtn = document.getElementById('prevPage');
        const nextBtn = document.getElementById('nextPage');
        const pageNumEl = document.getElementById('pageNumber');

        async function fetchTrips(page = 0) {
            const borough = searchInput.value || '';
            const offset = page * 10;
            const url = `${API_BASE_URL}/trips?borough=${borough}&limit=10&offset=${offset}`;

            tripContainer.innerHTML = '<p class="loading-text">Loading trips...</p>';

            try {
                const response = await fetch(url);
                const trips = await response.json();

                if (trips.length === 0) {
                     tripContainer.innerHTML = '<p class="loading-text">No trips found matching criteria.</p>';
                     return;
                }

                tripContainer.innerHTML = trips.map(trip => `
                    <div class="trip-card">
                        <div class="trip-header">
                            <div class="trip-id">Borough: ${trip.pickup_borough || 'Unknown'}</div>
                            <div class="trip-status">${trip.payment_type === 1 ? 'Credit Card' : 'Cash'}</div>
                        </div>
                        <div class="trip-details">
                            <div class="trip-detail-item">
                                <span class="trip-detail-label">Distance</span>
                                <span class="trip-detail-value">${trip.trip_distance} mi</span>
                            </div>
                            <div class="trip-detail-item">
                                <span class="trip-detail-label">Fare</span>
                                <span class="trip-detail-value">$${trip.fare_amount}</span>
                            </div>
                            <div class="trip-detail-item">
                                <span class="trip-detail-label">Speed</span>
                                <span class="trip-detail-value">${(trip.avg_speed_kmh || 0).toFixed(1)} km/h</span>
                            </div>
                        </div>
                        <div class="trip-route">
                            <strong>From:</strong> ${trip.pickup_zone || 'N/A'}
                            <span class="route-arrow"> → </span>
                            <strong>To:</strong> ${trip.dropoff_zone || 'N/A'}
                        </div>
                    </div>
                `).join('');

                // Update Pagination Interface
                pageNumEl.innerText = `Page ${page + 1}`;
                prevBtn.disabled = page === 0;
                prevBtn.style.opacity = page === 0 ? "0.5" : "1";

            } catch (e) {
                console.error(e);
                tripContainer.innerHTML = '<p class="loading-text">Error loading trips. Ensure backend is running.</p>';
            }
        }

        // Event Listeners
        if (searchBtn) {
            searchBtn.addEventListener('click', () => { currentPage = 0; fetchTrips(0); });
        }

        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') { currentPage = 0; fetchTrips(0); }
        });

        prevBtn.addEventListener('click', () => {
            if (currentPage > 0) {
                currentPage--;
                fetchTrips(currentPage);
            }
        });

        nextBtn.addEventListener('click', () => {
            currentPage++;
            fetchTrips(currentPage);
        });

        // Initial Load
        fetchTrips(0);
    }
});