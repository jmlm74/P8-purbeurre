# P8-purbeurre

# P8 du parcours DA Python d'OpenClassRoom

## Créez une plateforme pour amateurs de Nutella

La startup Pur Beurre, avec laquelle vous avez déjà travaillé, souhaite développer une plateforme web à destination de ses clients. Ce site permettra à quiconque de trouver un substitut sain à un aliment considéré comme "Trop gras, trop sucré, trop salé" (même si nous savons tous que [le gras c’est la vie](https://www.youtube.com/watch?v=x2QBDQXn3iU)).  

### Cahier des charges

Le cahier des charges est disponible en cliquant [sur ce lien](https://s3-eu-west-1.amazonaws.com/course.oc-static.com/projects/DAPython_P8/Cahier_des_charges.zip).  

### Fonctionnalités

 - Affichage du champ de recherche dès la page d’accueil  
 - La recherche ne doit pas s’effectuer en AJAX  
 - Interface responsive  
 - Authentification de l’utilisateur : création de compte en entrant un mail et un mot de passe, sans possibilité de changer son mot de passe pour le moment.  


### Étapes
#### 1 - Planifier votre projet  
Découpez votre projet en étapes et sous-étapes en suivant une méthodologie de projet agile que vous adapterez à vos besoins. Remplissez un tableau Trello ou Pivotal Tracker.  
Avant de coder, initialisez un repo Github et faites votre premier push.  

#### 2 - Créer un nouveau projet Django  
Créez votre projet, modifiez les réglages par défaut et commencez à le développer  fonctionnalité par fonctionnalité. Vous trouverez des indications supplémentaires dans les étapes suivantes sur certaines des fonctionnalités à réaliser.  

#### 3 - La page d’accueil des héros  
Intéressez-vous à la page d’accueil de la plateforme. Vous aurez besoin d’intégrer une librairie externe, Bootstrap, ainsi que jQuery. Structurez bien vos assets !  
Puis créez le contenu HTML et mettez en forme l’ensemble grâce à CSS et ses librairies.  

#### 4 - [Ça c'est mon espace](http://dai.ly/x3kisu?start=28)  
Comment votre utilisateur se crée-t-il un compte ? Certainement grâce à un premier formulaire. Codez donc la page de création de compte ainsi que le formulaire associé. Installez le module nécessaire pour gérer l’authentification avec Django.  
Mettez à jour la barre de menu pour qu’elle affiche une icône “Mon compte” quand l’utilisateur est connecté et une icône “Créer un compte” quand il ne l’est pas.  
Puis créez la page “Mon compte” (voir les esquisses dans le cahier des charges).  

#### 5 - Search but don't destroy  
Ah, la recherche ! Un défi intéressant !  
Commencez par parcourir la documentation de l’[API Open Food Facts](http://en.wiki.openfoodfacts.org/Project:API) et trouvez comment récupérer les informations de l’aliment recherché.  
Puis construisez votre base de données en y intégrant uniquement les éléments nécessaires (le score nutritionnel par exemple).  
Enfin, inventez un algorithme qui va chercher dans votre base de données l’aliment qui a un meilleur score nutritionnel à l’aliment demandé mais qui reste dans la même catégorie. Vous pouvez le faire ! Je crois en vous !  
 - Mettez à jour la page d’accueil et le menu pour que le formulaire de recherche soit effectivement fonctionnel.  
 - Créez la page qui affiche les résultats de recherche.  
 - Puis créez la page détaillant les caractéristiques de l’aliment de substitution.  
À la fin, fêtez cette première fonctionnalité en faisant une pause qui vous fait plaisir (c’est important !).  

##### 6 - Des aliments sains dans un corps sain  
À présent, plongez dans la fonctionnalité qui permet à l’utilisateur d’enregistrer un produit de substitution en favoris. Mettez à jour la page qui affiche les résultats de recherche en ajoutant un bouton sous chaque produit. Puis ajoutez une nouvelle fonctionnalité à Django.  
Créez la page Mes Produits, accessible en cliquant sur la carotte dans le menu.  

#### 7 - Finitions et mise en ligne  
Créez la page Mentions Légales et mettez en ligne votre site en utilisant Heroku.  
….alors, done?  
Well done!  
Sortez prendre l’air et fêter votre nouveau site avec vos amis. ;-)  

## Livrables  
### Principe  
 - L'utilisateur doit être connecté pour utiliser l'outil. Il peut librement se créer un compte.  
 - Les données utilisées proviennent directement de la base  d'Open Food Facts.  
 - L'utilisateur entre un mot qui doit se trouver dans le nom (fournit par Open Food Facts) afin de le rechercher dans la base.  
 - Si le critère match complètement la page des substituts possibles est directement affichée sinon une proposition de produits correspondant à la recherche est proposée avant.  
 - Sur la page des substituts il est possible d'en enregistrer un ou plusieurs en ant que favoris (bookmarks) qui s'afficheront dans la page "détail" du produit ainsi que dans la page des bookmarks de l'utilisateur.  
 - Chaque environnement est isolé (les bokkmarks d'un utilisateur n'appraissent pas dans les environnements des autres utilisateurs).  
### Langages de developpement et outils  
 - python >= 3.8
 - Django >= 3.0
### Liens  
L'application est visible [ici](https://purbeurre-jmlm74.herokuapp.com/).  
La documentation se trouve [à cet endroit](https://mega.nz/folder/sBQi1YAb#uW63w7kxFWON9nroXWrGKw).  
  
### Installation & pré-requis  
#### Pré-requis  
 - Créer un environnement virtuel avec pipenv, virtualenv ou autre et l'activer.  
#### Installation  
 - Télécharger le repo.  
 - Se mettre dans le répertoire du repo et installer les pré-requis avec la commande suivante : 'pip install -r requirements.txt'.  
 - Démarrer votre serveur Django sans oublier les migrations et la création d'un super-user.  
#### Tests unitaires  
 - Faits avec Unittest et Selenium  