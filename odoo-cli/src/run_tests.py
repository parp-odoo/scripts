import argparse

from server import run_tests


def main():
    parser = argparse.ArgumentParser(description="Run Odoo tests and remember the last test tags.")
    parser.add_argument("test_tags", nargs="?", help="Odoo test selector; defaults to the saved test tags")
    args = parser.parse_args()
    result = run_tests(args.test_tags)
    return 1 if result is False else result


if __name__ == "__main__":
    raise SystemExit(main())
