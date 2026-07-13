from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

RANDOM_SEED = 42
N_CUSTOMERS = 2000
N_PRODUCTS = 180
N_MONTHS = 36
START_MONTH = "2023-01-01"
OUTPUT_DIR = Path("../data/synthetic")

rng = np.random.default_rng(RANDOM_SEED)

def weighted_choice(values, probabilities, size= None):
    probabilities = np.array(probabilities, dtype=float)
    probabilities = probabilities / probabilities.sum()
    return rng.choice(values, p=probabilities, size =size)


def make_customer_name(customer_id: int) -> str:
    adjectives = [
        "Northstar", "BluePeak", "Silverline", "Prime", "Vertex", "Nexora",
        "Summit", "BrightPath", "IronBridge", "NovaCore", "Greenfield",
        "Atlas", "Redwood", "ClearView", "UrbanGrid", "Everline",
    ]
    nouns = [
        "Industries", "Systems", "Trading", "Solutions", "Medical",
        "Logistics", "Manufacturing", "Supplies", "Distribution", "Energy",
        "Retail Group", "Technologies", "Services", "Partners",
    ]
    suffixes = ["GmbH", "AG", "Ltd", "SAS", "BV", "SRL", "LLC", "Group"]
    return f"{rng.choice(adjectives)} {rng.choice(nouns)} {rng.choice(suffixes)} {customer_id:04d}"


def create_product_dimension(n_products: int = N_PRODUCTS) -> pd.DataFrame:
    prod_lines = [
        "Industrial Equipment",
        "Consumables",
        "Maintenance",
        "Safety",
        "Automation",
        "Specialty Materials",
        "Services",
    ]
    grp1_values = [
        "Core Products",
        "Premium Products",
        "Maintenance Kits",
        "Safety Solutions",
        "Automation Modules",
        "Service Contracts",
    ]
    grp2_by_grp1 = {
        "Core Products": ["Core Basic", "Core Advanced", "Core Replacement"],
        "Premium Products": ["Premium Standard", "Premium Plus", "Premium Custom"],
        "Maintenance Kits": ["Preventive Kits", "Repair Kits", "Calibration Kits"],
        "Safety Solutions": ["Personal Safety", "Facility Safety", "Compliance Safety"],
        "Automation Modules": ["Sensors", "Controllers", "Monitoring"],
        "Service Contracts": ["Installation", "Training", "Extended Support"],
    }
    grp3_by_grp2 = {
        grp2: [f"{grp2} Type {i}" for i in range(1, 3)]
        for grp2_list in grp2_by_grp1.values()
        for grp2 in grp2_list
    }

    rows = []
    for i in range(1, n_products + 1):
        grp1 = weighted_choice(
            grp1_values,
            [0.24, 0.15, 0.18, 0.14, 0.17, 0.12],
        )
        grp2 = rng.choice(grp2_by_grp1[grp1])
        grp3 = rng.choice(grp3_by_grp2[grp2])
        prod_line = rng.choice(prod_lines)
        base_price = {
            "Core Products": 75,
            "Premium Products": 250,
            "Maintenance Kits": 120,
            "Safety Solutions": 90,
            "Automation Modules": 420,
            "Service Contracts": 650,
        }[grp1]
        unit_price = float(np.round(rng.lognormal(np.log(base_price), 0.35), 2))
        margin_category = weighted_choice(
            ["Low", "Medium", "High"],
            [0.25, 0.50, 0.25] if grp1 != "Service Contracts" else [0.10, 0.35, 0.55],
        )
        rows.append(
            {
                "ID_Product": f"P{i:04d}",
                "Product_Name": f"{grp3} {i:04d}",
                "Prod_Line": prod_line,
                "Prd_Grp_1": grp1,
                "Prd_Grp_2": grp2,
                "Prd_Grp_3": grp3,
                "Unit_Price": unit_price,
                "Margin_Category": margin_category,
            }
        )
    return pd.DataFrame(rows)


