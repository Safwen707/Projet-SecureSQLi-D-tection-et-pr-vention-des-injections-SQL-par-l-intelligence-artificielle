import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, log_loss, f1_score
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Chargement du dataset équilibré
print("[DEBUG] Chargement du dataset équilibré...")
train_df = pd.read_csv("Processed/train_model_input.csv")
test_df = pd.read_csv("Processed/test_model_input.csv")

X_train = train_df.drop(columns=["Label"]).values
y_train = train_df["Label"].values

X_test = test_df.drop(columns=["Label"]).values
y_test = test_df["Label"].values

print("[INFO] Taille X_train:", X_train.shape)
print("[INFO] Taille X_test:", X_test.shape)

# 2. Définir manuellement les hyperparamètres XGBoost
model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    use_label_encoder=False,
    eval_metric='logloss',
    random_state=42
)

# 3. Entraînement du modèle
print("[DEBUG] Entraînement du modèle XGBoost...")
model.fit(X_train, y_train)

# 4. Évaluation du modèle
print("[DEBUG] Évaluation sur le jeu de test...")
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)

acc_test = accuracy_score(y_test, y_pred)
logloss_test = log_loss(y_test, y_pred_proba)
f1 = f1_score(y_test, y_pred)

print("\n[RESULTATS]")
print(f"Accuracy Test : {acc_test:.4f}")
print(f"Log Loss Test : {logloss_test:.4f}")
print(f"F1-Score Test : {f1:.4f}")
print("\nClassification Report :\n", classification_report(y_test, y_pred))

# 5. Matrice de confusion
conf_matrix = confusion_matrix(y_test, y_pred)
print("\nMatrice de confusion :\n", conf_matrix)

plt.figure(figsize=(6,4))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.title("Matrice de Confusion")
plt.xlabel("Prédiction")
plt.ylabel("Valeur Réelle")
plt.show()

# 6. Sauvegarde du modèle
joblib.dump(model, "xgboost_best_model.pkl")
print("[OK] Modèle sauvegardé sous 'xgboost_best_model.pkl'")
