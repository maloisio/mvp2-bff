from flask import Flask, request
from flask_cors import CORS

from ariadne import graphql_sync, make_executable_schema
from ariadne.explorer import ExplorerGraphiQL

from graphql_api.schema import type_defs
from graphql_api.queries import query
from graphql_api.mutations import mutation

app = Flask(__name__)
CORS(app)

schema = make_executable_schema(
    type_defs,
    query,
    mutation
)


@app.get("/")
def home():
    return {
        "service": "healthcare-bff",
        "status": "running"
    }


@app.get("/graphql")
def graphql_playground():
    explorer = ExplorerGraphiQL().html(None)
    return explorer


@app.post("/graphql")
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value={"request": request}
    )

    return result, 200 if success else 400


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5002,
        debug=True
    )