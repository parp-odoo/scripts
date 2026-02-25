import os
import requests
import time

from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
load_dotenv()

start = time.perf_counter()

user_name = os.getenv("GITHUB_USERNAME")
token = os.getenv("GITHUB_TOKEN")


def get_user_prs(repo):
    url = "https://api.github.com/search/issues"
    query = f"repo:odoo/{repo} type:pr author:{user_name} state:open"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.get(url, headers=headers, params={"q": query})
    response.raise_for_status()
    return response.json().get("items", [])


def get_pr_details(repo, pr_number):
    url = f"https://api.github.com/repos/odoo/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def run_threading_get_all_pr_details(repo, pr_ids):
    results = []
    with ThreadPoolExecutor(max_workers=len(pr_ids)) as executor:
        futures = [
            executor.submit(get_pr_details, repo, pr_id)
            for pr_id in pr_ids
        ]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    return results


def print_dirty_prs(repo):
    user_pr_list = get_user_prs(repo)

    dirty_prs = []

    pr_ids = [pr["number"] for pr in user_pr_list]
    pr_detail_list = run_threading_get_all_pr_details(repo, pr_ids)

    for pr in pr_detail_list:
        if pr.get("mergeable_state") == "dirty":
            dirty_prs.append(pr)

    print(f"\n{repo} : ")
    if not dirty_prs:
        print("✅ No dirty PRs found.")
        return

    print(f"⚠️  Dirty PRs ({len(dirty_prs)} found):")
    for idx, pr in enumerate(dirty_prs, 1):
        print(f"{idx}. {pr.get('title')}")
        print(f"   🔗 {pr.get('html_url')}")
        print(f"   🌿 Branch: {pr.get('head', {}).get('ref')}")


repo_list = ["odoo", "enterprise"]
with ThreadPoolExecutor(max_workers=2) as executor:
    futures = [
        executor.submit(print_dirty_prs, repo)
        for repo in repo_list
    ]
    for future in as_completed(futures):
        result = future.result()

end = time.perf_counter()


print(f"\nTime taken: {end - start:.4f} seconds")
