
"""Week 6: local, read-only Flask weather dashboard."""

import argparse
import time

from flask import Flask, jsonify, render_template

from common import load_config, project_path
from storage import Store


def create_app(config_path="config.json"):
    config = load_config(config_path)
    app = Flask(__name__)
    database = project_path(config["database"])

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/latest")
    def latest():
        with Store(database) as store:
            row = store.latest(config["station_id"])

        if row is None:
            return jsonify({
                "status": "unknown",
                "reason": "No observations available",
                "observation": None
            })

        age_seconds = time.time() - row["observed_epoch"]

        if not row.get("valid"):
            status = "invalid"
        elif age_seconds < -5:
            status = "unknown"
        elif age_seconds > 15:
            status = "stale"
        else:
            status = "fresh"

        return jsonify({
            "status": status,
            "age_seconds": round(age_seconds, 1),
            "observation": row
        })

    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.json")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    app = create_app(args.config)

    app.run(
        host="127.0.0.1",
        port=args.port,
        debug=False
    )
