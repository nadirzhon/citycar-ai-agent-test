import os
from datetime import datetime, timezone
import requests

BASE_URL = os.environ["AMOCRM_BASE_URL"].rstrip("/")
TOKEN = os.environ["AMOCRM_ACCESS_TOKEN"]
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def get_all(path, params=None):
    response = requests.get(
        f"{BASE_URL}{path}", headers=HEADERS, params=params, timeout=20
    )
    response.raise_for_status()
    return response.json().get("_embedded", {})

def find_problem_deals():
    deals = get_all("/leads", {"limit": 250}).get("leads", [])
    now = datetime.now(timezone.utc).timestamp()
    result = []

    for deal in deals:
        tasks = get_all(
            "/tasks",
            {"filter[entity_type]": "leads",
             "filter[entity_id]": deal["id"],
             "limit": 250},
        ).get("tasks", [])

        overdue = any(
            not task.get("is_completed", False)
            and task.get("complete_till", now + 1) < now
            for task in tasks
        )
        if not tasks or overdue:
            result.append({
                "id": deal["id"],
                "name": deal.get("name"),
                "overdue": overdue,
            })
    return result

if __name__ == "__main__":
    for deal in find_problem_deals():
        print(deal)
