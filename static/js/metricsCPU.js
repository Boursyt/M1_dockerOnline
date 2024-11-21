async function updateCPUUsage() {
    try {

        // Récupérer les données CPU depuis l'API
        const response = await fetch('/admin/metrics/cpu'); // Assurez-vous que l'URL est correcte

        // Vérifiez si la réponse est correcte
        if (!response.ok) {
            console.error("Error in response:", response.status, response.statusText);
            return;
        }

        // Convertir la réponse en JSON
        let data = await response.json();
        console.log("Fetched data:", data);

        // Vérifiez si la donnée CPU usage est présente
        if (data && data.cpu_usage != null) {
            const cpuUsage = data.cpu_usage; // Extraire l'utilisation CPU
            console.log(`CPU Usage: ${cpuUsage}%`);

            // Mettre à jour le graphique circulaire en utilisant les tag html
            const circle = document.querySelector('#cpu-circle');
            const percentageText = document.querySelector('#cpu-percent');

            // Mettre à jour stroke-dasharray (valeur utilisée, reste)
            const strokeDasharrayValue = `${cpuUsage}, 100`;
            circle.setAttribute('stroke-dasharray', strokeDasharrayValue);

            // Mettre à jour le texte de pourcentage
            percentageText.textContent = `${cpuUsage}%`;
        } else {
            console.error("CPU usage data not found in the response.");
        }
    } catch (error) {
        console.error("Error fetching CPU usage:", error);
    }
}

// Initialisation : Appeler la fonction une première fois
updateCPUUsage();

// Répéter toutes les 10 secondes
setInterval(updateCPUUsage, 10000);
