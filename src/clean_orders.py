from pathlib import Path
import re
import pandas as pd


def parse_euro_amount(raw_val: object) -> float | None:
    if raw_val is None or pd.isna(raw_val):
        return None
    s = str(raw_val).strip()
    if not s or s.upper() in {"N/A", "NA", "NULL", "NONE", "-"}:
        return None
    s = re.sub(r"[^\d,.\-]", "", s)
    if not s:
        return None
    # Formato europeo tipico: 1.234,56 -> 1234.56
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def parse_order_date(raw_val: object) -> pd.Timestamp | pd.NaT:
    if raw_val is None or pd.isna(raw_val):
        return pd.NaT
    s = str(raw_val).strip()
    if not s:
        return pd.NaT
    # Prova prima YYYY-MM-DD, poi DD/MM/YYYY
    dt = pd.to_datetime(s, format="%Y-%m-%d", errors="coerce")
    if pd.isna(dt):
        dt = pd.to_datetime(s, format="%d/%m/%Y", errors="coerce")
    return dt


def clean_orders(input_path: Path, clean_out: Path, rejected_out: Path) -> None:
    df = pd.read_csv(input_path)

    df["order_id_clean"] = df["order_id"].astype(str).str.strip().str.upper()
    df["customer_clean"] = (
        df["customer_name"]
        .fillna("UNKNOWN_CUSTOMER")
        .astype(str)
        .str.strip()
        .replace("", "UNKNOWN_CUSTOMER")
    )
    df["status_clean"] = df["status"].astype(str).str.strip().str.lower()
    df["order_date_clean"] = df["order_date"].apply(parse_order_date)
    df["amount_clean"] = df["amount_raw"].apply(parse_euro_amount)

    # Identifica duplicati su order_id_clean (mantiene la prima occorrenza)
    is_duplicate = df.duplicated(subset=["order_id_clean"], keep="first")

    reasons = []
    for idx, row in df.iterrows():
        row_reasons = []
        if not row["order_id_clean"] or row["order_id_clean"] == "NAN":
            row_reasons.append("missing_order_id")
        if is_duplicate.loc[idx]:
            row_reasons.append("duplicate_order_id")
        if pd.isna(row["order_date_clean"]):
            row_reasons.append("invalid_order_date")
        if row["amount_clean"] is None or pd.isna(row["amount_clean"]):
            row_reasons.append("unparseable_amount")
        elif row["amount_clean"] < 0:
            row_reasons.append("negative_amount")
        reasons.append(";".join(row_reasons))

    df["reject_reason"] = reasons

    rejected_df = df[df["reject_reason"] != ""].copy()
    valid_df = df[df["reject_reason"] == ""].copy()

    valid_out = valid_df[[
        "order_id_clean",
        "customer_clean",
        "order_date_clean",
        "amount_clean",
        "status_clean",
    ]].rename(columns={
        "order_id_clean": "order_id",
        "customer_clean": "customer_name",
        "order_date_clean": "order_date",
        "amount_clean": "amount",
        "status_clean": "status",
    })

    clean_out.parent.mkdir(parents=True, exist_ok=True)
    rejected_out.parent.mkdir(parents=True, exist_ok=True)

    valid_out.to_csv(clean_out, index=False)
    rejected_df.to_csv(rejected_out, index=False)

    print(f"Righe totali: {len(df)} | Valide: {len(valid_out)} | Scartate: {len(rejected_df)}")


if __name__ == "__main__":
    clean_orders(
        input_path=Path("data/sample/raw_orders.csv"),
        clean_out=Path("output/clean_orders.csv"),
        rejected_out=Path("output/rejected_orders.csv"),
    )
