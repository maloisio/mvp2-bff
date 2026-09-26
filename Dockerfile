FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip show ariadne
RUN pip show graphql-core
RUN python -c "import graphql; print(graphql.__file__); print(getattr(graphql, '__version__', 'sem versão'))"
RUN python -c "from graphql.type import GraphQLSchema; print('GRAPHQL OK')"

COPY . .

EXPOSE 5002

CMD ["python", "app.py"]