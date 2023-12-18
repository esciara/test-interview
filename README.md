# Interview test

## Travail à réaliser

### Réutilisation des étapes du pipeline

> Certaines étapes de votre data pipeline pourraient être réutilisées par d’autres data pipelines

Les étapes de transformation sont placées dans leur propre module, et peuvent être réutilisées.

Idem pour les fonctions de lecture et d'écriture de fichiers et de manipulation de fichiers.

### Intégration dans un orchestrateur de jobs

> On suppose que votre travail devra être intégré dans un orchestrateur de jobs (de type DAG) par la
suite, votre code et la structure choisie doivent donc favoriser cette intégration

Les transformations se font par appel de `main.py`. Il peut être adapté, ou même la fonction `_clean_and_load_data_file` peut être rendue publique et appelée directement. 

### Pratiques de développement
> Votre code doit respecter les pratiques que vous mettriez en place dans un cadre professionnel au
sein d’une équipe de plusieurs personnes

#### Organisation du projet
```
├── .github
│   ├── workflows
│   │   └── test.yaml
│   └── dependabot.yml
├── data
│   ├── data_files
│   │   ├── incoming      <= landing zone pour les fichiers bruts
│   │   └── processed     <= fichiers traités
│   ├── datalake
│   │   ├── ingested      <= données ingérées
│   │   └── rejected      <= données rejetées car non conformes/pas traitables
│   └── samples
│       ├── clinical_trials.csv
│       ├── drugs.csv
│       ├── pubmed.csv
│       └── pubmed.json
├── invoke.yaml
├── poetry.lock
├── poetry.toml
├── pyproject.toml
├── README.md
├── src                   <= code source
├── tasks.py
└── tests                 <= tests unitaires
```

#### Pratiques utilisées (non exhaustif et dans le desordre)

- TDD (tests unitaires sur toutes les transformations)
- [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
- CI/CD avec [Github Actions](https://github.com/features/actions)
- Mise à jour des dépendances avec [Dependabot](https://docs.github.com/en/code-security/dependabot)
- Crasfsmanship et clean code => refactoring ; on ne développe pas pour le moment une fonctionnalité qui n'est pas demandée ; etc.
- [semantic-versioning](https://semver.org/) (non utilisé ici) pour le nommage des versions
- [semantic-release](https://semantic-release.gitbook.io/semantic-release/) (non utilisé ici) pour la gestion des versions

#### Outils de développement

- [Poetry](https://python-poetry.org/) pour la gestion des dépendances
- [Invoke](https://www.pyinvoke.org/) pour l'automatisation des tâches (à la place de Makefile)
- [Pytest](https://docs.pytest.org/en/) pour les tests unitaires
- [PyHamcrest](https://pyhamcrest.readthedocs.io/en/latest/) pour les assertions dans les tests unitaires
- [Black](https://black.readthedocs.io/en/stable/) pour le formattage du code
- [Isort](https://pycqa.github.io/isort/) pour le tri des imports
- [Ruff (linter)](https://docs.astral.sh/ruff/linter/) pour la vérification de la qualité du code (à la place de `flake8` et consorts)
- [Mypy](https://mypy.readthedocs.io/en/stable/) pour le typage statique
- [pre-commit](https://pre-commit.com/) (non utilisé ici) pour lancer les outils de développement avant chaque commit
- [tox](https://tox.readthedocs.io/en/latest/) (non utilisé ici) pour lancer les tests unitaires sur plusieurs versions de Python

#### Technologie utilisée

- Python 3.11 (avec retrocompatibilité 3.10) ; j'aurais pu utiliser 3.12, mais la librairie que je voulais utiliser au départ ne le supportait pas encore.
- [Pandas](https://pandas.pydata.org/) pour la manipulation des données