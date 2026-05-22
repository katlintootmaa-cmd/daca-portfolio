"""Roll A: API Query.

See moodul loob Supabase ühenduse, pärib sales/customers/products tabelid
DataFrame'idena ning kasutab pagination'i ja retry loogikat, et suurte
tabelite laadimine oleks töökindlam.
"""

from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Any

import pandas as pd
from dotenv import load_dotenv
from supabase import create_client


logger = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent.parent

FALLBACK_SALES_PATHS = [
    PROJECT_ROOT / "datasets" / "clean" / "sales.csv",
    ROOT.parent / "datasets" / "clean" / "sales.csv",
    PROJECT_ROOT / "SQL" / "sales_supabase_import.csv",
    PROJECT_ROOT / "SQL" / "sales_rows.csv",
]
FALLBACK_CUSTOMER_PATHS = [
    PROJECT_ROOT / "datasets" / "clean" / "customers.csv",
    ROOT.parent / "datasets" / "clean" / "customers.csv",
    PROJECT_ROOT / "SQL" / "customers.csv",
    PROJECT_ROOT / "SQL" / "customers_rows.csv",
]
FALLBACK_PRODUCT_PATHS = [
    PROJECT_ROOT / "datasets" / "clean" / "products.csv",
    ROOT.parent / "datasets" / "clean" / "products.csv",
    PROJECT_ROOT / "SQL" / "products.csv",
    PROJECT_ROOT / "SQL" / "products_rows.csv",
]


def load_environment() -> None:
    """Leia lähim .env fail ja lae API tunnused keskkonnamuutujatesse."""
    dotenv_path = next(
        (path for path in [Path.cwd() / ".env", *[parent / ".env" for parent in Path.cwd().parents]] if path.exists()),
        None,
    )
    load_dotenv(dotenv_path=dotenv_path)


def create_supabase_client() -> Any:
    """Loo Supabase klient .env failis olevate URL-i ja API võtme põhjal."""
    load_environment()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("Puudub SUPABASE_URL või SUPABASE_ANON_KEY/SUPABASE_KEY .env failis.")

    return create_client(url, key)


def fetch_table(
    supabase: Any,
    table_name: str,
    page_size: int = 1000,
    max_retries: int = 3,
    retry_base_seconds: float = 1,
    date_column: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.DataFrame:
    """Päri üks Supabase tabel lehekülgede kaupa ja proovi vea korral uuesti."""
    rows: list[dict[str, Any]] = []
    start = 0

    while True:
        end = start + page_size - 1

        for attempt in range(1, max_retries + 1):
            try:
                query = supabase.table(table_name).select("*")
                if date_column and start_date:
                    query = query.gte(date_column, start_date)
                if date_column and end_date:
                    query = query.lte(date_column, end_date)

                response = query.range(start, end).execute()
                page = response.data or []
                rows.extend(page)
                logger.info("%s: read %s-%s, rows=%s", table_name, start, end, len(page))
                break
            except Exception as exc:
                if attempt == max_retries:
                    raise RuntimeError(f"API päring tabelile '{table_name}' ebaõnnestus: {exc}") from exc
                wait_seconds = retry_base_seconds * (2 ** (attempt - 1))
                logger.warning(
                    "%s: katse %s/%s ebaõnnestus, proovin uuesti %s s pärast",
                    table_name,
                    attempt,
                    max_retries,
                    wait_seconds,
                )
                time.sleep(wait_seconds)

        if len(page) < page_size:
            break
        start += page_size

    return pd.DataFrame(rows)


def fetch_sales(
    supabase: Any,
    start_date: str | None = None,
    end_date: str | None = None,
    page_size: int = 1000,
    max_retries: int = 3,
    retry_base_seconds: float = 1,
    table_name: str = "sales",
) -> pd.DataFrame:
    """Päri müügiandmed, vajadusel kuupäevavahemiku filtriga."""
    return fetch_table(
        supabase,
        table_name,
        page_size=page_size,
        max_retries=max_retries,
        retry_base_seconds=retry_base_seconds,
        date_column="sale_date",
        start_date=start_date,
        end_date=end_date,
    )


def fetch_customers(
    supabase: Any,
    page_size: int = 1000,
    max_retries: int = 3,
    retry_base_seconds: float = 1,
    table_name: str = "customers",
) -> pd.DataFrame:
    """Päri kliendiandmed Supabase customers tabelist."""
    return fetch_table(
        supabase,
        table_name,
        page_size=page_size,
        max_retries=max_retries,
        retry_base_seconds=retry_base_seconds,
    )


def fetch_products(
    supabase: Any,
    page_size: int = 1000,
    max_retries: int = 3,
    retry_base_seconds: float = 1,
    table_name: str = "products",
) -> pd.DataFrame:
    """Päri tooteandmed Supabase products tabelist."""
    return fetch_table(
        supabase,
        table_name,
        page_size=page_size,
        max_retries=max_retries,
        retry_base_seconds=retry_base_seconds,
    )


def read_first_existing_csv(paths: list[Path], label: str) -> pd.DataFrame:
    """Loe esimene olemasolev kohalik CSV fallback fail."""
    for path in paths:
        if path.exists():
            df = pd.read_csv(path)
            logger.info("CSV fallback '%s': %s rida failist %s", label, len(df), path)
            return df

    logger.warning("CSV fallback '%s' puudub. Otsitud failid: %s", label, ", ".join(str(path) for path in paths))
    return pd.DataFrame()


def csv_fallback_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame] | None:
    """Kasuta kohalikke CSV faile, kui API ei ole saadaval."""
    sales = read_first_existing_csv(FALLBACK_SALES_PATHS, "sales")
    customers = read_first_existing_csv(FALLBACK_CUSTOMER_PATHS, "customers")
    products = read_first_existing_csv(FALLBACK_PRODUCT_PATHS, "products")

    if sales.empty or customers.empty:
        return None
    return sales, customers, products


