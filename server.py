from flask import Flask, jsonify, request
from flask.views import MethodView
from models import Session, Advertisement
from sqlalchemy.exc import IntegrityError

app = Flask("app")


class HttpError(Exception):
    def __init__(self, status_code: int, message: dict | list | str | IntegrityError):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def http_error_handler(error: HttpError):
    error_message = {"status": "error", "description": error.message}
    response = jsonify(error_message)
    response.status_code = error.status_code
    return response


def get_adv(session: Session, adv_id: int):
    adv = session.get(Advertisement, adv_id)
    if adv is None:
        raise HttpError(404, message="advertisement does not exist")
    return adv


class AdvertisementView(MethodView):
    def get(self, adv_id: int):
        with Session() as session:
            adv = get_adv(session, adv_id)
            return jsonify(
                {
                    "id": adv.id,
                    "title": adv.title,
                    "description": adv.description,
                    "creates_at": adv.created_at.isoformat(),
                    "owner": adv.owner,
                }
            )

    def post(self):
        json_data = request.json
        with Session() as session:
            adv = Advertisement(**json_data)
            session.add(adv)
            try:
                session.commit()
            except IntegrityError as error:
                raise HttpError(409, message=error)
            return jsonify({"id": adv.id})

    def patch(self, adv_id: int):
        json_data = request.json
        with Session() as session:
            adv = get_adv(session, adv_id)
            for field, value in json_data.items():
                setattr(adv, field, value)
            session.add(adv)
            try:
                session.commit()
            except IntegrityError as error:
                raise HttpError(409, message=error)
            return jsonify(
                {
                    "id": adv.id,
                    "title": adv.title,
                    "description": adv.description,
                    "creates_at": adv.created_at.isoformat(),
                    "owner": adv.owner,
                }
            )

    def delete(self, adv_id: int):
        with Session() as session:
            adv = get_adv(session, adv_id)
            session.delete(adv)
            session.commit()
            return jsonify({"status": "success"})


app.add_url_rule(
    "/adv/<int:adv_id>",
    view_func=AdvertisementView.as_view("with_adv_id"),
    methods=["GET", "PATCH", "DELETE"],
)

app.add_url_rule(
    "/adv/", view_func=AdvertisementView.as_view("create_adv"), methods=["POST"]
)

if __name__ == "__main__":
    app.run()
