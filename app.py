import pandas as pd
import geopandas as gpd
import pyfpgrowth
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import folium
from folium.plugins import MarkerCluster

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load the data
districts_gdf = gpd.read_file(r'C:\\Users\\msm76\\Desktop\\Training\\cleaned\\RiyadhDistricts.topojson')
realestate_data = pd.read_csv(r'C:\\Users\\msm76\\Desktop\\Training\\cleaned\\CleanedandCombined.csv')
arabic_to_english_mapping = {
        "السويدى": "Al Swaidi","المهدية": "Al Mahdiah","الزهرة": "Alzahrah","الملقا": "Al Malga","الخير": None,"النظيم": "Al Natheem",
        "النخيل": "Al Nakheel","شرق الرياض": None,"عريض": "Al Ared", "طريق الخرج": None,
        "نمار": "Nammar", "الملك عبد الله": "Al Malik Abdullah", "قرطبة": "Qurtubah", "الجنادرية": "Al Jinadiriyah", "عرقه": "Irgah","الشفاء": "Shafa",
        "الربيع": "Al Rabia",
        "الجرادية": None,
        "العارض": "Al Ared",
        "الرمال": "Al Rimal",
        "العزيزية": "Al Aziziyah",
        "المرسلات": "Al Mursalat",
        "المعذر": "Al Mather",
        "القدس": "Al Quds",
        "الصحافة": "Al Sahafa",
        "الملز": "Al Malaz",
        "الياسمين": "Al Yasmeen",
        "الدار البيضاء": "Al Dar Al Baidaa",
        "العود": "Al Oud",
        "البديعة": "Al Badiah",
        "عكاظ": "Okadh",
        "لبن": "Laban",
        "الشرفية": "Al Sharafiyah",
        "الشميسى": "Al Shimaisi",
        "الملك فهد": "Al Malik Fahad",
        "المونسية": "Al Mounasiah",
        "النهضة": "Al Nahdah",
        "حطين": "Hitteen",
        "غرناطة": "Ghernata",
        "النرجس": "Al Nargas",
        "اشبيليا": "Ishbayliyah",
        "الحمراء": "Al Hamra",
        "شبرا": "Shobra",
        "الشهداء": "Al Shuhada",
        "العوالي": None,
        "الملك فيصل": "Al Malik Faisal",
        "النسيم": "Al Naseem",
        "ام الحمام": "Um Al Hamam Al Sharqi",
        "القادسية": "Al Qadisiyah",
        "الزهراء": "Al Zahraa",
        "الغنامية": None,
        "الورود": "Al Worood",
        "المروة": None,
        "الخليج": "Al Khaleej",
        "بدر": "Badr",
        "السليمانية": "As Sulimaniyah",
        "أحد": "Ohod",
        "العريجاء": "Al Uraija",
        "البرية": None,
        "الفيصلية": "Al Faisaliyah",
        "منفوحة": "Manfuha",
        "المصيف": "Al Maseef",
        "طويق": "Tuwaiq",
        "الرفيعة": "Al Rafiah",
        "الروضة": "Al Rawabi",
        "غبيراء": "Ghubairah",
        "الوزارات": "Al Wazarat",
        "الضباط": "Al Dhobbat",
        "الرابية": "Al Rabia",
        "سكيرينة": None,
        "البيان": None,
        "المصفاة": None,
        "اليرموك": "Al Yarmouk",
        "الازدهار": "Al Izdihar",
        "الريان": "Al Rayan",
        "الروابى": "Al Rawabi",
        "التعاون": "Al Taawon",
        "ديراب": "Dirab",
        "العقيق": "Al Akeek",
        "ثليم": None,
        "طيبة": None,
        "الندى": "Al Nada",
        "عتيقة": "Otaigah",
        "جرير": "Jareer",
        "الحزم": "Hazim",
        "السعادة": "Al Saadah",
        "المغرزات": "Al Mugharazat",
        "الصفاء": "Al Safaa",
        "الاندلس": "Al Andalus",
        "الخزامى": "Al Khozami",
        "الغدير": "Al Ghadeer",
        "الحائر": None,
        "الفيحاء": "Al Faihaa",
        "هيت": None,
        "المشاعل": "Al Mishael",
        "الجزيرة": "Al Jazirah",
        "القيروان": "Ghairawan",
        "أخرى": None,
        "خنشليلة": None,
        "المنار": "Al Manar",
        "السلى": "Al Silay",
        "الصالحية": None,
        "النخبة": None,
        "اليمامة": "Yamamah",
        "الهدا": "Al Hada",
        "الزهور": None,
        "الامانة": None,
        "الربوة": "Al Rabwa",
        "العليا": "Al Olaya",
        "دعكنة": None,
        "العمل": None,
        "النفل": "Al Nafal",
        "السلام": "Al Salam",
        "المنصورة": "Mansora",
        "سلطانة": "Sultanah",
        "الخالدية": "Al Khalidiah",
        "المحمدية": "Al Mohamadiyah",
        "ام سليم": None,
        "الواحة": "Al Waha",
        "الشرق": None,
        "الوادي": "Al Wadi",
        "النزهة": "Al Nuzha",
        "المناخ": "Al Manakh",
        "المروج": "Al Morooj",
        "الدريهمية": "Derihmiyah",
        "المدينة الصناعية الجديدة": "Second Industrial City in Riyadh",
        "الملك عبدالعزيز": "Al Malik Abdulaziz",
        "الصناعية": "First Industrial City in Riyadh",
        "الغروب": None,
        "الرائد": "Al Raid",
        "المربع": "Al Murabba",
        "صياح": "Seyah",
        "صلاح الدين": "Salah Aldin",
        "الناصرية": None,
        "الراية": None,
        "العلا": None,
        "الدوبية": None,
        "الفاروق": "Al Farook",
        "المعيزلية": "Al Muayzilah",
        "المنصورية": "Mansora",
        "النور": None,
        "المشرق": None,
        "سدرة": None,
        "المرقب": "Al Marqab",
        "الطويلعة": None,
        "الدرعية": None,
        "المصانع": "Al Masanee",
        "الشعلة": None,
        "الرحمانية": "Al Rahmaniyah",
        "الشعاب": None,
        "الفرسان": None,
        "النموذجية": "Al Namodhajiyah",
        "3419": None,
        "البطحاء": None,
        "المؤتمرات": None,
        "الندوة": None,
        "بنبان": None,
        "الديرة": "Al Deerah",
        "ام الشعال": None,
        "الوشام": "Al Wesham",
        "الرسالة": None,
        "مطار الملك خالد الدولى": None,
        "عليشة": "Ulaysha",
        "طريق الحجاز": None,
        "السحاب": None,
        "الوسام": None,
        "الشميسي": "Al Shimaisi",
        "معكال": None,
        "إشبيلية": "Ishbayliyah",
        "أم الحمام الغربي": "Um Al Hamam Al Gharbi",
        "جبره": None,
        "حلة بن دايل": None,
        "الفاخرية": None,
        "مدينة الملك عبدالله بن عبد العزيز للطاقة": None,
        "الشمال": None,
        "الفوطة": "Al Foutah",
        "المعارض": None,
        "الطندباوى": None,
        "طريق خريص": None,
        "غرب المطار": None}

