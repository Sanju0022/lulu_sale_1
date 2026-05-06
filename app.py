import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

# ── Config ────────────────────────────────────────────────────────────────────
NUM_ROWS = 1200
OUTPUT_FILE = "lulu_hypermart_dubai_sales.csv"

# ── Reference Data ────────────────────────────────────────────────────────────
PRODUCT_CATEGORIES = {
    "Electronics":    ["Samsung 65\" QLED TV", "Apple iPhone 15", "Sony PlayStation 5", "Dell Laptop i7",
                       "Huawei Tablet", "JBL Bluetooth Speaker", "Canon DSLR Camera", "LG Refrigerator",
                       "Dyson Vacuum Cleaner", "Xiaomi Smart Watch"],
    "Clothing":       ["Men's Linen Kandura", "Women's Abaya (Black)", "Kids' School Uniform", "Nike Running Shoes",
                       "Adidas Track Suit", "H&M Casual T-Shirt", "Zara Formal Dress", "Levis Denim Jeans",
                       "Under Armour Sports Bra", "Quiksilver Swim Shorts"],
    "Dairy":          ["Full Cream Milk 1L", "Greek Yoghurt 500g", "Cheddar Cheese Block", "Fresh Butter 250g",
                       "Labneh 400g", "Low-Fat Milk 2L", "Mozzarella 200g", "Cream Cheese 150g",
                       "Flavoured Yoghurt Duo", "Condensed Milk 400ml"],
    "Grocery":        ["Basmati Rice 5kg", "Sunflower Oil 3L", "Whole Wheat Bread", "Macaroni 500g",
                       "Tomato Paste 400g", "Lentils 1kg", "Chickpeas 800g", "Brown Sugar 1kg",
                       "Sea Salt 500g", "Mixed Spices Pack"],
    "Fresh Produce":  ["Organic Apples 1kg", "Imported Strawberries 250g", "Egyptian Dates 500g",
                       "Avocado 4-Pack", "Baby Spinach 200g", "Mixed Salad Leaves", "Mango 1kg",
                       "Cherry Tomatoes 500g", "Broccoli Head", "Fresh Mushrooms 250g"],
    "Beverages":      ["Lipton Green Tea 100s", "Nescafé Gold 200g", "Pepsi 2.25L", "Volvic Water 12-Pack",
                       "Red Bull 4-Pack", "Tropicana Orange Juice 1L", "Al Ain Water 6L",
                       "Aloe Vera Drink 500ml", "Coconut Water 330ml", "Mango Juice 1.5L"],
    "Personal Care":  ["Dove Body Wash 500ml", "Head & Shoulders Shampoo", "Nivea Men Face Wash",
                       "Oral-B Toothbrush", "Colgate Total Toothpaste", "Gillette Fusion Razor",
                       "Neutrogena Sunscreen SPF50", "L'Oréal Conditioner", "Dettol Soap 6-Pack",
                       "Always Pads Overnight"],
    "Home & Kitchen": ["Tefal Non-Stick Pan", "Pyrex Glass Set 3pc", "Philips Rice Cooker",
                       "IKEA Storage Boxes", "Milton Steel Lunch Box", "Prestige Pressure Cooker",
                       "Nespresso Pod 10-Pack", "Brita Water Filter", "Joseph Joseph Chopping Board",
                       "Kitchen Towel Roll 6-Pack"],
    "Baby Products":  ["Pampers Diapers L 52s", "Huggies Wipes 3-Pack", "Johnson's Baby Shampoo",
                       "Aptamil Formula Stage 2", "Farlin Baby Bottle 260ml", "Chicco Feeding Spoon Set",
                       "Mothercare Baby Blanket", "Dettol Baby Liquid Soap", "Graco Baby Monitor",
                       "MAM Pacifier 2-Pack"],
    "Sports & Fitness": ["Adidas Yoga Mat", "Decathlon Resistance Bands", "Protein Whey Powder 1kg",
                         "Nike Water Bottle 750ml", "Under Armour Gym Gloves", "Fitbit Inspire 3",
                         "Wilson Tennis Racket", "Speedo Swimming Goggles", "Reebok Ankle Weights",
                         "GNC Multivitamin 90 Tabs"],
}

