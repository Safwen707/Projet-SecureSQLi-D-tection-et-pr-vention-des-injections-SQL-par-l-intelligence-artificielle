// api.js - Module pour la détection d'injections SQL
export const predictSQLi = async (sqlQuery) => {
    console.log("predictSQLi appelé avec:", sqlQuery);
    
    try {
      // URL correcte vers le serveur Flask qui tourne sur le port 5000
      const apiUrl = 'http://localhost:5000/predict';
      console.log("Envoi de la requête à:", apiUrl);
 
      // 📤 Envoyer la requête POST
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: sqlQuery,  // On envoie la requête SQL comme une chaîne dans la clé 'query'
        }),
        // Add timeout to avoid hanging requests
        signal: AbortSignal.timeout(10000) // 10 seconds timeout
      });
      
      console.log("Statut de la réponse:", response.status);
  
      // ✅ Vérifier les erreurs
      if (!response.ok) {
        const errorText = await response.text();
        console.error("Réponse d'erreur:", errorText);
        throw new Error(`API request failed with status ${response.status}: ${errorText}`);
      }
  
      // ✅ Extraire les données JSON de la réponse
      const data = await response.json();
      console.log("Données reçues:", data);
  
      return {
        prediction: data.prediction,      // Classe prédite : 0 (safe) ou 1 (SQLi)
        probabilities: data.probabilities // Probabilité pour chaque classe
      };
  
    } catch (error) {
      console.error('Error calling prediction API:', error);
      // Check if it's a connection error and provide a more specific message
      if (error.message.includes('Failed to fetch') || 
          error.name === 'AbortError' ||
          error.message.includes('NetworkError')) {
        throw new Error('Impossible de se connecter au serveur de prédiction (Flask). Assurez-vous que le serveur Python est en cours d\'exécution sur le port 5000.');
      }
      throw error;
    }
};