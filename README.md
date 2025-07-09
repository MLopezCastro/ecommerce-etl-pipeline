# 🛒 E-commerce ETL Pipeline

Este proyecto implementa un pipeline de procesamiento de datos para un sistema de e-commerce. El objetivo es limpiar, validar y transformar datos de órdenes y clientes para obtener un archivo final unificado y listo para análisis.

---

## 📁 Estructura del proyecto

```
ecommerce-etl-pipeline/
│
├── data/
│   ├── raw/
│   │   ├── orders.csv
│   │   └── customers.csv
│   └── output/
│       └── final.csv
│
├── scripts/
│   ├── process.py
│   ├── transform.py
│   └── validate.py
│
├── main.py
└── README.md
```

---

## ⚙️ Cómo ejecutar el pipeline

Desde la terminal:

```bash
python main.py --orders data/raw/orders.csv --customers data/raw/customers.csv --output data/output/final.csv
```

---

## 🧪 Reglas implementadas

| **Regla**              | **Descripción**                                            |
|------------------------|------------------------------------------------------------|
| `no_nulls`             | Orden, fecha, cliente, producto ≠ NULL                     |
| `unique_key(order_id)` | `order_id` debe ser único                                  |
| `positive_values`      | `quantity` y `unit_price` ≥ 0                              |
| `valid_email`          | Email contiene “@”                                         |
| `date_not_future`      | `order_date` no puede ser futura                           |
| `vip_level`            | `gold / silver / regular` según reglas                     |

> 🟡 *Nota: la validación `allowed_status` no fue incluida en esta versión debido a que el dataset de órdenes no contenía la columna `order_status`. Se incorporará en la versión 2 del bloque.*

---

## 📝 Notas adicionales

- Se utilizaron `pandas` para procesamiento de datos.
- Se implementó `logging` enriquecido con formato:
  ```
  %(asctime)s | %(levelname)s | %(name)s | %(message)s
  ```
- Se registran logs como:
  ```python
  logging.info(f"Registros procesados: {len(df)}")
  logging.info(f"Ventas totales: USD {df['total_amount'].sum():,.2f}")
  ```

---

## 🚧 Pendientes para la versión 2

- Incorporar validación `allowed_status` una vez que el dataset esté completo.
- Revisión del diseño de columnas del CSV original vs. el modelo entregado.
- Validar consistencia de tipos de datos al leer archivos.
