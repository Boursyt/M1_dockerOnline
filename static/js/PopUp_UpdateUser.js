document.querySelectorAll('.mod').forEach(button => {
  button.addEventListener('click', event => {
    const userId = event.target.getAttribute('data-user-id');
    // Récupère les données de l'utilisateur et pré-remplis le formulaire
    // Exemple : fetchUserData(userId).then(data => prefillForm(data));
    document.getElementById('edit-modal').style.display = 'block';

    // Pré-remplir le formulaire avec les données actuelles de l'utilisateur
    document.getElementById('username').value = userId;
    // Ajoute ici le code pour pré-remplir les autres champs
  });
});

document.getElementById('edit-form').addEventListener('submit', event => {
  event.preventDefault();
  const formData = new FormData(event.target);

  fetch(`/admin/user/update/${formData.get('username')}`, {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': getCookie('csrftoken'), // Assure-toi d'inclure le CSRF token
    },
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      // Mets à jour l'affichage ou redirige l'utilisateur
      location.reload();
    } else {
      alert('Erreur lors de la mise à jour de l\'utilisateur.');
    }
  });

  document.getElementById('edit-modal').style.display = 'none';
});

// Fonction pour récupérer le CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