def create_customer_dimension(n_customers: int = N_CUSTOMERS) -> pd.DataFrame:
    segments = ["Enterprise", "Mid-Market", "SMB", "Distributor", "Public Sector"]
    sizes = ["Small", "Medium", "Large", "Very Large"]
    industries = [
        "Manufacturing", "Healthcare", "Retail", "Construction", "Logistics",
        "Energy", "Technology", "Public Administration", "Food & Beverage",
        "Automotive",
    ]
    countries = ["Germany", "France", "Netherlands", "Italy", "Spain", "Austria", "Switzerland", "Belgium"]
    channels = ["Inbound", "Outbound Sales", "Partner", "Trade Fair", "Referral", "Website"]
    behavior_types = [
        "High-Value Loyal",
        "New Growing",
        "Occasional Buyer",
        "Declining",
        "Churn Risk",
    ]

    rows = []
    for i in range(1, n_customers + 1):
        customer_id = f"C{i:05d}"
        segment = weighted_choice(segments, [0.16, 0.32, 0.30, 0.14, 0.08])
        size_probs = {
            "Enterprise": [0.02, 0.12, 0.36, 0.50],
            "Mid-Market": [0.10, 0.42, 0.36, 0.12],
            "SMB": [0.58, 0.32, 0.09, 0.01],
            "Distributor": [0.05, 0.30, 0.45, 0.20],
            "Public Sector": [0.12, 0.38, 0.35, 0.15],
        }[segment]
        customer_size = weighted_choice(sizes, size_probs)
        industry = weighted_choice(industries, [0.18, 0.10, 0.10, 0.11, 0.10, 0.08, 0.10, 0.07, 0.08, 0.08])
        country = weighted_choice(countries, [0.30, 0.16, 0.12, 0.10, 0.10, 0.08, 0.08, 0.06])
        behavior = weighted_choice(behavior_types, [0.18, 0.20, 0.28, 0.18, 0.16])
        start_date = pd.Timestamp(START_MONTH) - pd.DateOffset(months=int(rng.integers(0, 30)))
        if behavior == "New Growing":
            start_date = pd.Timestamp(START_MONTH) + pd.DateOffset(months=int(rng.integers(0, 22)))

        rows.append(
            {
                "ID_Customer": customer_id,
                "Customer_Name": make_customer_name(i),
                "Customer_Segment": segment,
                "Customer_Size": customer_size,
                "Industry": industry,
                "Region_CC": weighted_choice(["DACH", "Western Europe", "Southern Europe", "Benelux"], [0.40, 0.25, 0.20, 0.15]),
                "Region_OC": weighted_choice(["North", "South", "East", "West", "Central"], [0.20, 0.22, 0.17, 0.21, 0.20]),
                "Country": country,
                "Acquisition_Channel": weighted_choice(channels, [0.18, 0.24, 0.22, 0.12, 0.10, 0.14]),
                "Customer_Start_Date": start_date,
                "_Behavior_Type": behavior})

    df = pd.DataFrame(rows)
    df.loc[rng.choice(df.index, size=int(0.03 * len(df)), replace=False), "Region_OC"] = np.nan
    df.loc[rng.choice(df.index, size=int(0.02 * len(df)), replace=False), "Acquisition_Channel"] = np.nan
    return df


def product_preference_weights(customer: pd.Series, products: pd.DataFrame) -> np.ndarray:
    weights = np.ones(len(products))

    segment_boost = {
        "Enterprise": ["Premium Products", "Automation Modules", "Service Contracts"],
        "Mid-Market": ["Core Products", "Maintenance Kits", "Automation Modules"],
        "SMB": ["Core Products", "Safety Solutions"],
        "Distributor": ["Core Products", "Premium Products", "Maintenance Kits"],
        "Public Sector": ["Safety Solutions", "Service Contracts"]}
    industry_boost = {
        "Manufacturing": ["Maintenance Kits", "Automation Modules"],
        "Healthcare": ["Safety Solutions", "Service Contracts"],
        "Retail": ["Core Products", "Safety Solutions"],
        "Construction": ["Core Products", "Safety Solutions"],
        "Logistics": ["Automation Modules", "Maintenance Kits"],
        "Energy": ["Premium Products", "Automation Modules"],
        "Technology": ["Automation Modules", "Service Contracts"],
        "Public Administration": ["Safety Solutions", "Service Contracts"],
        "Food & Beverage": ["Maintenance Kits", "Safety Solutions"],
        "Automotive": ["Premium Products", "Automation Modules"]}

    weights[products["Prd_Grp_1"].isin(segment_boost[customer["Customer_Segment"]])] *= 2.2
    weights[products["Prd_Grp_1"].isin(industry_boost[customer["Industry"]])] *= 1.8
    weights *= np.where(products["Margin_Category"].eq("High"), 1.15, 1.0)
    return weights / weights.sum()


def monthly_purchase_probability(behavior: str, month_index: int, start_month_index: int) -> float:
    age = max(month_index - start_month_index, 0)
    if behavior == "High-Value Loyal":
        p = 0.78
    elif behavior == "New Growing":
        p = min(0.18 + 0.025 * age, 0.68)
    elif behavior == "Occasional Buyer":
        p = 0.22
    elif behavior == "Declining":
        p = max(0.65 - 0.018 * age, 0.12)
    else:
        p = max(0.38 - 0.025 * age, 0.03)
    return float(np.clip(p, 0.01, 0.90))


