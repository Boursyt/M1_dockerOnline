const fileDropZone = document.getElementById('fileDropZone');
const fileInput = document.getElementById('fileInput');
const fileNameDisplay = document.getElementById('fileName');

fileDropZone.addEventListener('click', () => {
   fileInput.click();
});

fileDropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileDropZone.classList.add('dragover');
});

fileDropZone.addEventListener('dragleave', () => {
    fileDropZone.classList.remove('dragover');
});

fileDropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    fileDropZone.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length) {
        fileInput.files = files;
        fileNameDisplay.textContent = "Fichier sélectionné : " + files[0].name;
    }
});

fileInput.addEventListener('change', () => {
    if (fileInput.files.length) {
        fileNameDisplay.textContent = "Fichier sélectionné : " + fileInput.files[0].name;
    }
});