CUSTOMER_SEGMENTS = ["Premium", "Regular", "Budget", "Loyalty Member", "Corporate", "Tourist"]
SEG_WEIGHTS       = [0.12, 0.35, 0.20, 0.18, 0.08, 0.07]

PAYMENT_METHODS   = ["Cash", "Credit Card", "Debit Card", "Apple Pay", "Samsung Pay", "LuLu Gift Card"]
STORE_LOCATIONS   = ["Al Barsha", "Deira City Centre", "Dubai Festival City", "Mirdif City Centre",
                     "Al Ghurair", "Ras Al Khor", "Dragon Mart", "Silicon Oasis"]
GENDER            = ["Male", "Female"]
NATIONALITIES     = ["Emirati", "Indian", "Pakistani", "Filipino", "Egyptian", "British",
                     "American", "Bangladeshi", "Sri Lankan", "Jordanian"]

# Unit price ranges per category (AED)
PRICE_RANGES = {
    "Electronics":      (150,  5500),
    "Clothing":         (25,   450),
    "Dairy":            (3,    35),
    "Grocery":          (2,    50),
    "Fresh Produce":    (3,    45),
    "Beverages":        (4,    60),
    "Personal Care":    (8,    120),
    "Home & Kitchen":   (20,   600),
    "Baby Products":    (15,   280),
    "Sports & Fitness": (25,   900),
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def random_date(start, end):
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

def generate_transaction_id(i):
    return f"LLU-DXB-{str(i+1).zfill(6)}"

def generate_customer_id():
    return f"CUST-{random.randint(10000, 99999)}"

# ── Build Dataset ─────────────────────────────────────────────────────────────
start_date = datetime(2023, 1, 1)
end_date   = datetime(2024, 12, 31)

records = []
for i in range(NUM_ROWS):
    category    = random.choice(list(PRODUCT_CATEGORIES.keys()))
    product     = random.choice(PRODUCT_CATEGORIES[category])
    segment     = random.choices(CUSTOMER_SEGMENTS, weights=SEG_WEIGHTS, k=1)[0]
    unit_price  = round(random.uniform(*PRICE_RANGES[category]), 2)

    # Quantity influenced by category and segment
    if category in ("Grocery", "Dairy", "Beverages", "Personal Care"):
        qty = random.randint(1, 10)
    elif category == "Electronics":
        qty = random.randint(1, 3)
    else:
        qty = random.randint(1, 5)

    discount_pct = 0.0
    if segment == "Loyalty Member":
        discount_pct = random.choice([0.05, 0.10, 0.15])
    elif segment == "Premium":
        discount_pct = random.choice([0.0, 0.05])
    elif segment == "Budget":
        discount_pct = random.choice([0.0, 0.05, 0.10, 0.20])

    gross_sales  = round(unit_price * qty, 2)
    discount_amt = round(gross_sales * discount_pct, 2)
    net_sales    = round(gross_sales - discount_amt, 2)

    records.append({
        "Transaction_ID":    generate_transaction_id(i),
        "Date":              random_date(start_date, end_date).strftime("%Y-%m-%d"),
        "Store_Location":    random.choice(STORE_LOCATIONS),
        "Customer_ID":       generate_customer_id(),
        "Customer_Segment":  segment,
        "Product_Category":  category,
        "Product_Name":      product,
        "Quantity":          qty,
        "Unit_Price_AED":    unit_price,
        "Gross_Sales_AED":   gross_sales,
        "Discount_Pct":      discount_pct,
        "Net_Sales_AED":     net_sales,
        "Payment_Method":    random.choice(PAYMENT_METHODS),
        "Customer_Gender":   random.choice(GENDER),
        "Customer_Nationality": random.choice(NATIONALITIES),
    })

df = pd.DataFrame(records).sort_values("Date").reset_index(drop=True)

# ── Save ──────────────────────────────────────────────────────────────────────
df.to_csv(OUTPUT_FILE, index=False)

print(f"✅  Dataset saved → {OUTPUT_FILE}")
print(f"   Rows : {len(df):,}")
print(f"   Cols : {len(df.columns)}")
print(f"\nColumn list:\n{df.dtypes.to_string()}")
print(f"\nSample (5 rows):\n{df.head().to_string()}")
print(f"\nNet Sales summary (AED):\n{df['Net_Sales_AED'].describe().round(2).to_string()}")
