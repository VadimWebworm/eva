from flask import Flask, jsonify, request, g
from sentence_transformers import SentenceTransformer
from numpy.linalg import norm
from huggingface_hub.utils._errors import RepositoryNotFoundError


def get_app():
    app = Flask(__name__)
    app.config['MODEL_PATH'] = 'models/ts_model'

    def get_model():
        if 'ts_model' not in g:
            try:
                g.ts_model = SentenceTransformer(app.config['MODEL_PATH'])
            except RepositoryNotFoundError:
                g.ts_model = SentenceTransformer('rubert-base-cased-sentence')
                g.ts_model.save(app.config['MODEL_PATH'])
        return g.ts_model

    @app.route("/", methods=['POST'])
    def do_prediction():
        json = request.get_json()
        s = [json['s1'], json['s2']]
        model = get_model()
        e = model.encode(s)

        score = e[0] @ e[1].T / (norm(e[0]) * norm(e[1]))

        result = {"Similarity": str(score)}
        return jsonify(result)

    return app


if __name__ == "__main__":
    app = get_app()
    app.run(host='0.0.0.0')