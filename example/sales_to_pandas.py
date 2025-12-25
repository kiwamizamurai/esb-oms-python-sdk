"""Example: Fetch last month's sales and analyze with pandas.

Usage:
    # Set environment variables
    export ESB_USERNAME="your_username"
    export ESB_PASSWORD="your_password"

    # Run the script
    uv run python example/sales_to_pandas.py
"""

from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta

import pandas as pd

from esb_oms import Environment, ESBClient

# Get credentials from environment
USERNAME = os.environ.get("ESB_USERNAME", "")
PASSWORD = os.environ.get("ESB_PASSWORD", "")


def get_last_month_dates() -> tuple[str, str]:
    """Get first and last day of last month."""
    today = datetime.now(tz=UTC).date()
    first_of_this_month = today.replace(day=1)
    last_of_last_month = first_of_this_month - timedelta(days=1)
    first_of_last_month = last_of_last_month.replace(day=1)
    return first_of_last_month.isoformat(), last_of_last_month.isoformat()


def main() -> None:
    if not USERNAME or not PASSWORD:
        print("Set ESB_USERNAME and ESB_PASSWORD environment variables")
        return

    # Calculate date range
    date_from, date_to = get_last_month_dates()
    print(f"Fetching sales: {date_from} ~ {date_to}")

    # Fetch all pages of sales data
    all_sales = []
    page = 1

    with ESBClient(
        username=USERNAME,
        password=PASSWORD,
        environment=Environment.PRODUCTION,
    ) as client:
        while True:
            sales = client.report.get_sales_information(
                sales_date_from=date_from,
                sales_date_to=date_to,
                page=page,
            )
            if not sales:
                break
            all_sales.extend(sales)
            print(f"  Page {page}: {len(sales)} records")
            page += 1

    if not all_sales:
        print("No sales data found")
        return

    print(f"Total fetched: {len(all_sales)} orders")

    # Convert to DataFrame (order-level, one row per order)
    rows = []
    for sale in all_sales:
        rows.append({
            "sales_num": sale.sales_num,
            "bill_num": sale.bill_num,
            "sales_date": sale.sales_date,
            "sales_date_in": sale.sales_date_in,
            "sales_date_out": sale.sales_date_out,
            "branch_code": sale.branch_code,
            "member_code": sale.member_code,
            "member_name": sale.member_name,
            "visit_purpose_name": sale.visit_purpose_name,
            "pax_total": sale.pax_total,
            "subtotal": float(sale.subtotal),
            "discount_total": float(sale.discount_total),
            "vat_total": float(sale.vat_total),
            "grand_total": float(sale.grand_total),
            "payment_total": float(sale.payment_total),
            "status_name": sale.status_name,
        })

    df = pd.DataFrame(rows)

    # Display results
    print(f"\n=== Orders ({len(df)} records) ===")
    print(df.head(10).to_string(index=False))

    print("\n=== Summary by Status ===")
    print(df.groupby("status_name")["grand_total"].agg(["count", "sum"]))

    print("\n=== Summary by Branch ===")
    branch_summary = df.groupby("branch_code")["grand_total"].agg(["count", "sum"])
    print(branch_summary.sort_values("sum", ascending=False).head(10))

    print(f"\n=== Total Revenue: {df['grand_total'].sum():,.0f} ===")


if __name__ == "__main__":
    main()
