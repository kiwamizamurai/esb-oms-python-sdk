"""Example: Fetch sales payment summary.

Usage:
    # Set environment variables
    export ESB_USERNAME="your_username"
    export ESB_PASSWORD="your_password"

    # Run the script
    uv run python example/sales_payment_summary.py
"""

from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta

from esb_oms import Environment, ESBClient

# Get credentials from environment
USERNAME = os.environ.get("ESB_USERNAME", "")
PASSWORD = os.environ.get("ESB_PASSWORD", "")


def get_yesterday() -> str:
    """Get yesterday's date."""
    today = datetime.now(tz=UTC).date()
    yesterday = today - timedelta(days=1)
    return yesterday.isoformat()


def main() -> None:
    if not USERNAME or not PASSWORD:
        print("Set ESB_USERNAME and ESB_PASSWORD environment variables")
        return

    # Calculate date
    sales_date = get_yesterday()
    print(f"Fetching sales payment summary for: {sales_date}")

    with ESBClient(
        username=USERNAME,
        password=PASSWORD,
        environment=Environment.PRODUCTION,
    ) as client:
        summaries = client.report.get_sales_payment_summary(
            sales_date=sales_date,
        )

    if not summaries:
        print("No payment summary data found")
        return

    print(f"\n=== Payment Summary ({len(summaries)} branches) ===")

    total_amount = 0.0
    total_count = 0

    for summary in summaries:
        print(f"\nBranch: {summary.branch_name} ({summary.branch_code})")
        print(f"Date: {summary.sales_date}")
        print("-" * 60)
        print(f"{ 'Payment Method':<30} | {'Count':>8} | {'Amount':>12}")
        print("-" * 60)

        branch_total = 0.0
        branch_count = 0

        for payment in summary.payments:
            print(
                f"{payment.payment_method_name:<30} | "
                f"{payment.payment_count:>8} | "
                f"{payment.payment_amount:>12,.2f}"
            )
            branch_total += float(payment.payment_amount)
            branch_count += payment.payment_count

        print("-" * 60)
        print(
            f"{ 'TOTAL':<30} | "
            f"{branch_count:>8} | "
            f"{branch_total:>12,.2f}"
        )

        total_amount += branch_total
        total_count += branch_count

    print("\n=== Grand Total ===")
    print(f"Total Transactions: {total_count}")
    print(f"Total Amount:       {total_amount:,.2f}")


if __name__ == "__main__":
    main()
