from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List

from openai import OpenAI

from presets import FandomPreset, get_preset


@dataclass
class DecodedItem:
    original: str
    decoded: str
    glossary: List[Dict[str, str]]


MODEL_DEFAULT = os.getenv("FANDOMSLANG_MODEL", "gpt-4.1-mini")

_client = OpenAI()


def _build_system_message(preset: FandomPreset) -> str:
    return (
        "You are FandomSlang Decoder, an assistant that translates niche fandom slang, memes, "
        "ship names and in-jokes into clear, plain English for newcomers.\n\n"
        "Goals:\n"
        "- Preserve the basic sentiment and enthusiasm of the original.\n"
        "- Remove unexplained jargon and explain slang in simple language.\n"
        "- Be inclusive and avoid offensive phrasing; soften or neutralise harsh slang when needed.\n\n"
        f"Fandom context: {preset.description}\n"
        f"Helpful hints for slang and concepts in this fandom:\n{preset.prompt_hints}\n\n"
        "Always respond ONLY with a single JSON object that matches the requested schema, "
        "with no extra commentary or markdown."
    )


def _build_user_message(texts: List[str]) -> str:
    schema_example = {
        "items": [
            {
                "original": "original fandom text here",
                "decoded": "plain English explanation here",
                "glossary": [
                    {"term": "rizz", "definition": "charisma / ability to flirt"}
                ],
            }
        ]
    }
    payload = {
        "instructions": (
            "Decode each input into plain English for a newcomer. "
            "If there is no slang, still restate it clearly but concisely.\n"
            "- Keep decoded text readable and natural-sounding.\n"
            "- Populate the glossary with any slang, memes, acronyms, ships, or references that might confuse a newcomer.\n"
            "- The glossary should be short, friendly explanations, not dictionary entries.\n"
        ),
        "inputs": texts,
        "response_schema_example": schema_example,
    }
    return json.dumps(payload, ensure_ascii=False)


def _safe_parse_json(content: str) -> Dict[str, Any]:
    """
    Try to parse JSON even if the model surrounds it with text.
    """
    content = content.strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Try to extract the first JSON object in the string
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(content[start : end + 1])
            except json.JSONDecodeError:
                pass
    # Fallback: wrap as a minimal structure
    return {
        "items": [
            {
                "original": "",
                "decoded": content,
                "glossary": [],
            }
        ]
    }


def decode_slang(
    texts: List[str],
    fandom_key: str,
    model: str | None = None,
) -> List[DecodedItem]:
    """
    Call the OpenAI API to decode up to 3 fandom texts.
    """
    # Filter out completely empty inputs but preserve order of non-empty texts
    clean_texts = [t for t in texts if t and t.strip()]
    if not clean_texts:
        return []

    preset = get_preset(fandom_key)
    system_message = _build_system_message(preset)
    user_message = _build_user_message(clean_texts)

    resp = _client.chat.completions.create(
        model=model or MODEL_DEFAULT,
        messages=[
            {"role": "system", "content": system_message},
            {
                "role": "user",
                "content": (
                    "Follow the instructions in this JSON payload and return ONLY the JSON response:\n"
                    f"{user_message}"
                ),
            },
        ],
        temperature=0.4,
    )

    content = resp.choices[0].message.content or ""
    parsed = _safe_parse_json(content)
    items_raw = parsed.get("items") or []

    decoded_items: List[DecodedItem] = []
    for idx, original in enumerate(clean_texts):
        item_data: Dict[str, Any] = {}
        if isinstance(items_raw, list) and idx < len(items_raw):
            maybe = items_raw[idx]
            if isinstance(maybe, dict):
                item_data = maybe

        decoded_text = item_data.get("decoded") or item_data.get("explanation") or original
        glossary_raw = item_data.get("glossary") or []

        glossary: List[Dict[str, str]] = []
        if isinstance(glossary_raw, list):
            for g in glossary_raw:
                if not isinstance(g, dict):
                    continue
                term = str(g.get("term") or "").strip()
                definition = str(g.get("definition") or "").strip()
                if term and definition:
                    glossary.append({"term": term, "definition": definition})

        decoded_items.append(
            DecodedItem(
                original=original,
                decoded=str(decoded_text),
                glossary=glossary,
            )
        )

    return decoded_items

