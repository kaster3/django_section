FROM python:3.12

ENV PYTHONBUFFERED=1

WORKDIR app/

RUN pip install -U pip "poetry==1.8.4"
RUN poetry config virtualenvs.create false --local

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY .template.env ./

COPY dbsection/ ./dbsection/

ENV PYTHONPATH=/dbsection

CMD ["python", "dbsection/manager.py", "runserver"]