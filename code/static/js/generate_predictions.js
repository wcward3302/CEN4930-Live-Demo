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