def sample_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Loo väike varuandmestik, et pipeline saaks ka API tõrke korral joosta."""
    sales = pd.DataFrame(
        {
            "sale_id": range(1, 22),
            "sale_date": pd.date_range("2024-09-01", periods=21, freq="14D"),
            "customer_id": [1001, 1002, 1003, 1001, 1004, 1005, 1001, 1002, 1006, 1004, 1003, 1007, 1005, 1001, 1002, 1008, 1004, 1006, 1001, 1007, 1003],
            "product_id": [201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221],
            "quantity": [2, 1, 3, 1, 4, 1, 2, 2, 1, 3, 1, 1, 2, 5, 1, 1, 2, 1, 3, 1, 2],
            "total_price": [180.0, 59.9, 240.0, 75.0, 420.0, 89.9, 310.0, 129.0, 45.0, 260.0, 55.0, 35.0, 150.0, 520.0, 80.0, 25.0, 190.0, 65.0, 410.0, 44.0, 135.0],
            "channel": ["pood", "online", "pood", "pood", "online", "pood", "online", "pood", "pood", "online", "pood", "pood", "online", "pood", "online", "pood", "pood", "online", "online", "pood", "online"],
            "store_location": ["Tallinn", None, "Tartu", "Tallinn", None, "Parnu", None, "Tartu", "Narva", None, "Tartu", "Tallinn", None, "Tallinn", None, "Parnu", "Tartu", None, None, "Tallinn", None],
        }
    )
    customers = pd.DataFrame(
        {
            "customer_id": [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
            "first_name": ["Kati", "Mart", "Liina", "Peeter", "Anna", "Jaan", "Mari", "Toomas"],
            "last_name": ["Tamm", "Kask", "Saar", "Sepp", "Oja", "Pihl", "Kuusk", "Rebane"],
            "email": ["kati@example.com", "mart@example.com", None, "peeter@example.com", "anna@example.com", None, "mari@example.com", None],
            "phone": ["+3725000001", None, "+3725000003", "+3725000004", None, "+3725000006", None, None],
            "city": ["Tallinn", "Tartu", "Tartu", "Tallinn", "Parnu", "Narva", "Tallinn", "Parnu"],
            "loyalty_tier": ["gold", "silver", None, "gold", "bronze", None, "bronze", None],
        }
    )
    products = pd.DataFrame(
        {
            "product_id": list(range(201, 222)),
            "product_name": [f"Toode {i}" for i in range(201, 222)],
            "category": ["riided", "jalanoud", "aksessuaarid"] * 7,
        }
    )
    return sales, customers, products
