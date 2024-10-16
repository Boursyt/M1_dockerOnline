const toggleSwitch = document.getElementById('theme');

// Vérifie le mode enregistré dans le localStorage
const currentTheme = localStorage.getItem('theme');
if (currentTheme === 'light') {
    document.body.classList.add('light-mode');
    document.body.classList.remove('dark-mode');
    toggleSwitch.checked = true;  // Set the toggle switch to checked
} else {
    document.body.classList.add('dark-mode');
    document.body.classList.remove('light-mode');
    toggleSwitch.checked = false;  // Set the toggle switch to unchecked
}

// Ajoute un écouteur d'événements pour basculer entre les modes
toggleSwitch.addEventListener('change', () => {
    if (toggleSwitch.checked) {
        document.body.classList.add('light-mode');
        document.body.classList.remove('dark-mode');
        localStorage.setItem('theme', 'light');
    } else {
        document.body.classList.add('dark-mode');
        document.body.classList.remove('light-mode');
        localStorage.setItem('theme', 'dark');
    }
});