#!/usr/bin/env python3
"""Подставляет боевые ссылки в plan.json.

    python3 set-links.py <user> <repo> [branch]

По умолчанию ветка main. Скрипт правит plan.json на месте
и печатает первую ссылку, чтобы её можно было сразу проверить.
"""
import json, sys, os

if len(sys.argv) < 3:
    print(__doc__); sys.exit(1)
user, repo = sys.argv[1], sys.argv[2]
branch = sys.argv[3] if len(sys.argv) > 3 else "main"
base = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/fortylove-linkedin"

here = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(here, "plan.json")
plan = json.load(open(path, encoding="utf-8"))

n = 0
for post in plan["posts"]:
    for asset in post["assets"]:
        url = asset["image"]["url"]
        tail = url.split("/fortylove-linkedin/")[-1]
        asset["image"]["url"] = f"{base}/{tail}"
        n += 1

json.dump(plan, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"переписано ссылок: {n}")
print("первая:", plan["posts"][0]["assets"][0]["image"]["url"])
