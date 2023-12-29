<a name="readme-top"></a>




<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Insiares/9mois">
    <img src="./static/img/9mois.jpg" alt="Logo" width="100" height="80">
  </a>

<h3 align="center">Recherche full text pour l'appli 9 mois à croquer</h3>
<br />

![GitHub tag checks state](https://img.shields.io/github/checks-status/Insiares/9mois/master)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/Insiares/9mois/workflow.yml)

  <p align="center">
    <br />
    <a href="https://github.com/Insiares/9mois/issues">Report Bug</a>
    ·
    <a href="https://github.com/Insiares/9mois/issues">Request Feature</a>
  </p>
</div>






<!-- ABOUT THE PROJECT -->
## A propos


Une solution de recherche de documents par calcul de similarité `fait maison`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python-shield]][Python-url]
* ![sk-learn][scikit-shield]
* ![numpy][NumPy]
* [![flask][flask-shield]][flask-url]
* ![mysql][mysql-shield]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Installation

### Docker Compose

Windows Terminal :

```
set url=mysql+pymysql://<login>:<password>@<ip_or_hostname_or_fqdn>:<port>/<db_name>
```
```
docker-compose up -d --build
```

Linux :

```
docker-compose up -d --build \
-e url=mysql+pymysql://<login>:<password>@<ip_or_hostname_or_fqdn>:<port>/<db_name>
```

### Docker

```
docker run -d -e url=mysql+pymysql://<login>:<password>@<ip_or_hostname_or_fqdn>:<port>/<db_name> -p 5000:5000 ownedge/9mois
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage API

L'API de recherche est connectée à la base de données de l'application et va indéxer son contenu au lancement de l'API.

L'API de recherche offre deux points de terminaisons : 

* `/update` permet de mettre à jour l'indexage lorsque le contenu de la base de données à été modifiée, sans devoir relancer le service.

* `/search` est la route principale permettant d'obtenir la réponse de la recherche. la méthode prends deux arguments : 
  * `query` : contenu de la recherche
  * `table_choices` (facultatif): Sélection des tables dans lesquels effectuer la recherche. S'il -n'est pas fourni, la recherche sera effectuée sur toutes les tables par défaut.

  Le résultat de la recherche est un document sérialisé dont la structure de données est : 
  ```json
  {
  "query": query (str),
  "table": table_choices (str),
  "results": [
    {
                "score": score de similarité (float),
                "document_id": id du document au sein           
                              de la base de données (int),
                "document": contenu du document (str),
                "table": nom de la table contenant le document (str)
    }
            ]
  }
  ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[GPT-shield]:https://img.shields.io/badge/chatGPT-74aa9c?logo=openai&logoColor=white
[GPT-url]:https://openai.com/
[Python-shield]:https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]:https://www.python.org/
[Streamlit-shield]:https://static.streamlit.io/badges/streamlit_badge_black_white.svg
[Streamlit-url]:https://streamlit.io/
[flask-shield]:https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
[mysql-shield]:https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white
[scikit-shield]:https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white
[NumPy]:https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white
[flask-url]: https://flask.palletsprojects.com/en/3.0.x/
[contributors-shield]: https://img.shields.io/github/contributors/Insiares/9mois.svg?style=for-the-badge
[contributors-url]: https://github.com/Insiares/9mois/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Insiares/9mois.svg?style=for-the-badge
[forks-url]: https://github.com/Insiares/9mois/network/members
[stars-shield]: https://img.shields.io/github/stars/Insiares/9mois.svg?style=for-the-badge
[stars-url]: https://github.com/Insiares/9mois/stargazers
[issues-shield]: https://img.shields.io/github/issues/Insiares/9mois.svg?style=for-the-badge
[issues-url]: https://github.com/Insiares/9mois/issues
[license-shield]: https://img.shields.io/github/license/Insiares/9mois.svg?style=for-the-badge
[license-url]: https://github.com/Insiares/9mois/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
