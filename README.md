# 🏥 Système de Prédiction de Réadmission Médicale

Une application web simple utilisant l'intelligence artificielle pour analyser le risque de réadmission médicale basé sur le texte clinique.

## 🌟 Fonctionnalités

- **Interface web moderne et intuitive** en français
- **Analyse IA en temps réel** du texte clinique
- **Prédiction du risque de réadmission** avec trois niveaux :
  - 🟢 **Risque Faible** (affiché en vert)
  - 🟡 **Risque Moyen** (affiché en orange)
  - 🔴 **Risque Élevé** (affiché en rouge)
- **Analyse détaillée** avec nombre d'indicateurs de complications et de stabilité
- **Interface responsive** qui fonctionne sur mobile et ordinateur

## 🚀 Installation et Utilisation

### Prérequis
- Python 3.7+
- pip (gestionnaire de paquets Python)

### Installation

1. **Cloner ou télécharger le projet**
```bash
git clone <repository-url>
cd readmission-prediction
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Lancer l'application**
```bash
python app.py
```

4. **Ouvrir l'application**
   - Ouvrir votre navigateur web
   - Aller à l'adresse : `http://localhost:5000`

## 🎯 Comment utiliser l'application

1. **Saisir le texte clinique** : Entrez le texte médical du patient dans la zone de texte (diagnostic, évolution clinique, investigations, etc.)

2. **Cliquer sur "Analyser"** : L'IA analyse automatiquement le texte

3. **Voir le résultat** :
   - **Vert** = Risque faible de réadmission
   - **Orange** = Risque moyen de réadmission  
   - **Rouge** = Risque élevé de réadmission

4. **Analyser les détails** : L'application affiche le nombre d'indicateurs de complications vs stabilité détectés

## 🧠 Comment fonctionne l'IA

L'algorithme utilise une approche basée sur l'analyse de mots-clés :

### Indicateurs de Complications
- sepsis, pneumonia, respiratory distress
- cardiac arrest, bleeding, wound infection
- fever, infection, critical, emergency
- Et bien d'autres...

### Indicateurs de Stabilité
- stable, recovered well, no complications
- vitals normal, pain controlled, clean wound
- healing, good, excellent, satisfactory
- Et bien d'autres...

### Calcul du Risque
- **Risque Faible** : ≤ 33% d'indicateurs de complications
- **Risque Moyen** : 34-66% d'indicateurs de complications
- **Risque Élevé** : > 66% d'indicateurs de complications

## 📝 Exemples de Textes

### Risque Faible
```
Patient stable, cicatrisation normale, pas de signes d'infection, 
tolère bien l'alimentation, mobilisation satisfaisante, 
paramètres vitaux normaux.
```

### Risque Élevé
```
Patient présentant des signes de sepsis avec fièvre persistante, 
pneumonie nosocomiale, détresse respiratoire, nécessitant une réintubation.
```

## 🛠️ Architecture Technique

- **Backend** : Flask (Python)
- **Frontend** : HTML5, CSS3, JavaScript vanilla
- **IA** : Algorithme de classification basé sur l'analyse lexicale
- **Déploiement** : Compatible avec tout serveur supportant Python

## 📊 API REST

L'application expose également une API REST pour l'intégration :

```bash
POST /predict
Content-Type: application/json

{
  "text": "Texte clinique du patient..."
}
```

**Réponse :**
```json
{
  "success": true,
  "result": {
    "risk_level": 0,
    "risk_label": "Faible",
    "probability": 0.25,
    "explanation": "Plus d'indicateurs de stabilité...",
    "complication_count": 1,
    "stability_count": 3
  }
}
```

## ⚠️ Avertissement Médical

Cette application est développée à des fins de démonstration et de recherche uniquement. Elle ne doit pas être utilisée pour prendre des décisions médicales réelles sans supervision médicale appropriée. Consultez toujours un professionnel de santé qualifié pour toute décision médicale.

## 🔧 Développement

Pour modifier ou étendre l'application :

1. **Modifier les mots-clés** : Éditer les listes dans `app.py`
2. **Améliorer l'interface** : Modifier `templates/index.html`
3. **Ajuster l'algorithme** : Modifier la méthode `predict_readmission()`

## 📄 Licence

Ce projet est à des fins éducatives et de démonstration.