# Define categorization functions
def categorize_price(price):
    bins = [0, 300000, 690000, 1200000, float('inf')]
    labels = ['Low price', 'Mid price', 'High price', 'Very High price']
    return pd.cut([price], bins=bins, labels=labels)[0]

def categorize_space(space):
    bins = [0, 286.79, 375, 600, float('inf')]
    labels = ['Small space', 'Medium space', 'Large space', 'Extra Large space']
    return pd.cut([space], bins=bins, labels=labels)[0]

def get_detailed_price_per_meter_interval(row):
    price_per_meter = row['price'] / row['space sqm']
    if price_per_meter < 500:
        return '0 - 499'
    elif 500 <= price_per_meter < 1000:
        return '500 - 999'
    elif 1000 <= price_per_meter < 1500:
        return '1000 - 1499'
    elif 1500 <= price_per_meter < 2000:
        return '1500 - 1999'
    elif 2000 <= price_per_meter < 2500:
        return '2000 - 2499'
    elif 2500 <= price_per_meter < 3000:
        return '2500 - 2999'
    elif 3000 <= price_per_meter < 3500:
        return '3000 - 3499'
    elif 3500 <= price_per_meter < 4000:
        return '3500 - 3999'
    else:
        return '4000 and above'

# Categorize price and space in the dataset
realestate_data['price_per_meter_interval'] = realestate_data.apply(get_detailed_price_per_meter_interval, axis=1)
realestate_data['price_category'] = pd.cut(realestate_data['price'], bins=[0, 300000, 690000, 1200000, float('inf')], labels=['Low price', 'Mid price', 'High price', 'Very High price'], right=False)
realestate_data['space_category'] = pd.cut(realestate_data['space sqm'], bins=[0, 286.79, 375, 600, float('inf')], labels=['Small space', 'Medium space', 'Large space', 'Extra Large space'], right=True)
print(realestate_data.head())

