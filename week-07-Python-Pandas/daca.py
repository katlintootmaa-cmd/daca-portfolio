"""Week 7 pandas/RFM harjutuste skript.

Fail ühendub Supabase PostgreSQL andmebaasiga, laeb müügi- ja kliendiandmed,
teeb pandas ülevaated, lihtsad töötlused, Plotly graafikud ja RFM analüüsi.
"""

from __future__ import annotations

import os

import pandas as pd
import plotly.express as px
import psycopg
from dotenv import load_dotenv


SHOW_CHARTS = False
REQUIRED_ENV_VARS = (
    "SUPABASE_DB_HOST",
    "SUPABASE_DB_NAME",
    "SUPABASE_DB_USER",
    "SUPABASE_DB_PASSWORD",
)


def print_section(title: str) -> None:
    """Prindi terminali loetav sektsiooni pealkiri."""
    print(f"\n{'=' * 12} {title} {'=' * 12}")


def get_supabase_connection() -> psycopg.Connection:
    """Loo PostgreSQL ühendus Supabase andmebaasiga .env muutujate põhjal."""
    load_dotenv()

    missing = [name for name in REQUIRED_ENV_VARS if not os.getenv(name)]
    if missing:
        missing_list = ", ".join(missing)
        raise RuntimeError(f".env failist puuduvad Supabase ühenduse muutujad: {missing_list}")

    return psycopg.connect(
        host=os.environ["SUPABASE_DB_HOST"],
        port=int(os.getenv("SUPABASE_DB_PORT", "5432")),
        dbname=os.environ["SUPABASE_DB_NAME"],
        user=os.environ["SUPABASE_DB_USER"],
        password=os.environ["SUPABASE_DB_PASSWORD"],
        sslmode="require",
        connect_timeout=10,
    )


def load_supabase_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Lae Supabase'ist müügi- ja kliendiandmed ning korrasta tüübid."""
    sales_query = """
        SELECT
            s.sale_id,
            s.invoice_id,
            s.sale_date,
            s.customer_id,
            s.product_id,
            s.quantity,
            s.unit_price,
            s.total_price,
            s.channel,
            s.store_location,
            s.payment_method,
            p.category AS product_category
        FROM sales AS s
        LEFT JOIN products AS p
            ON s.product_id = p.product_id
        ORDER BY s.sale_date, s.sale_id;
    """

    customers_query = """
        SELECT
            customer_id,
            first_name,
            last_name,
            email,
            city,
            registration_date,
            loyalty_tier,
            birth_year
        FROM customers
        ORDER BY customer_id;
    """

    with get_supabase_connection() as conn:
        sales = fetch_dataframe(conn, sales_query)
        customers = fetch_dataframe(conn, customers_query)

    sales["sale_date"] = pd.to_datetime(sales["sale_date"])
    sales["total_price"] = pd.to_numeric(sales["total_price"])
    sales["unit_price"] = pd.to_numeric(sales["unit_price"])
    sales["customer_id"] = pd.to_numeric(sales["customer_id"], errors="coerce").astype("Int64")
    customers["customer_id"] = customers["customer_id"].astype("Int64")

    sales["city"] = sales["store_location"].fillna("Online")
    sales["product_category"] = sales["product_category"].fillna("Teadmata")

    return sales, customers


def fetch_dataframe(conn: psycopg.Connection, query: str) -> pd.DataFrame:
    """Käivita SQL päring ja tagasta tulemus pandas DataFrame'ina."""
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        columns = [description.name for description in cur.description]

    return pd.DataFrame(rows, columns=columns)


def exercise_1_dataframe_overview(df: pd.DataFrame) -> None:
    """Kuva DataFrame'i põhiülevaade ja lihtsad kirjeldavad näitajad."""
    print_section("Osa 1: DataFrame uurimine")

    print("Shape:", df.shape)
    print("\nHead:")
    print(df.head())

    print("\nInfo:")
    df.info()

    print("\nDescribe:")
    print(df.describe())

    print("\nDtypes:")
    print(df.dtypes)

    print("\nHarjutus 1B vastused:")
    print("Unikaalseid kliente:", df["customer_id"].nunique())
    print("Linnad:", df["city"].unique())
    print("Tellimused linniti:")
    print(df["city"].value_counts())
    print("Kogukäive:", round(df["total_price"].sum(), 2))

    print("\nHarjutus 1C: product_category ülevaade")
    print("Unikaalseid kategooriaid:", df["product_category"].nunique())
    print("Kategooriad:", df["product_category"].unique())
    print("Tellimused kategooriate kaupa:")
    print(df["product_category"].value_counts())
    print("Keskmine tellimuse summa kategooriate kaupa:")
    print(df.groupby("product_category")["total_price"].mean().sort_values(ascending=False))


