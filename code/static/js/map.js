// Map Code

// Fetch heat map data and add to the map
function generateHeatMap(selectedYear) {
    fetch('/get_heatmap_data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ year: selectedYear })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            // Clear existing layers (if any)
            if (window.heatLayer) {
                map.removeLayer(window.heatLayer);
            }

            // Add new heat map layer
            window.heatLayer = L.heatLayer(data.heatmap_data, { radius: 15 }).addTo(map);
        })
        .catch(err => {
            console.error('Error fetching heatmap data:', err);
        });
}

// Initialize the map
const map = L.map('map').setView([27.994402, -81.760254], 7);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Dynamically pass the selected year from HTML to JavaScript
const selectedYear = document.getElementById('map').dataset.year;
generateHeatMap(selectedYear);

// Handle map click event for nearest point lookup
function onMapClick(e) {
    const clickedLat = e.latlng.lat;
    const clickedLng = e.latlng.lng;

    const outputDiv = document.getElementById('output');

    fetch('/get_nearest_data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ latitude: clickedLat, longitude: clickedLng })
    })
        .then(response => response.json())
        .then(data => {
            const selectedYear = parseInt(document.getElementById('map').dataset.year, 10);
            const filteredData = Object.keys(data)
                .filter(key => !isNaN(parseInt(key, 10)) && parseInt(key, 10) <= selectedYear) // Include years <= selected year
                .reduce((result, key) => {
                    result[key] = data[key];
                    return result;
                }, {});

            // Display data or error message
            if (Object.keys(filteredData).length > 0) {
                const dataEntries = Object.entries(filteredData)
                    .map(([year, value]) => {
                        const isPredicted = parseInt(year, 10) === 2029 ? " - AI predicted value" : "";
                        return `<p><strong>Year ${year}:</strong> ${value}${isPredicted}</p>`;
                    })
                    .join("");

                outputDiv.innerHTML = `
                    <h2>Nearest Data:</h2>
                    <p><strong>Coordinates:</strong> (${data.latitude.toFixed(4)}, ${data.longitude.toFixed(4)})</p>
                    ${dataEntries}
                `;
            } else {
                outputDiv.innerHTML = `
                    <h2>Nearest Data:</h2>
                    <p style="color: red;">No data available for the selected year (${selectedYear}) or earlier.</p>
                `;
            }
        })
        .catch(err => {
            outputDiv.innerHTML = `<h2>Error:</h2><pre>${err.message}</pre>`;
        });
}

map.on('click', onMapClick);