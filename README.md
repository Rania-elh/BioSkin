# BioSkin

BioSkin est un site web qui permet aux utilisateurs de générer des recettes de soins cosmétiques maison, personnalisées selon leur type de peau, leurs besoins (acné, hydratation, éclat…) et les ingrédients qu’ils ont déjà chez eux. Le site offre une expérience simple, naturelle et efficace, axée sur la beauté personnalisée et responsable.

---

## Fonctionnalités principales

### Must Have
- Filtrage des recettes selon le **type de peau** ou le **besoin spécifique**.
- Génération de **recettes personnalisées** à partir des **ingrédients disponibles chez l’utilisateur**.
- Système d’**authentification** : création de compte et connexion.
- Enregistrement des **recettes favorites** dans le profil utilisateur.

### Should Have
- Affichage des **bienfaits des ingrédients** dans les recettes.
- **Noter et commenter** les recettes pour guider les autres utilisateurs.

### Could Have
- **Illustration étape par étape** avec des images pour chaque recette.

### Won’t Have
- Aucun diagnostic ou recommandation à caractère **médical**.

---

## Technologies utilisées

### Frontend
	- HTML5 / CSS3
	- JavaScript (Vanilla ou React selon implémentation)
- Responsive Design (mobile first)

### Backend
	- Node.js avec Express *(ou Flask si Python choisi)*
	- API RESTful

### Base de données
- MySQL (MariaDB)

	---

## Structure du projet

	```plaintext
	bioskin/
	│
	├── backend/          → Fichiers serveur, logique API
	├── frontend/         → Pages web, scripts, styles
	├── database/         → Script de création de BDD et tables
	├── README.md         → Ce fichier
	└── .gitignore