# Prepare transactions data
transactions = realestate_data.apply(lambda x: [x['estateType'], x['estateCategory'], str(x['district']), x['price_category'], x['space_category'], x['price_per_meter_interval']], axis=1).tolist()

# Find frequent patterns
patterns = pyfpgrowth.find_frequent_patterns(transactions, support_threshold=25)

# Generate association rules
min_length = 4
filtered_patterns = {k: v for k, v in patterns.items() if len(k) >= min_length}
rules = pyfpgrowth.generate_association_rules(filtered_patterns, confidence_threshold=0.5)

# Calculate support, confidence, and lift
total_transactions = len(transactions)
rules_list = []
for antecedent, consequent_conf in rules.items():
    consequent, confidence = consequent_conf
    antecedent_support = patterns[antecedent] / total_transactions
    antecedent_consequent = tuple(sorted(antecedent + consequent))
    if antecedent_consequent in patterns:
        rule_support = patterns[antecedent_consequent] / total_transactions
    else:
        rule_support = 0
    rules_list.append({
        'antecedent': antecedent,
        'consequent': consequent,
        'support': rule_support,
        'confidence': confidence,
    })

rules_df = pd.DataFrame(rules_list)

# Define the filter function
def filter_rules(rules, queDict, realestate_data):
    filtered_rules = rules.copy()
    estateType = queDict.get('estateType')
    price_category = queDict.get('price_category')
    space_category = queDict.get('space_category')
    price_per_meter_interval = realestate_data['price_per_meter_interval'].unique()
    districts = realestate_data['district'].unique()
    
    filtered_rules['antecedent_len'] = rules['antecedent'].apply(lambda x: len(x))
    filtered_rules['consequent_len'] = rules['consequent'].apply(lambda x: len(x))
    
    if estateType is not None:
        filtered_rules = filtered_rules[
            filtered_rules['antecedent'].apply(lambda x: any(district in x for district in districts) and
            (estateType in x if estateType is not None else True) and
            (price_category in x if price_category is not None else True) and
            (space_category in x if space_category is not None else True) and
            any(pr in x for pr in price_per_meter_interval))
        ]
    
    return filtered_rules.sort_values(by='consequent_len', ascending=False)

