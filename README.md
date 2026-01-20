# AttVidsScraper - Video Extraction API

**AttVidsScraper** est une API Flask robuste conçue pour l'extraction de flux vidéo (HLS/MP4) à partir de diverses plateformes comme Voe, Vidoza, Doodstream, Vidmoly, VK, Callistanise et Embed4me. Elle intègre un système de proxy dynamique pour contourner les restrictions IP et les blocages CORS.

---

## 🚀 Installation et Configuration

### 1. Cloner le projet

```bash
git clone [https://github.com/AttD7/AttVidsScraper.git](https://github.com/AttD7/AttVidsScraper.git)
cd AttVidsScraper
```

### 2. Créer l'environnement virtuel (Recommandé)

Pour isoler les dépendances et éviter les conflits système :

```bash
python -m venv venv
# Activer l'environnement (Windows)
.\venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration de Playwright

Indispensable pour l'extraction basée sur le rendu du navigateur (Vidmoly, VK) :

```bash
playwright install chromium
```

### 🛠️ Démarrage du serveur

Pour lancer l'API en mode développement :

```bash
python app.py
```

Le serveur sera accessible par défaut sur : http://localhost:8888

---

### 📖 Documentation de l'API

L'API expose les points de terminaison suivants pour l'extraction de liens vidéo.

#### 🎥 Points d'accès d'extraction

| Endpoint          | available & working  | Méthode  | Paramètre |                                    Description                                        |
| :---------------- | :------------------: | :------: | --------: | ------------------------------------------------------------------------------------: |
| /vidmoly          |          ✅          |   GET    |    url    | Extraction HLS via Playwright.                                                        |
| /callistanise     |          ✅          |   GET    |    url    | Extraction HLS (Callistanise, Smoothpre, Dingtezuni, Movearnpre, Minochinos, etc...). |
| /embed4me         |          ✅          |   GET    |    id     | Extraction pour Embed4me / Lplayer via ID.                                            |
| /vk               |          ✅          |   GET    |    url    | Extraction VK (oid & id) limitée à 720p.                                              |
| /vidoza           |          ✅          |   GET    |    url    | Extraction pour vidoza / via url.                                                     |
| /voe              |          ✅          |   GET    |    url    | Extraction pour vode / via url.                                                       |
| /doodstream       |          ✅          |   GET    |    url    | Extraction pour doodstream / via url et d0000d.                                       |
| /sendvid          |          ❌          |   GET    |    url    | To do (in coming soon)                                                                |
| /sibnet           |          ❌          |   GET    |    url    | To do (in coming soon)                                                                |


---

### 🔍 Détails des Endpoints

#### 1. Vidmoly

- **Description** : Extraction HLS pour Vidmoly via Playwright.
- **Embed URL Exemple** : https://vidmoly.net/embed-v7ad0oiawrdv.html
- **Exemple** : http://localhost:8888/vidmoly?url=https://vidmoly.net/embed-v7ad0oiawrdv.html
- **Retour attendu** :

```bash
# JSON

  {
    "source": "http://localhost:8888/vidmoly-proxy?url=https%3A//prx-1351.online/.../master.m3u8",
    "status": "success"
  }
```

#### 2. Callistanise (earnvids.com) 

- **Domaines alternatifs** : Callistanise.com, Smoothpre.com, Dingtezuni.com, Movearnpre.com, Minochinos.com, etc...
- **Description** : Extraction HLS pour Callistanise via Requests.
- **Embed URL Exemple** : https://dingtezuni.com/embed/fdbfypeipkyc
- **Exemple** : http://localhost:8888/callistanise?url=https://dingtezuni.com/embed/fdbfypeipkyc
- **Retour attendu** :

```bash
# JSON

  {
    "source": "http://localhost:8888/callistanise-proxy?url=https%3A//.../master.txt",
    "status": "success"
  }
