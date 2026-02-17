const API_BASE_URL = "http://127.0.0.1:5001/api";

async function testConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/trips?limit=5`);
        const data = await response.json();

        if (data.length > 0) {
            console.log("Integration Successful: Data recieveid from Neon via Flask");
            document.getElementById("totalTrips").innerText = data.length;
        }
    }
    catch (Error){
        console.error("Integration Failed:", error);
    }
}

document.addEventListener('DOMContentLoaded', testConnection)