#!/usr/bin/env python3
import argparse
import asyncio
import logging
import sys
from core.scanner import run_scan

def main():
    parser = argparse.ArgumentParser(description="WordPress/WooCommerce Security Scanner")
    parser.add_argument("--url", required=True, help="Target site URL")
    parser.add_argument("--output", help="Output JSON file (optional, prints to stdout if not set)")
    parser.add_argument("--delay", type=float, default=0.5, help="Rate limit delay between requests (seconds)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    report = asyncio.run(run_scan(args.url, args.output, args.delay))
    if report:
        if not args.output:
            import json
            print(json.dumps(report, indent=2))
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()