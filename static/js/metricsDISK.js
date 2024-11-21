/// recuperer la valeur et la renvotyer dans la page, la mettre a jour toutes les 10 s
async function updatediskUsage() {
    try {

        // Récupérer les données disk depuis l'API
        const response = await fetch('/admin/metrics/disk'); // Assurez-vous que l'URL est correcte

        // Vérifiez si la réponse est correcte
        if (!response.ok) {
            console.error("Error in response:", response.status, response.statusText);
            return;
        }

        // Convertir la réponse en JSON
        let data = await response.json();
        console.log("Fetched data:", data);

        // Vérifiez si la donnée disk usage est présente
        if (data && data.disk_usage != null) {
            const diskUsage = data.disk_usage; // Extraire l'utilisation disk
            console.log(`disk Usage: ${diskUsage}%`);

            // Mettre à jour le graphique circulaire
            const circle = document.querySelector('#disk-circle');
            const percentageText = document.querySelector('#disk-percent');

            // Mettre à jour stroke-dasharray (valeur utilisée, reste)
            const strokeDasharrayValue = `${diskUsage}, 100`;
            circle.setAttribute('stroke-dasharray', strokeDasharrayValue);

            // Mettre à jour le texte de pourcentage
            percentageText.textContent = `${diskUsage}%`;
        } else {
            console.error("disk usage data not found in the response.");
        }
    } catch (error) {
        console.error("Error fetching disk usage:", error);
    }
}

// Initialisation : Appeler la fonction une première fois
updatediskUsage();

// Répéter toutes les 10 secondes
setInterval(updatediskUsage, 10000);

