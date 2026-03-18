from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class FandomPreset:
    key: str
    label: str
    description: str
    prompt_hints: str


PRESETS: Dict[str, FandomPreset] = {
    "general": FandomPreset(
        key="general",
        label="General Internet",
        description=(
            "General online fandom / social media slang across TikTok, Twitter, Discord, "
            "and comment sections."
        ),
        prompt_hints=(
            "Common slang includes: slaps (very good), mid (average), rizz (charisma / flirt ability), "
            "ship (to support a romantic pairing), OTP (one true pairing), lowkey / highkey, canon, "
            "headcanon, crackship, angst, comfort character, main, side character, filler, spoiler."
        ),
    ),
    "anime": FandomPreset(
        key="anime",
        label="Anime / Manga",
        description="Anime, manga and light novel fandom slang and tropes.",
        prompt_hints=(
            "Recognise terms like: isekai, shonen, seinen, waifu, husbando, MC (main character), "
            "OP (opening theme or overpowered depending on context), ED (ending theme), tsundere, "
            "yandere, canon, filler, arc, season, ship, OTP, AU (alternate universe)."
        ),
    ),
    "kpop": FandomPreset(
        key="kpop",
        label="K‑pop",
        description="K‑pop stan culture, groups, comebacks and fandom slang.",
        prompt_hints=(
            "Recognise terms like: stan (enthusiastic fan), bias, bias wrecker, maknae (youngest member), "
            "line distribution, comeback, title track, b‑side, fanchant, lightstick, selca, "
            "era, stage, fancam, main vocal, main dancer, visual."
        ),
    ),
    "marvel": FandomPreset(
        key="marvel",
        label="Marvel / MCU",
        description="Marvel comics and MCU movie/TV fandom slang and meta discussion.",
        prompt_hints=(
            "Recognise terms like: MCU, multiverse, variant, retcon, canon, post‑credit scene, "
            "Easter egg, Phase 1/2/3/4, soft reboot, ship names made from character name blends "
            "(e.g., 'Stucky' for Steve/Bucky)."
        ),
    ),
    "star_wars": FandomPreset(
        key="star_wars",
        label="Star Wars",
        description="Star Wars movies, shows, books and game fandom slang.",
        prompt_hints=(
            "Recognise terms like: Jedi, Sith, Padawan, Order 66, canon vs Legends, the prequels, "
            "the sequels, the Original Trilogy, the Clone Wars, the High Republic, dark side, "
            "light side, chosen one, ship names, AU (alternate universe)."
        ),
    ),
    "gaming": FandomPreset(
        key="gaming",
        label="Gaming",
        description="Video game fandom, esports, MMO and competitive meta slang.",
        prompt_hints=(
            "Recognise terms like: meta, OP (overpowered), nerf, buff, strat (strategy), "
            "build, comp (team composition), GG, tilt, one‑shot, DPS, tank, healer, AFK, "
            "grind, RNG, patch, ranked, queue, main (primary character played)."
        ),
    ),
    "tv_western": FandomPreset(
        key="tv_western",
        label="Western TV / Streaming",
        description="Western TV shows, streaming dramas and general series fandom.",
        prompt_hints=(
            "Recognise terms like: season, episode, mid‑season finale, ship, slow burn, "
            "love triangle, cliffhanger, filler episode, monster‑of‑the‑week, ensemble cast, "
            "showrunner, canon vs fanon."
        ),
    ),
}


def get_preset(key: str) -> FandomPreset:
    """
    Return the preset for a given key, defaulting to the general preset.
    """
    return PRESETS.get(key) or PRESETS["general"]


def all_presets() -> Dict[str, FandomPreset]:
    """
    Convenience helper for templates and forms.
    """
    return PRESETS

