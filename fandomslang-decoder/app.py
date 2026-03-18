from __future__ import annotations

import os
from typing import List

from flask import Flask, redirect, render_template, request, url_for

from ai_client import DecodedItem, decode_slang
from presets import FandomPreset, all_presets, get_preset


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("FANDOMSLANG_SECRET_KEY", "dev-secret-key")

    @app.context_processor
    def inject_presets() -> dict:
        return {"PRESETS": all_presets()}

    @app.route("/", methods=["GET"])
    def index():
        fandom_key = request.args.get("fandom") or "general"
        preset: FandomPreset = get_preset(fandom_key)
        return render_template(
            "index.html",
            fandom_key=fandom_key,
            preset=preset,
            decoded_items=[],
            original_inputs=["", "", ""],
            error_message=None,
        )

    @app.route("/decode", methods=["POST"])
    def decode():
        fandom_key = request.form.get("fandom") or "general"
        preset: FandomPreset = get_preset(fandom_key)

        texts: List[str] = [
            request.form.get("text1", ""),
            request.form.get("text2", ""),
            request.form.get("text3", ""),
        ]

        non_empty = [t for t in texts if t and t.strip()]
        if not non_empty:
            return redirect(url_for("index", fandom=fandom_key))

        error_message = None
        decoded_items: List[DecodedItem] = []
        try:
            decoded_items = decode_slang(texts, fandom_key=fandom_key)
        except Exception as exc:  # pragma: no cover - defensive
            error_message = (
                "Something went wrong while contacting the AI backend. "
                "Please try again in a moment."
            )
            # In a real app, log the exception; here we keep it simple.
            print(f"Decode error: {exc}")  # noqa: T201

        return render_template(
            "index.html",
            fandom_key=fandom_key,
            preset=preset,
            decoded_items=decoded_items,
            original_inputs=texts,
            error_message=error_message,
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)

