fc-api
======

Getting Started
---------------

- Change directory into newly created project.

    ```cd fc_api```

- Create a Python virtual environment.

    ```python3 -m venv env```

- Upgrade packaging tools.

    ```env/bin/pip install --upgrade pip setuptools```

- Install the project in editable mode with its testing requirements.

    ```env/bin/pip install -e ".[testing]"```

- Initialize and upgrade the database using Alembic.

    - Generate your first revision.

        ```env/bin/alembic -c development.ini revision --autogenerate -m "init"```

    - Upgrade to that revision.

        ```env/bin/alembic -c development.ini upgrade head```

- Load default data into the database using a script.

    ```env/bin/initialize_fc_api_db development.ini```

- Run project's tests.

    ```env/bin/pytest```

- Run project.

    ```env/bin/pserve development.ini```
