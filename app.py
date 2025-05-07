# Import des bibliothèques nécessaires à l'API Flask
from flask import Flask, request, jsonify  # Flask = framework web, request = pour récupérer les données envoyées, jsonify = pour renvoyer du JSON
from flask_cors import CORS  # Pour gérer les problèmes de CORS (Cross-Origin Resource Sharing)
import joblib  # Pour charger des fichiers .pkl (modèle et vectorizer)
import traceback  # Pour afficher les traces d'erreur détaillées

# Initialisation de l'app Flask
app = Flask(__name__)
CORS(app)  # Active CORS pour toutes les routes

# Chargement du modèle XGBoost et du vectorizer préalablement sauvegardés
try:
    model = joblib.load("xgboost_best_model.pkl")  # Charge le modèle d'apprentissage
    vectorizer = joblib.load("tfidf_vectorizer.pkl")  # Charge le transformateur TF-IDF (ou autre)
    print("✅ Modèle et vectorizer chargés avec succès")
except Exception as e:
    print(f"❌ ERREUR lors du chargement du modèle ou du vectorizer: {str(e)}")
    print(traceback.format_exc())
    # On continue pour permettre à Flask de démarrer, mais les prédictions échoueront

@app.route('/predict', methods=['POST'])  # Crée un endpoint "/predict" accessible en POST
def predict():
    try:
        data = request.get_json()  # Récupère les données JSON envoyées dans la requête
        
        # Si aucune donnée n'est reçue
        if not data:
            return jsonify({
                'error': 'No JSON data received',
                'tip': 'Send a POST request with Content-Type: application/json and a JSON body containing a "query" field'
            }), 400
        
        query = data.get('query')  # Extrait la requête SQL envoyée dans la clé 'query'
        
        # Journal pour débogage
        print(f"Received query: {query}")

        # Vérification que la requête est une chaîne de caractères valide
        if not query or not isinstance(query, str):
            return jsonify({'error': 'Invalid input. Expected a SQL string.'}), 400

        # Vérifie que le modèle et le vectorizer ont été chargés correctement
        if 'model' not in globals() or 'vectorizer' not in globals():
            return jsonify({'error': 'Model or vectorizer not loaded. Check server logs.'}), 500

        # Applique le vectorizer à la requête (même transformation que lors de l'entraînement)
        vectorized_input = vectorizer.transform([query])  # Résultat : vecteur numérique compatible avec XGBoost

        # Prédiction de la classe (ex: 0 = safe, 1 = SQLi)
        prediction = int(model.predict(vectorized_input)[0])

        # Récupération des probabilités pour chaque classe
        proba = model.predict_proba(vectorized_input)[0].tolist()

        # Retourne la prédiction au format JSON
        return jsonify({
            'prediction': prediction,
            'probabilities': proba,
            'query': query  # Renvoie la requête pour confirmation
        })

    except Exception as e:
        # En cas d'erreur, renvoie un message d'erreur au format JSON avec la trace
        error_trace = traceback.format_exc()
        print(f"❌ ERROR in /predict: {str(e)}")
        print(error_trace)
        
        return jsonify({
            'error': str(e),
            'trace': error_trace
        }), 500

# Route simple pour vérifier que le serveur est en marche
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'API is running',
        'endpoints': {
            '/predict': 'POST - Predict if a SQL query contains an injection'
        }
    })

# Lancement du serveur Flask en mode debug sur le port 5000
if __name__ == '__main__':
    print("Starting Flask server on http://0.0.0.0:5000")
    print("Use Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)