import pandas as pd

def unique_key(df: pd.DataFrame, col: str):
    """Valida que una columna clave no tenga valores duplicados."""
    if df[col].duplicated().any():
        dups = df.loc[df[col].duplicated(), col].tolist()[:5]
        raise ValueError(f"Duplicados en la columna {col}: {dups}")

def no_nulls(df: pd.DataFrame, cols: list):
    """Valida que no haya valores nulos en columnas críticas."""
    for col in cols:
        if df[col].isnull().any():
            raise ValueError(f"Valores nulos encontrados en la columna {col}")

def valid_email(df: pd.DataFrame):
    """Valida que los emails contengan el carácter '@'."""
    bad = df.loc[~df["email"].str.contains("@"), "email"].unique()
    if len(bad):
        raise ValueError(f"Emails inválidos encontrados: {bad[:5]}")

def date_not_future(df: pd.DataFrame, col: str):
    """Verifica que la columna de fecha no contenga fechas futuras."""
    hoy = pd.to_datetime("today").normalize()
    if (pd.to_datetime(df[col]) > hoy).any():
        raise ValueError(f"La columna {col} contiene fechas futuras.")

def allowed_status(df: pd.DataFrame):
    """Valida que los estados en la columna 'status' sean válidos."""
    allowed = {"completed", "pending", "canceled", "shipped", "returned"}
    actual = set(df["status"].unique())
    if not actual.issubset(allowed):
        raise ValueError(f"Estados no permitidos encontrados: {actual - allowed}")
