import pandas as pd
from scripts.helpers import parse_iso_date

def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte los nombres de columnas a snake_case minúsculas."""
    df.columns = (
        df.columns.str.strip()
                  .str.lower()
                  .str.replace(" ", "_")
                  .str.replace("-", "_")
    )
    return df

def convert_types(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte columnas específicas a tipos esperados."""
    df["customer_id"] = df["customer_id"].astype(str)
    df["order_id"] = df["order_id"].astype(str)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    return df

def add_total_amount(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega columna total_amount = quantity * price."""
    df["total_amount"] = df["quantity"] * df["unit_price"]
    return df

def merge_orders_customers(df_orders: pd.DataFrame,
                           df_customers: pd.DataFrame) -> pd.DataFrame:
    """Enriquece órdenes con datos del cliente."""
    return df_orders.merge(df_customers, on="customer_id", how="left")

def categorize_vip(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega columna vip_level basada en vip_flag y total_amount."""
    df["vip_level"] = "regular"
    mask_gold = (df["vip_flag"] == "Y") & (df["total_amount"] > 100)
    mask_silver = (df["vip_flag"] == "Y") & (df["total_amount"] <= 100)
    df.loc[mask_gold, "vip_level"] = "gold"
    df.loc[mask_silver, "vip_level"] = "silver"
    return df

def normalize_country(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte países a mayúsculas y corrige errores típicos."""
    df["country"] = df["country"].str.upper().str.strip()
    fixes = {"ARG": "AR", "USA": "US"}
    df["country"] = df["country"].replace(fixes)
    return df