def exercise_2_processing(df: pd.DataFrame, customers: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Filtreeri, grupeerib ja ühenda andmeid kliendi ostukäitumise leidmiseks."""
    print_section("Osa 2: filtreerimine, groupby ja merge")

    tallinn = df[df["city"] == "Tallinn"]
    print("Tallinna tellimused:")
    print(f"Kokku: {len(tallinn)} tellimust, käive: {tallinn['total_price'].sum():.2f} EUR")

    print("\nKäive linniti:")
    city_revenue = df.groupby("city")["total_price"].agg(["sum", "mean", "count"])
    city_revenue.columns = ["kogukäive", "keskmine", "tellimusi"]
    print(city_revenue.sort_values("kogukäive", ascending=False))

    df = df.copy()
    df["order_size"] = df["total_price"].apply(
        lambda price: "Suur (100+)" if price >= 100 else "Väike (<100)"
    )
    print("\nTellimused suuruse järgi:")
    print(df["order_size"].value_counts())

    customer_summary = (
        df.groupby("customer_id")["total_price"]
        .agg(kogukulutus="sum", keskmine="mean", tellimusi="count")
        .reset_index()
        .sort_values("kogukulutus", ascending=False)
    )
    customer_summary["vip_status"] = customer_summary["kogukulutus"].apply(
        lambda amount: "VIP" if amount > 200 else "Tavaline"
    )

    print("\nKliendi ostukäitumise kokkuvõte:")
    print(customer_summary)

    merged = pd.merge(df, customers, on="customer_id", how="left")
    print("\nShape enne merge:", df.shape)
    print("Shape pärast merge:", merged.shape)

    top_customers = (
        merged.dropna(subset=["customer_id"])
        .groupby(["customer_id", "first_name", "last_name"], dropna=False)["total_price"]
        .sum()
        .reset_index(name="kogukulutus")
        .sort_values("kogukulutus", ascending=False)
        .head(5)
    )

    print("\nTOP 5 klienti nime ja kogukulutuse järgi:")
    print(top_customers)

    return df, customer_summary


def exercise_3_visualizations(df: pd.DataFrame, customer_summary: pd.DataFrame) -> None:
    """Koosta Plotly graafikud kategooriate, kuude, VIP ja tellimuse suuruse kohta."""
    print_section("Osa 3: Plotly visualiseerimised")

    cat_revenue = (
        df.groupby("product_category")["total_price"]
        .sum()
        .reset_index()
        .sort_values("total_price", ascending=True)
    )
    category_fig = px.bar(
        cat_revenue,
        x="total_price",
        y="product_category",
        orientation="h",
        title="UrbanStyle: millised tootekategooriad toovad kõige rohkem käivet?",
        labels={"total_price": "Käive (EUR)", "product_category": "Kategooria"},
        color="product_category",
        text="total_price",
    )
    category_fig.update_layout(showlegend=False)
    category_fig.update_traces(texttemplate="%{text:.2f} EUR", textposition="outside")

    monthly = df.groupby(df["sale_date"].dt.to_period("M"))["total_price"].sum().reset_index()
    monthly["sale_date"] = monthly["sale_date"].astype(str)
    monthly_fig = px.line(
        monthly,
        x="sale_date",
        y="total_price",
        title="UrbanStyle: kuukäive trend 2024",
        labels={"sale_date": "Kuu", "total_price": "Käive (EUR)"},
        markers=True,
    )

    vip_counts = customer_summary["vip_status"].value_counts().reset_index()
    vip_fig = px.pie(
        vip_counts,
        values="count",
        names="vip_status",
        title="UrbanStyle: kliendid VIP-staatuse järgi",
    )

    order_size_revenue = (
        df.groupby(["city", "order_size"])["total_price"]
        .sum()
        .reset_index()
        .sort_values("total_price", ascending=False)
    )
    story_fig = px.bar(
        order_size_revenue,
        x="city",
        y="total_price",
        color="order_size",
        barmode="group",
        title="UrbanStyle: suuremate tellimuste käive linnade kaupa",
        labels={"city": "Linn", "total_price": "Käive (EUR)", "order_size": "Tellimuse suurus"},
        text="total_price",
    )
    story_fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")

    print("Valmis graafikud: kategooriate käive, kuukäive, VIP jaotus, tellimuse suurus linniti.")
    print("Graafikute avamiseks muuda faili alguses SHOW_CHARTS = True.")

    if SHOW_CHARTS:
        category_fig.show()
        monthly_fig.show()
        vip_fig.show()
        story_fig.show()


def assign_segment(score: int) -> str:
    """Määra lihtsustatud RFM segment koondskoori põhjal."""
    if score >= 8:
        return "VIP Champions"
    if score >= 6:
        return "Loyal Customers"
    if score >= 4:
        return "Potential Loyalists"
    return "At Risk"


def rfm_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Arvuta Recency, Frequency ja Monetary skoorid ning kliendisegmendid."""
    print_section("Süntees: RFM kliendisegmenteerimine")

    rfm_source = df.dropna(subset=["customer_id"]).copy()
    reference_date = rfm_source["sale_date"].max() + pd.Timedelta(days=1)

    recency = rfm_source.groupby("customer_id")["sale_date"].max().reset_index()
    recency.columns = ["customer_id", "last_purchase"]
    recency["recency_days"] = (reference_date - recency["last_purchase"]).dt.days

    frequency = rfm_source.groupby("customer_id").size().reset_index(name="frequency")

    monetary = rfm_source.groupby("customer_id")["total_price"].sum().reset_index()
    monetary.columns = ["customer_id", "monetary"]

    rfm = (
        recency[["customer_id", "recency_days"]]
        .merge(frequency, on="customer_id")
        .merge(monetary, on="customer_id")
    )

    rfm["R_score"] = pd.qcut(rfm["recency_days"].rank(method="first"), q=3, labels=[3, 2, 1]).astype(int)
    rfm["F_score"] = pd.qcut(rfm["frequency"].rank(method="first"), q=3, labels=[1, 2, 3]).astype(int)
    rfm["M_score"] = pd.qcut(rfm["monetary"].rank(method="first"), q=3, labels=[1, 2, 3]).astype(int)
    rfm["RFM_score"] = rfm["R_score"] + rfm["F_score"] + rfm["M_score"]
    rfm["segment"] = rfm["RFM_score"].apply(assign_segment)

    rfm = rfm.sort_values("RFM_score", ascending=False)
    print("Andmestiku periood:", rfm_source["sale_date"].min().date(), "kuni", rfm_source["sale_date"].max().date())
    print("Viitekuupäev:", reference_date.date())
    print("\nRFM tabel:")
    print(rfm)

    segment_counts = rfm["segment"].value_counts().reset_index()
    segment_fig = px.bar(
        segment_counts,
        x="segment",
        y="count",
        title="UrbanStyle: kliendisegmentide jaotus (RFM)",
        labels={"segment": "Segment", "count": "Klientide arv"},
        color="segment",
    )

    scatter_fig = px.scatter(
        rfm,
        x="recency_days",
        y="monetary",
        color="segment",
        size="frequency",
        hover_data=["customer_id"],
        title="UrbanStyle: Recency vs Monetary (RFM)",
        labels={"recency_days": "Päevi viimasest ostust", "monetary": "Kogukulutus (EUR)"},
    )

    if SHOW_CHARTS:
        segment_fig.show()
        scatter_fig.show()

    vip_count = (rfm["segment"] == "VIP Champions").sum()
    vip_revenue_share = (
        rfm.loc[rfm["segment"] == "VIP Champions", "monetary"].sum() / rfm["monetary"].sum()
    )

    print("\nRFM küsimuste vastused:")
    print("VIP Champions kliente:", vip_count)
    print(f"VIP-klientide osakaal kogutuludest: {vip_revenue_share:.1%}")
    print(
        "Soovitus At Risk segmendile: saada personaalne tagasituleku pakkumine "
        "ja mõõda, kas järgmise 30 päeva jooksul tehakse uus ost."
    )

    return rfm


def main() -> None:
    """Käivita kõik Week 7 harjutuse sammud järjest."""
    df, customers = load_supabase_data()
    print(f"Laadisin Supabase'ist {len(df)} müügirida ja {len(customers)} klienti.")

    exercise_1_dataframe_overview(df)
    processed_df, customer_summary = exercise_2_processing(df, customers)
    exercise_3_visualizations(processed_df, customer_summary)
    rfm_analysis(processed_df)


if __name__ == "__main__":
    main()
