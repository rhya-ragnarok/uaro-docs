"""mkdocs-macros module: renders pet table rows from docs/data/*.yml (test slice: Poring/Mastering only)."""
import yaml
from pathlib import Path

DATA_DIR = Path(__file__).parent / "docs" / "data"


def _load(name):
    return yaml.safe_load((DATA_DIR / f"{name}.yml").read_text())


def _resolve(lookup, ref_id, label):
    if ref_id not in lookup:
        raise KeyError(f"{label} id '{ref_id}' not found in {label}s.yml")
    entry = lookup[ref_id]
    return f"![{entry['name']}](img/{entry['img']}) {entry['name']}"


def define_env(env):
    items = _load("items")
    mobs = _load("mobs")
    pets = _load("pets")

    @env.macro
    def pets_table_test():
        header = (
            "| Pets | Food | Taming Item | Accessory | Equip Bonus | Capture Rates |\n"
            "|---|---|---|---|---|---|"
        )
        rows = []
        for pet in pets.values():
            mob = _resolve(mobs, pet["mob"], "mob")
            food = _resolve(items, pet["food"], "item")
            taming_item = _resolve(items, pet["taming_item"], "item")
            accessory = _resolve(items, pet["accessory"], "item") if pet.get("accessory") else "None"
            bonus = pet["bonus"].get("loyal") or pet["bonus"].get("cordial") or ""
            rows.append(f"| {mob} | {food} | {taming_item} | {accessory} | {bonus} | {pet['capture_rate']} |")
        return "\n".join([header, *rows])