def create_sales_fact(customers: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    months = pd.date_range(START_MONTH, periods=N_MONTHS, freq="MS")
    start_period = pd.Period(START_MONTH, freq="M")

    size_multiplier = {"Small": 0.7, "Medium": 1.0, "Large": 1.8, "Very Large": 3.0}
    segment_multiplier = {"Enterprise": 1.8, "Mid-Market": 1.2, "SMB": 0.7, "Distributor": 1.6, "Public Sector": 1.1}
    behavior_multiplier = {
        "High-Value Loyal": 1.9,
        "New Growing": 1.0,
        "Occasional Buyer": 0.6,
        "Declining": 1.1,
        "Churn Risk": 0.5}
    seasonal_index = np.array([0.88, 0.92, 1.05, 1.02, 1.08, 1.12, 0.95, 0.90, 1.10, 1.18, 1.25, 0.82])

    rows = []
    product_price = products.set_index("ID_Product")["Unit_Price"].to_dict()
    product_ids = products["ID_Product"].to_numpy()
    for _, customer in customers.iterrows():
        start_idx = max((customer["Customer_Start_Date"].to_period("M") - start_period).n, 0)
        pref = product_preference_weights(customer, products)
        favorite_count = int(rng.integers(4, 14))
        favorite_products = rng.choice(product_ids, size=favorite_count, replace=False, p=pref)

        for month_idx, month in enumerate(months):
            if month_idx < start_idx:
                continue
            behavior = customer["_Behavior_Type"]
            p_buy = monthly_purchase_probability(behavior, month_idx, start_idx)
            p_buy *= seasonal_index[month.month - 1]
            if rng.random() > min(p_buy, 0.95):
                continue

            n_lines = int(rng.poisson(1.2 if behavior != "High-Value Loyal" else 2.4) + 1)
            n_lines = min(n_lines, 8)
            chosen_products = rng.choice(favorite_products, size=min(n_lines, len(favorite_products)), replace=False)

            for product_id in chosen_products:
                base_units = (
                    size_multiplier[customer["Customer_Size"]]
                    * segment_multiplier[customer["Customer_Segment"]]
                    * behavior_multiplier[behavior]
                    * seasonal_index[month.month - 1]
                )
                units = max(1, int(rng.poisson(base_units * rng.uniform(1.0, 4.0))))
                discount = rng.uniform(0.86, 1.03) if customer["Customer_Size"] in ["Large", "Very Large"] else rng.uniform(0.95, 1.08)
                sales = float(np.round(units * product_price[product_id] * discount, 2))
                rows.append(
                    {
                        "Month_Year": month,
                        "Customer_ID": customer["ID_Customer"],
                        "Product_ID": product_id,
                        "Sales": sales,
                        "Units": units})

    fact_sales = pd.DataFrame(rows)

    return fact_sales


def create_salesforce_activity(customers: pd.DataFrame, fact_sales: pd.DataFrame) -> pd.DataFrame:
    months = pd.date_range(START_MONTH, periods=N_MONTHS, freq="MS")
    sales_months = fact_sales.assign(Month_Year=lambda d: pd.to_datetime(d["Month_Year"]).dt.to_period("M"))
    sales_lookup = set(zip(sales_months["Customer_ID"], sales_months["Month_Year"].astype(str)))

    reps = [f"Rep_{i:02d}" for i in range(1, 26)]
    activity_types = ["Call", "Email", "Meeting", "Demo", "Proposal", "Account Review"]
    stages = ["Prospecting", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost", "Nurture"]
    rows = []

    for _, customer in customers.iterrows():
        behavior = customer["_Behavior_Type"]
        base_activity = {
            "High-Value Loyal": 0.55,
            "New Growing": 0.70,
            "Occasional Buyer": 0.25,
            "Declining": 0.45,
            "Churn Risk": 0.58
        }[behavior]
        for month in months:
            period_str = month.to_period("M").strftime("%Y-%m")
            has_sales = (customer["ID_Customer"], period_str) in sales_lookup
            p_activity = base_activity + (0.18 if has_sales else 0.0)
            if behavior == "Churn Risk" and month >= months[-6]:
                p_activity += 0.18
            if rng.random() > min(p_activity, 0.95):
                continue

            activity_count = int(max(1, rng.poisson(2.0 + (2.5 if has_sales else 0.0))))
            rows.append(
                {
                    "Month_Year": month,
                    "Customer_ID": customer["ID_Customer"],
                    "SF_Activity_Count": activity_count,
                    "SF_Selling_Time": float(np.round(activity_count * rng.uniform(0.25, 1.2), 2)),
                    "SF_Activity_Time_": float(np.round(activity_count * rng.uniform(0.15, 0.9), 2)),
                    "Activity_Type": weighted_choice(activity_types, [0.32, 0.28, 0.16, 0.08, 0.07, 0.09]),
                    "Sales_Rep": rng.choice(reps),
                    "Opportunity_Stage": weighted_choice(stages, [0.22, 0.20, 0.16, 0.10, 0.12, 0.06, 0.14])})

    return pd.DataFrame(rows)


def add_controlled_missing_values(
    fact_sales: pd.DataFrame,
    dim_product: pd.DataFrame,
    fact_sf: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    product_missing_idx = rng.choice(dim_product.index, size=max(1, int(0.015 * len(dim_product))), replace=False)
    dim_product.loc[product_missing_idx, "Margin_Category"] = np.nan

    sf_missing_idx = rng.choice(fact_sf.index, size=max(1, int(0.02 * len(fact_sf))), replace=False)
    fact_sf.loc[sf_missing_idx, "Opportunity_Stage"] = np.nan

    sales_missing_idx = rng.choice(fact_sales.index, size=max(1, int(0.005 * len(fact_sales))), replace=False)
    fact_sales.loc[sales_missing_idx, "Sales"] = np.nan

    return fact_sales, dim_product, fact_sf


def validate_data(
    fact_sales: pd.DataFrame,
    dim_customer: pd.DataFrame,
    dim_product: pd.DataFrame,
    fact_sf: pd.DataFrame,
) -> None:
    assert dim_customer["ID_Customer"].is_unique, "Customer IDs must be unique."
    assert dim_product["ID_Product"].is_unique, "Product IDs must be unique."
    assert set(fact_sales["Customer_ID"]).issubset(set(dim_customer["ID_Customer"])), "Unknown customers in fact_sales."
    assert set(fact_sales["Product_ID"]).issubset(set(dim_product["ID_Product"])), "Unknown products in fact_sales."
    assert set(fact_sf["Customer_ID"]).issubset(set(dim_customer["ID_Customer"])), "Unknown customers in fact_sf."
    assert fact_sales["Units"].dropna().ge(0).all(), "Units must be non-negative."
    assert fact_sales["Month_Year"].nunique() == N_MONTHS, "Unexpected number of sales months."


def summarize(
    fact_sales: pd.DataFrame,
    dim_customer: pd.DataFrame,
    dim_product: pd.DataFrame,
    fact_sf: pd.DataFrame,
) -> None:
    recent_cutoff = pd.Timestamp(START_MONTH) + pd.DateOffset(months=N_MONTHS - 6)
    recent_sales_customers = set(fact_sales.loc[pd.to_datetime(fact_sales["Month_Year"]) >= recent_cutoff, "Customer_ID"])
    recent_sf_customers = set(fact_sf.loc[pd.to_datetime(fact_sf["Month_Year"]) >= recent_cutoff, "Customer_ID"])
    print("\nSynthetic data generation summary")
    print("---------------------------------")
    print(f"Customers: {len(dim_customer):,}")
    print(f"Products: {len(dim_product):,}")
    print(f"Sales rows: {len(fact_sales):,}")
    print(f"Salesforce activity rows: {len(fact_sf):,}")
    print(f"Months: {fact_sales['Month_Year'].nunique()}")
    print(f"Total sales: {fact_sales['Sales'].sum(skipna=True):,.2f}")
    print(f"Customers with recent SF activity but no recent sales: {len(recent_sf_customers - recent_sales_customers):,}")
    print(f"Customers with recent sales but no recent SF activity: {len(recent_sales_customers - recent_sf_customers):,}")
    print("\nCustomer behavior distribution:")
    print(dim_customer["_Behavior_Type"].value_counts(normalize=True).round(3))
    print("\nProduct hierarchy cardinality:")
    print(dim_product[["Prod_Line", "Prd_Grp_1", "Prd_Grp_2", "Prd_Grp_3"]].nunique())


def save_outputs(
    fact_sales: pd.DataFrame,
    dim_customer: pd.DataFrame,
    dim_product: pd.DataFrame,
    fact_sf: pd.DataFrame,
    output_dir: Path = OUTPUT_DIR,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    customer_public = dim_customer.drop(columns=["_Behavior_Type"])
    fact_sales.to_csv(output_dir / "df_fact_sales.csv", index=False)
    customer_public.to_csv(output_dir / "df_dim_customer.csv", index=False)
    dim_product.to_csv(output_dir / "df_dim_product.csv", index=False)
    fact_sf.to_csv(output_dir / "df_fact_sf.csv", index=False)


def main() -> None:
    dim_product = create_product_dimension()
    dim_customer = create_customer_dimension()
    fact_sales = create_sales_fact(dim_customer, dim_product)
    fact_sf = create_salesforce_activity(dim_customer, fact_sales)

    fact_sales, dim_product, fact_sf = add_controlled_missing_values(fact_sales, dim_product, fact_sf)

    validate_data(fact_sales, dim_customer, dim_product, fact_sf)
    summarize(fact_sales, dim_customer, dim_product, fact_sf)
    save_outputs(fact_sales, dim_customer, dim_product, fact_sf)

    print(f"\nFiles saved to: {OUTPUT_DIR.resolve()}")

if __name__ == "__main__":
    main()
