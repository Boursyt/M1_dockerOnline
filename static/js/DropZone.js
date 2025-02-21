const dockerDropZone = document.getElementById('dockerDropZone');
const dockerFileInput = document.getElementById('dockerFileInput');
const dockerFileNameDisplay = document.getElementById('dockerFileName');

dockerDropZone.addEventListener('click', () => {
    dockerFileInput.click();
});

dockerDropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dockerDropZone.classList.add('dragover');
});

dockerDropZone.addEventListener('dragleave', () => {
    dockerDropZone.classList.remove('dragover');
});

dockerDropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dockerDropZone.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length) {
        dockerFileInput.files = files;
        dockerFileNameDisplay.textContent = "Fichier sélectionné : " + files[0].name;
    }
});

dockerFileInput.addEventListener('change', () => {
    if (dockerFileInput.files.length) {
        dockerFileNameDisplay.textContent = "Fichier sélectionné : " + dockerFileInput.files[0].name;
    }
});

const composeDropZone = document.getElementById('composeDropZone');
const composeFileInput = document.getElementById('composeFileInput');
const composeFileNameDisplay = document.getElementById('composeFileName');

composeDropZone.addEventListener('click', () => {
    composeFileInput.click();
});

composeDropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    composeDropZone.classList.add('dragover');
});

composeDropZone.addEventListener('dragleave', () => {
    composeDropZone.classList.remove('dragover');
});

composeDropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    composeDropZone.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length) {
        composeFileInput.files = files;
        composeFileNameDisplay.textContent = "Fichier sélectionné : " + files[0].name;
    }
});

composeFileInput.addEventListener('change', () => {
    if (composeFileInput.files.length) {
        composeFileNameDisplay.textContent = "Fichier sélectionné : " + composeFileInput.files[0].name;
    }
});