# Define the function to find districts in rules
def find_districts_in_rules(rules, districts):
    # Set to hold districts found in the rules
    districts_found = set()
    price_per_meter_interval_found = set()
    price_per_meter_interval_unique = realestate_data['price_per_meter_interval'].unique()
    
    # Function to check and collect districts in a row
    def check_districts(row):
        for p in price_per_meter_interval_unique:
            if p in row['antecedent'] or p in row['consequent']:
                price_per_meter_interval_found.add(p)
        for district in districts:
            if district in row['antecedent'] or district in row['consequent']:
                districts_found.add(district)
    print(price_per_meter_interval_found)
    # Apply the function across all rows
    rules.apply(check_districts, axis=1)
    # Add a new column 'district_english' to the dataframe using the mapping
    districts_found_eng = [arabic_to_english_mapping.get(district, district) for district in list(districts_found)]
    
    return list(districts_found_eng), list(price_per_meter_interval_found)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    estate_types = realestate_data['estateType'].unique().tolist()
    estate_categories = realestate_data['estateCategory'].unique().tolist()
    return templates.TemplateResponse("index.html", {"request": request, "estate_types": estate_types, "estate_categories": estate_categories})

@app.post("/district_price", response_class=JSONResponse)
async def district_price(
    request: Request,
    price_per_meter: float = Form(...),
    space: float = Form(...),
    estate_type: str = Form(...)
):
    price = price_per_meter * space
    price_category = categorize_price(price)
    space_category = categorize_space(space)
    price_per_meter_interval = get_detailed_price_per_meter_interval({'price': price, 'space sqm': space})

    queDict = {
        'estateType': estate_type,
        'price_category': price_category,
        'space_category': space_category,
        'price_per_meter_interval': price_per_meter_interval
    }

    filtered_rules = filter_rules(rules_df, queDict, realestate_data)
    found_districts, found_intervals = find_districts_in_rules(filtered_rules, realestate_data['district'].unique())
   

    # Create a dictionary to map districts to intervals using Arabic names
    district_to_interval = {}
    for _, rule in filtered_rules.iterrows():
        for district in realestate_data['district'].unique():
            if district in rule['antecedent'] or district in rule['consequent']:
                interval = next((i for i in found_intervals if i in rule['antecedent'] or i in rule['consequent']), 'Unknown')
                district_to_interval[district] = interval

    # Generate a folium map based on the user inputs
    folium_map = folium.Map(location=[24.7136, 46.6753], zoom_start=11)
    
    for idx, row in districts_gdf.iterrows():
        district_name_english = row['id']
        district_name_arabic = next((key for key, value in arabic_to_english_mapping.items() if value == district_name_english), district_name_english)
        if district_name_arabic in district_to_interval:
            interval = district_to_interval[district_name_arabic]
            geo_json = folium.GeoJson(
                data=row['geometry'].__geo_interface__,
                style_function=lambda x: {'fillColor': 'green', 'color': 'black', 'weight': 2, 'fillOpacity': 0.6}
            )
            popup_text = f"ID: {district_name_english}, Price Interval: {interval}"
        else:
            geo_json = folium.GeoJson(
                data=row['geometry'].__geo_interface__,
                style_function=lambda x: {'fillColor': 'blue', 'color': 'black', 'weight': 2, 'fillOpacity': 0.6}
            )
            popup_text = f"ID: {district_name_english}"
        
        popup = folium.Popup(popup_text, max_width=300)
        geo_json.add_child(popup)
        folium_map.add_child(geo_json)
    
    map_html = folium_map._repr_html_()
    if filtered_rules.empty:
        print('kys')
        return JSONResponse(content={
            'message':'There is no similar cases that we recorded, thus we have no recommended districts',
            "price_category": str(price_category),
            "space_category": str(space_category),
            "estate_type": estate_type,
            "filtered_rules": filtered_rules.to_html(),
            "found_districts": found_districts,
            "map_html": map_html
        })    
    return JSONResponse(content={
        "price_category": str(price_category),
        "space_category": str(space_category),
        "estate_type": estate_type,
        "filtered_rules": filtered_rules.to_html(),
        "found_districts": found_districts,
        "map_html": map_html
    })
