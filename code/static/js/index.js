function resetDataset() {
    fetch('/reset_dataset', { method: 'POST' })
        .then(response => {
            if (response.ok) {
                location.reload(); // Reload the page after a successful reset
            } else {
                response.text().then(text => alert("Error: " + text));
            }
        })
        .catch(error => alert("An error occurred: " + error));
}

function shutdownServer() {
    fetch('/shutdown', { method: 'POST' })
        .then(response => {
            if (response.ok) {
                alert("Server is shutting down...");
            } else {
                alert("Failed to shut down the server.");
            }
        })
        .catch(error => alert("An error occurred: " + error));
}