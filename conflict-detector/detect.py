import os
import requests
import time

from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
load_dotenv()

start = time.perf_counter()

user_name = os.getenv("GITHUB_USERNAME")
token = os.getenv("GITHUB_TOKEN")

BASE_URL = "https://api.github.com"

session = requests.Session()
session.headers.update({
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github+json",
})

MAX_RETRIES = 3
THREAD_WORKERS = 10


def request_with_retry(url, params=None):
    for attempt in range(MAX_RETRIES):
        try:
            response = session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == MAX_RETRIES - 1:
                print(f"❌ Request failed: {url} -> {e}")
                return None
            time.sleep(1)


def get_user_prs(repo):
    url = f"{BASE_URL}/search/issues"

    query = f"repo:odoo/{repo} type:pr author:{user_name} state:open"

    data = request_with_retry(url, params={"q": query})
    if not data:
        return []

    return data.get("items", [])


def get_pr_details(repo, pr_number):
    url = f"{BASE_URL}/repos/odoo/{repo}/pulls/{pr_number}"
    return request_with_retry(url)


def run_threading_get_all_pr_details(repo, pr_ids):
    results = []
    with ThreadPoolExecutor(max_workers=min(len(pr_ids), THREAD_WORKERS)) as executor:
        futures = [
            executor.submit(get_pr_details, repo, pr_id)
            for pr_id in pr_ids
        ]
        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception as e:
                print(f"❌ Thread error: {e}")
    return results


def print_dirty_prs(repo):
    user_pr_list = get_user_prs(repo)

    if not user_pr_list:
        print(f"\n{repo}: No PRs found.")
        return
    pr_ids = [pr["number"] for pr in user_pr_list]
    pr_detail_list = run_threading_get_all_pr_details(repo, pr_ids)

    dirty_prs = [
        pr for pr in pr_detail_list
        if pr.get("mergeable_state") == "dirty"
    ]
    print(f"\n{repo}:")

    if not dirty_prs:
        print("✅ No dirty PRs found.")
        return

    print(f"⚠️ Dirty PRs ({len(dirty_prs)} found):")
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
        future.result()

end = time.perf_counter()
print(f"\n⏱ Time taken: {end - start:.4f} seconds")
