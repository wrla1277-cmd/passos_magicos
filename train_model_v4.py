import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, classification_report
import joblib

# 1. Carregar a base unificada
print("Carregando base unificada...")
df = pd.read_csv('dados_unificados.csv')

# 2. Seleção de Features (X) e Target (y)
features = ['IAA', 'IEG', 'IPS', 'IDA', 'IPP', 'IPV', 'IAN']
target = 'Ponto_Virada'

# Garante que só usa linhas onde temos dados numéricos
X = df[features]
y = df[target]

# 3. Divisão Treino e Teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 4. Padronização (Scaler)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Treinamento do Modelo
print("Treinando modelo...")
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train_scaled, y_train)

# 6. Avaliação
y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
roc = roc_auc_score(y_test, y_pred_proba)
print(f"ROC-AUC Score: {roc:.4f}")

# 7. Salvar artefatos
joblib.dump(model, 'model_v4.pkl')
joblib.dump(scaler, 'scaler_v3.pkl') # Mantendo nome v3 ou v4 conforme preferir
print("Modelo e Scaler salvos com sucesso!")