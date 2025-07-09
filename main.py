import argparse
import logging
import pandas as pd
from scripts.helpers import parse_iso_date
from scripts.transform import (
    standardize_column_names, convert_types, add_total_amount,
    merge_orders_customers, normalize_country, categorize_vip
)
from scripts.validate import (
    unique_key, no_nulls, valid_email, date_not_future, allowed_status
)

# 0) Configurar logging enriquecido
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

# 1) Leer argumentos desde terminal
parser = argparse.ArgumentParser()
parser.add_argument("--orders", required=True)
parser.add_argument("--customers", required=True)
parser.add_argument("--output", required=True)
args = parser.parse_args()

# 2) Leer órdenes y clientes
orders = pd.read_csv(args.orders)
customers = pd.read_csv(args.customers)

# 3) Transformaciones previas
orders = (
    orders.pipe(standardize_column_names)
          .pipe(convert_types)
          .pipe(add_total_amount)
)

# 🔁 Corrección: mapear estados adicionales
orders["status"] = orders["status"].replace({
    "shipped": "completed",
    "returned": "canceled"
})

customers = standardize_column_names(customers)
customers["customer_id"] = customers["customer_id"].astype(str)
customers["signup_date"] = customers["signup_date"].apply(parse_iso_date)

# 4) Merge + transformaciones nuevas
df = (
    merge_orders_customers(orders, customers)
       .pipe(normalize_country)
       .pipe(categorize_vip)
)

# 5) Logging informativo
logging.info(f"Registros procesados: {len(df)}")
logging.info(f"Ventas totales: USD {df['total_amount'].sum():,.2f}")

# 6) Validaciones ampliadas
unique_key(df, "order_id")
no_nulls(df, ["country", "email"])
valid_email(df)
date_not_future(df, "order_date")
allowed_status(df)

# 7) Export final
df.to_csv(args.output, index=False)


