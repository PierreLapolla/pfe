# PFE-Gaming

## Jeu Mobile Action-RPG Basé sur les Activités Physiques

### Comment concevoir un jeu mobile action-RPG qui intègre de manière fluide les activités physiques et les données de sommeil du joueur pour influencer le gameplay, tout en offrant une expérience de jeu captivante et motivante ?

Les jeux vidéo mobiles connaissent une popularité croissante avec plus de 2,7 milliards de joueurs dans le monde en 2023.
Les jeux de rôle action (Action-RPG) sont particulièrement prisés pour leur gameplay dynamique et immersif.
Parallèlement, le suivi des activités physiques et des cycles de sommeil est devenu une tendance importante avec
l'adoption massive de montres connectées et d'applications de bien-être.
Associer le gameplay à la vie réelle du joueur en utilisant ses données de santé et de bien-être ouvre la voie à une
expérience ludique unique et motivante.
En intégrant l’activité physique et les données de sommeil, ce jeu pourrait proposer une progression personnalisée en
fonction des efforts réels du joueur, l’incitant à adopter un mode de vie plus sain.

## Installation

### Requirements

- [Pycharm](https://www.jetbrains.com/pycharm/download/)
- [Docker](https://docs.docker.com/get-docker/) running
- Python environment (strongly recommended)

### Setup

1. Clone the repository
2. Rename [.env.template](backend/.env.template) in `backend/` to `.env` and fill in the required fields
3. Rename [.env.template](frontend/.env.template) in `frontend/` to `.env` and fill in the required fields
4. Copy the secrets (firebase credentials) from Discord to `backend/`
5. (Optional) Install the Python dependencies:
    ```bash
    pip install -r backend/requirements.txt
    pip install -r frontend/requirements.txt
    pip install locust
    ```

### Run

1. Open [docker-compose.yml](docker-compose.yml)
2. Click the double green arrow next to `services`
3. [localhost:8000/docs](http://localhost:8000/docs): Backend documentation
4. [localhost:3000](http://localhost:3000): Frontend
5. [localhost:3001](http://localhost:3001): Grafana
6. See other services from [docker-compose.yml](docker-compose.yml) at their respective ports

### LaTeX

Ask Pedro

## Notes

- See [Shadcn](https://ui.shadcn.com/docs) for possible frontend web development

