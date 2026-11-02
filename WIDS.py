import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

normal_file = r"C:\Users\abuya\Downloads\Deauth_0.csv"
deauth_file = r"C:\Users\abuya\Downloads\Deauth_1-selected-columns.csv"

df_normal = pd.read_csv(normal_file, low_memory=False)
df_deauth = pd.read_csv(deauth_file, low_memory=False)

# Explicitly tag them: 0 = Normal, 1 = Deauth Attack
df_normal["Binary_Label"] = 0
df_deauth["Binary_Label"] = 1

# Combine both files into a single dataset
df = pd.concat([df_normal, df_deauth], ignore_index=True)
print(f"Combined dataset shape: {df.shape}")

# Numeric features common to both files
common_numeric = list(
    set(df_normal.select_dtypes(include=[np.number]).columns).intersection(
        set(df_deauth.select_dtypes(include=[np.number]).columns)
    )
)

features = ["frame.len", "frame.time_delta", "frame.time_delta_displayed"]
print(f"Features selected for model: {features}")

print(f"Features selected for model: {features}")

# Clean data
df_clean = df[features + ["Binary_Label"]].dropna()
X = df_clean[features]
y = df_clean["Binary_Label"]

print(f"Class Distribution:\n{y.value_counts()}")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

clf = RandomForestClassifier(n_estimators=50, random_state=42)
clf.fit(X_train, y_train)

print("\nModel Evaluation and Results")
y_pred = clf.predict(X_test)

acc = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

print(f"Model Accuracy: {acc * 100:.2f}%\n")
print("Confusion Matrix:")
print(cm)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nSimulating WIPS Automated Block Action")

def simulate_wips(incoming_stream, model):
  predictions = model.predict(incoming_stream)
  for idx, pred in enumerate(predictions):
    if pred == 1:
      print(
          f"[WIPS ALERT] Packet index {idx}: Malicious Deauth Flood detected!"
          " -> Action: Logged event & Blocked offending MAC address."
      )
    else:
      print(f"[Normal] Packet index {idx}: Traffic is safe.")

simulate_wips(X_test.head(3), clf)