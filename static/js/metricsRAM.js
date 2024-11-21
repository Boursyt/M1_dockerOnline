async function updateramUsage() {
    try {

        // Récupérer les données ram depuis l'API
        const response = await fetch('/admin/metrics/ram'); // Assurez-vous que l'URL est correcte

        // Vérifiez si la réponse est correcte
        if (!response.ok) {
            console.error("Error in response:", response.status, response.statusText);
            return;
        }

        // Convertir la réponse en JSON
        let data = await response.json();
        console.log("Fetched data:", data);

        // Vérifiez si la donnée ram usage est présente
        if (data && data.ram_usage != null) {
            const ramUsage = data.ram_usage; // Extraire l'utilisation ram
            console.log(`ram Usage: ${ramUsage}%`);

            // Mettre à jour le graphique circulaire
            const circle = document.querySelector('#ram-circle');
            const percentageText = document.querySelector('#ram-percent');

            // Mettre à jour stroke-dasharray (valeur utilisée, reste)
            const strokeDasharrayValue = `${ramUsage}, 100`;
            circle.setAttribute('stroke-dasharray', strokeDasharrayValue);

            // Mettre à jour le texte de pourcentage
            percentageText.textContent = `${ramUsage}%`;
        } else {
            console.error("ram usage data not found in the response.");
        }
    } catch (error) {
        console.error("Error fetching ram usage:", error);
    }
}

// Initialisation : Appeler la fonction une première fois
updateramUsage();

// Répéter toutes les 10 secondes
setInterval(updateramUsage, 10000);
