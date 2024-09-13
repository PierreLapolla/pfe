# PFE-Gaming

## Description

Bon la team vous voyez Solo Leveling? Bah voilà c'est ça mais en mieux.

## Installation

### Requirements

- [Pycharm](https://www.jetbrains.com/pycharm/download/)
- [Docker](https://docs.docker.com/get-docker/) running
- Python environment (strongly recommended but mandatory for LaTeX compilation)

### Setup

1. Clone the repository
2. Rename [.env.template](backend/.env.template) in `backend/` to `.env` and fill in the required fields
3. Rename [.env.template](frontend/.env.template) in `frontend/` to `.env` and fill in the required fields
4. Secrets are on Discord

### Run

1. Open [docker-compose.yml](docker-compose.yml)
2. Click the double green arrow next to `services`
3. See backend documentation at [localhost:8000/docs](http://localhost:8000/docs)
4. See frontend at [localhost:3000](http://localhost:3000)

### LaTeX

```bash
pip install docker
python3 rapport/compile.py
```

## Notes

- See [Shadcn](https://ui.shadcn.com/docs) for possible frontend web development

