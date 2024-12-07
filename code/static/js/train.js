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