```

#### 3. Embed4me (Lplayer) 

- **Description** : Extraction pour Embed4me / Lplayer via ID.
- **Embed URL Exemple** : https://lpayer.embed4me.com/#xv8jw
- **Exemple** : http://localhost:8888/embed4me?id=xv8jw
- **Retour attendu** :

```bash
# JSON

  {
    "ip_source": "http://localhost:8888/embed4me-proxy?url=https%3A//185.237.106.184/...",
    "source": "http://localhost:8888/embed4me-proxy?url=https%3A//s6d.servicecatalog.site/...",
    "status": "success"
  }
```

#### 4. VK Video 

- **Description** : Extraction pour VK / VK Video Player via id et oid.
- **Embed URL Exemple** : https://vk.com/video_ext.php?oid=755747641&id=456240670
- **Exemple** : http://localhost:8888/vk?url=https://vk.com/video_ext.php?oid=755747641&id=456240670
- **Spécificité** : Filtre automatiquement la qualité pour ne pas dépasser le 720p.
- **Retour attendu** :

```bash
# JSON

  {
    "source": "http://localhost:8888/vk-proxy?url=https%3A//vkvd423.okcdn.ru/%3FsrcIp%3D...",
    "status": "success"
  }
```

#### 5. Vidoza 

- **Description** : Extraction pour vidoza via url.
- **Embed URL Exemple** : https://videzz.net/embed-9b6zbu7135u0.html
- **Exemple** : http://localhost:8888/vidoza?url=https://videzz.net/embed-9b6zbu7135u0.html
- **Retour attendu** :

```bash
# JSON

  {
    "source": "http://localhost:8888/vidoza-proxy?url=https%3A//str41.vidoza.net/vod/v2/nv...",
    "status": "success"
  }
```

#### 6. Voe

- **Description** : Extraction pour voe / via url.
- **Embed URL Exemple** : https://voe.sx/e/llwq1wy1qfye
- **Exemple** : http://localhost:8888/voe?url=https://voe.sx/e/llwq1wy1qfye
- **Retour attendu** :

```bash
# JSON

  {
    "source": "http://localhost:8888/voe-proxy?url=https%3A//cdn-e4srqqyuolvqfr5r.edgeon-bandwidth.com/engine/download/01/1593...",
    "status": "success"
  }
```

#### 7. Doodstream / D000D

- **Description** : Extraction pour doodstream / via url et d0000d.
- **Embed URL Exemple** : https://d0000d.com/e/x84gtg15zdr0
- **Exemple** : http://localhost:8888/doodstream?url=https://d0000d.com/e/x84gtg15zdr0
- **Retour attendu** :

```bash
# JSON

  {
    "source": "http://localhost:8888/doodstream-proxy?url=https%3A//ior159p.cloudatacdn...",
    "status": "success"
  }
```

#### 8. Sendvid Video

- **Description** : To do (in coming soon).

#### 9. Sibnet Video

- **Description** : To do (in coming soon).

---

### 🛡️ Gestion des Proxies

Tous les proxies (/doodstream-proxy, /vidoza-proxy, /voe-proxy, /vk-proxy, /callistanise-proxy, /embed4me-proxy) acceptent un paramètre `url` encodé et retournent le flux vidéo ou le fichier m3u8 réécrit.

- **Paramètre** : `url` (String, Required).
- **Fonction** : Réécrit les fichiers  `MPD|.m3u8` à la volée pour que les segments `.mp4|.ts` passent par le serveur, contournant ainsi les blocages de domaine et les restrictions CORS.
- **Exemple** : http://localhost:8888/embed4me-proxy?url=https%3A//s6d.servicecatalog.site/v4/ck/xv8jw/cf-master.txt
- **Retour** : Flux binaire `video|mp2t`, `texte|M3U8` ou fichier vidéo direct `DASH|MP4`.

---

### ⚠️Notes importantes

- **Qualité Vidéo** : L'extraction VK est plafonnée à la qualité 720p maximum pour optimiser la bande passante et assurer la compatibilité.
- **Playwright Stealth** : Le moteur utilise `playwright-stealth` pour éviter la détection par les systèmes anti-bot lors du rendu des pages.
- **Déploiement** : Pour une mise en production, il est fortement recommandé d'utiliser un serveur WSGI comme `gunicorn` ou `uvicorn`.

---
Développé avec ❤️ pour l'extraction de contenu multimédia.
