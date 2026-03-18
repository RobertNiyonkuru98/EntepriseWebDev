document.addEventListener('DOMContentLoaded', () => {
    const applyBtn = document.getElementById('applyFilters');

    // Function to fetch data from your Python API
    async function fetchData() {
        const borough = document.getElementById('boroughFilter').value;
        const url = `http://127.0.0.1:5000/api/trips?borough=${borough}&limit=100`;

        try {
            const response = await fetch(url);
            const data = await response.json();

            // Update Stats
            document.getElementById('totalTrips').innerText = data.length;

            console.log("Data fetched successfully:", data);
            // Here you would call your Chart.js update functions
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    }

    if(applyBtn) {
        applyBtn.addEventListener('click', fetchData);
    }
});