// Generate_predictions Code

const trainFormGen = document.getElementById('trainForm');
const trainButtonGen = document.getElementById('trainButton');
const statusMessageGen = document.getElementById('statusMessage');
const resultMessageGen = document.getElementById('resultMessage');
    
trainFormGen.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent default form submission
    statusMessageGen.style.display = 'block';
    trainButtonGen.disabled = true;
    
    const formData = new FormData(trainFormGen);
    try {
        const response = await fetch('/generate_prediction_data', {
            method: 'POST',
            body: formData,
        });
    
        if (response.ok) {
            const result = await response.text();
            resultMessageGen.innerHTML = `<p>${result}</p>`;
            resultMessageGen.style.color = 'green';
        } else {
            const error = await response.text();
            resultMessageGen.innerHTML = `<p>Error: ${error}</p>`;
            resultMessageGen.style.color = 'red';
        }
    } catch (error) {
        resultMessageGen.innerHTML = `<p>An unexpected error occurred: ${error}</p>`;
        resultMessageGen.style.color = 'red';
    } finally {
        resultMessageGen.style.display = 'block';
        statusMessageGen.style.display = 'none';
        trainButtonGen.disabled = false;
    }
});



// Index Code

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



// Map Code




// Train Code

const trainForm = document.getElementById('trainForm');
const trainButton = document.getElementById('trainButton');
const statusMessage = document.getElementById('statusMessage');
const resultMessage = document.getElementById('resultMessage');

trainForm.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent default form submission
    statusMessage.style.display = 'block';
    trainButton.disabled = true;

    const formData = new FormData(trainForm);
    try {
        const response = await fetch('/train_model', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const result = await response.text();
            resultMessage.innerHTML = `<p>${result}</p>`;
            resultMessage.style.color = 'green';
        } else {
            const error = await response.text();
            resultMessage.innerHTML = `<p>Error: ${error}</p>`;
            resultMessage.style.color = 'red';
        }
    } catch (error) {
        resultMessage.innerHTML = `<p>An unexpected error occurred: ${error}</p>`;
        resultMessage.style.color = 'red';
    } finally {
        resultMessage.style.display = 'block';
        statusMessage.style.display = 'none';
        trainButton.disabled = false;
    }
});