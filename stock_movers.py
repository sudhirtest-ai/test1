#!/usr/bin/env python3
"""
Top 10 Stock Movers of the Day
Uses Yahoo Finance screener via yfinance — no API key required.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime


def format_large_number(n):
    if n is None or (isinstance(n, float) and pd.isna(n)):
        return "N/A"
    if n >= 1e12:
        return f"${n/1e12:.2f}T"
    if n >= 1e9:
        return f"${n/1e9:.2f}B"
    if n >= 1e6:
        return f"${n/1e6:.2f}M"
    return f"${n:,.0f}"


def fetch_movers(screener_id, count=10):
    result = yf.screen(screener_id, count=count)
    quotes = result.get("quotes", [])
    rows = []
    for q in quotes:
        rows.append({
            "Symbol":   q.get("symbol", ""),
            "Company":  (q.get("longName") or q.get("shortName") or "")[:30],
            "Price":    f"${q.get('regularMarketPrice', 0):.2f}",
            "Change":   f"{q.get('regularMarketChangePercent', 0):+.2f}%",
            "Volume":   f"{q.get('regularMarketVolume', 0):,.0f}",
            "Mkt Cap":  format_large_number(q.get("marketCap")),
        })
    return pd.DataFrame(rows)


def print_table(title, df):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")
    if df.empty:
        print("  No data available (market may be closed).")
        return
    print(df.to_string(index=False))


def main():
    print(f"\nStock Movers — {datetime.now().strftime('%A, %B %d, %Y %I:%M %p')}")

    print_table("TOP 10 GAINERS", fetch_movers("day_gainers"))
    print_table("TOP 10 LOSERS",  fetch_movers("day_losers"))
    print_table("MOST ACTIVE",    fetch_movers("most_actives"))

    print(f"\n{'='*70}")
    print("  Data sourced from Yahoo Finance")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
