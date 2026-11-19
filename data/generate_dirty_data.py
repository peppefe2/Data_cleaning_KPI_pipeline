from pathlib import Path
import random
import pandas as pd


def generate_orders(n_rows: int = 200, seed: int = 42) -> pd.DataFrame:
    rng = random.Random(seed)
    customers = ["Acme Srl", "Beta SpA", "Gamma Tech", "Delta Logistica", None]
    statuses = ["paid", "PAID", "cancelled", "pending", "refunded"]
    date_formats = ["%Y-%m-%d", "%d/%m/%Y", "2026/99/10"]

    rows = []
    for i in range(1, n_rows + 1):
        order_id = f"ORD-{1000 + i}"
        if rng.random() < 0.08:
            order_id = f" ord-{1000 + rng.randint(1, max(1, i - 1))} "

        base_amount = round(rng.uniform(200, 8000), 2)
        raw_amount = f"{base_amount:,.2f} EUR".replace(",", "X").replace(".", ",").replace("X", ".")
        if rng.random() < 0.07:
            raw_amount = rng.choice(["N/A", "", "-120,00"])

        fmt = rng.choice(date_formats)
        order_date = fmt if "99" in fmt else f"2026-10-{rng.randint(1, 28):02d}"
        if fmt == "%d/%m/%Y":
            order_date = f"{rng.randint(1, 28):02d}/10/2026"

        rows.append({
            "order_id": order_id,
            "customer_name": rng.choice(customers),
            "order_date": order_date,
            "amount_raw": raw_amount,
            "status": rng.choice(statuses),
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    out_path = Path("data/sample/raw_orders.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df = generate_orders()
    df.to_csv(out_path, index=False)
    print(f"Salvato {len(df)} righe in {out_path}")