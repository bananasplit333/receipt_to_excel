image_paths = [
  "data/static/img/costco_1.png",
  "data/static/img/costco_3.jpg",
  "data/static/img/costco_2.png",
  "data/static/img/home_depot_1.jpg"
]

topHeadings = [
  "Groceries & Food",
  "Clothing & Fashion",
  "Home & Living",
  "Electronics & Appliances",
  "Health & Beauty",
  "Automotive",
  "Sports & Recreation",
  "Office & School Supplies",
  "Seasonal & Decorations",
  "Crafts & Party Supplies",
  "Other"
]

sample_resp = """
Groceries & Food
  ORG SUGAR, 8.49
  DC FIGS, 4.97
  DRIED PLUMS, 8.99
  HERSHEY NUGG, 11.75
  KS ORG CHERRY, 7.99
  KS WLH PEPPER, 4.99
  KS PURE SALT, 2.79
  KS GRINDER, 6.89
  KS ORG EGGS, 6.49
  ORGANIC CHIP, 5.89
  PEPSI COLA, 10.99
  SWIFR WET 64, 15.79
  KS FAB SOFT, 8.99
  DAWN PLATIN, 9.99
  TIDEPODS, 24.49
  WOODBRG MERL, 53.94
  WHOLE MILK, 3.35
  KS ORG EVOO, 9.49
  10LB SUGAR, 5.59
  DM GRN BEAN, 9.69
  ORG STRWBRY, 8.99
  VIENNA SAUSG, 7.99
  CHOC3PKBAR, 5.99
  NAE POT PIE, 10.89
  KS CAGE FREE, 3.39
  POLSKA KIELB, 11.79
  PANTENESHAMP, 9.99
  PANTENE COND, 9.99
  KS CRMB BCN, 8.89
  MIXED VEGG, 5.99
  KS SLCED HAM, 8.99
  RUMMO-8PK, 9.99
  KS GRD PEPPR, 3.99
  FR ONIONSOUP, 9.99
  VRTYMIXFRUIT, 7.99

Electronics & Appliances

Home & Living

Clothing & Accessories

Health & Beauty
"""

def get_topHeadings():
    return topHeadings