"""
GARUDA AI - Crime Intelligence Platform
Synthetic Crime Database Generator for Karnataka State Crime Analytics
Generates realistic FIRs, Offenders, Victims, Financial Transactions, and Network Data
"""
import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "crime_database.db"

# =========================================================================
# Karnataka Neighborhoods with Socioeconomic Profiles
# =========================================================================
NEIGHBORHOODS = [
    ("Koramangala", 3.2, 5.5, 6, "High", 12.9714, 77.6227),
    ("Indiranagar", 2.8, 4.1, 4, "High", 12.9784, 77.6408),
    ("Jayanagar", 3.5, 6.2, 5, "Medium", 12.9308, 77.5838),
    ("Majestic", 12.5, 24.8, 0, "Low", 12.9767, 77.5713),
    ("Kalyan Nagar", 4.8, 9.5, 3, "Medium", 13.0256, 77.6379),
    ("Peenya", 11.2, 22.0, 1, "Low", 13.0296, 77.5195),
    ("Shivaji Nagar", 9.5, 18.5, 2, "Medium", 12.9857, 77.6057),
    ("Whitefield", 3.0, 5.0, 5, "High", 12.9698, 77.7500),
    ("Electronic City", 4.0, 7.2, 4, "Medium", 12.8452, 77.6602),
    ("Hebbal", 5.5, 10.0, 3, "Medium", 13.0358, 77.5970),
    ("Yelahanka", 6.2, 12.5, 2, "Low", 13.1007, 77.5963),
    ("Banashankari", 4.5, 8.8, 4, "Medium", 12.9255, 77.5468),
]

# =========================================================================
# Crime Types with Detailed Modus Operandi
# =========================================================================
OFFENSES = {
    "Burglary": {
        "mo": [
            "Forced entry through rear balcony door using crowbar. Targeted cash and jewelry.",
            "Entered locked apartment by picking key locks during daytime when occupants were at work.",
            "Smashed glass door of commercial electronics showroom, bypassed silent alarm, fled in van.",
            "Deactivated main power line, scaled boundary wall, entered through master bedroom window.",
            "Tailgated delivery agent into gated community, pried open locked wood doors of villa.",
            "Used duplicate keys obtained from former domestic help to enter residence during vacation.",
            "Cut through iron grille of ground floor bathroom window, ransacked locker room.",
        ],
        "severity": ["High", "High", "Critical", "High", "Medium"],
        "financial_range": (50000, 800000)
    },
    "Robbery": {
        "mo": [
            "Two suspects on black Pulsar motorcycle snatched gold chain from elderly woman on morning walk.",
            "Accused cornered pedestrian in dark underpass, threatened with long knife, demanded wallet and phone.",
            "Armed heist at jewelry store. Suspects masked, held staff at gunpoint, filled bags with gold ornaments.",
            "Snatched laptop bag from commuter waiting for auto-rickshaw, threatened violence, fled on scooter.",
            "Intercepted cash transport van near ATM, sprayed pepper spray on guards, stole cash trunk.",
            "Posed as Swiggy delivery executive, forced entry when door opened, robbed at knifepoint.",
            "Highway robbery near toll plaza - stopped car pretending accident, robbed occupants at gunpoint.",
        ],
        "severity": ["Critical", "High", "Critical", "High", "Critical"],
        "financial_range": (10000, 1500000)
    },
    "Narcotics Sale": {
        "mo": [
            "Peddling synthetic drugs (MDMA/LSD) to college students near cafes and pubs via encrypted chats.",
            "Hand-to-hand transaction of cannabis (Ganja) near public playground behind bus stop.",
            "Selling contraband pills from local paan shop hidden under counter merchandise.",
            "Undercover buy-bust operation: suspect arrested delivering cocaine packet at hotel lobby.",
            "Drop-off system: drugs taped under park bench, money sent via UPI transfer to merchant account.",
            "Interstate drug courier intercepted at Majestic bus stand with 5kg ganja in luggage.",
            "Dark web marketplace operator running crypto-based drug delivery network from apartment.",
        ],
        "severity": ["High", "Medium", "High", "Critical", "High"],
        "financial_range": (5000, 200000)
    },
    "Assault": {
        "mo": [
            "Bar brawl escalated over trivial issue, suspect hit victim on head with beer bottle, fled scene.",
            "Road rage incident: two drivers got into physical fight after minor bumper collision.",
            "Neighborhood dispute over parking space escalated; suspect assaulted victim with iron rod.",
            "Group of local youths cornered and assaulted college student near bus stand due to old rivalry.",
            "Domestic altercation turned violent inside private residence, neighbours called police helpline.",
            "Stalking victim for weeks, assaulted when confronted outside office premises.",
            "Gang rivalry led to public street fight involving machetes near commercial market.",
        ],
        "severity": ["Medium", "Low", "High", "Medium", "Medium"],
        "financial_range": (0, 10000)
    },
    "Cyber Fraud": {
        "mo": [
            "Phishing scam targeting senior citizens: suspect posed as bank manager, got OTP, withdrew funds.",
            "Part-time job scam: victims promised high returns for liking YouTube videos, asked to deposit fees.",
            "SIM swap fraud: cloned victim's SIM card to bypass two-factor authentication on net banking.",
            "Identity theft: created fake social media profiles of businessmen to solicit money from contacts.",
            "Ransomware attack on local clinic database, demanding payment in cryptocurrency for data decryption.",
            "Fake investment app promising 30% monthly returns, Ponzi scheme defrauding 200+ victims.",
            "WhatsApp/Telegram group running fake stock tips, charging membership and front-running trades.",
            "QR code scam at petrol pump - customer scanned 'payment' QR that debited their account.",
        ],
        "severity": ["High", "High", "Critical", "High", "Critical"],
        "financial_range": (100000, 5000000)
    },
    "Extortion": {
        "mo": [
            "Goon representing local gang demanded weekly 'hafta' (protection money) from street vendors.",
            "Sent threatening letters and WhatsApp calls demanding money from builder, claiming gang allegiance.",
            "Blackmailed victim using morphed private photographs, demanding digital payment.",
            "Threatened local shopkeeper with destruction of property if extortion demands not met.",
            "Demanded bribe and ransom under threat of filing false police cases against businessman.",
            "Land mafia sent goons to threaten farmer with dire consequences unless land transferred.",
            "Kidnapped businessman's son, demanded ransom via crypto wallet, released after 48 hours.",
        ],
        "severity": ["High", "High", "Critical", "High", "Critical"],
        "financial_range": (20000, 500000)
    },
    "Vehicle Theft": {
        "mo": [
            "Hotwired parked two-wheeler using master key from unguarded parking lot at night.",
            "Broke car window in IT park basement parking, bypassed ignition with relay device.",
            "Stole delivery bike with keys left in ignition while driver was inside apartment complex.",
            "Organized racket: stolen vehicles repainted and sold with forged RC in neighboring districts.",
            "Used signal jammer to prevent car central locking, stole laptop and documents from car.",
        ],
        "severity": ["Medium", "High", "Medium", "Critical", "Medium"],
        "financial_range": (30000, 1200000)
    },
    "Murder": {
        "mo": [
            "Contract killing: hired assailant shot victim outside residence. Motive linked to business dispute.",
            "Domestic violence escalated fatally. Husband stabbed wife during argument, neighbours witnessed.",
            "Gang rivalry resulted in public shooting near Majestic market. Victim was rival gang informer.",
            "Honor killing: family members conspired to murder daughter's partner from different community.",
            "Drunken brawl at local bar turned fatal when accused struck victim's head with heavy object.",
        ],
        "severity": ["Critical", "Critical", "Critical", "Critical", "Critical"],
        "financial_range": (0, 50000)
    },
}

# Kannada translations for bilingual support
KANNADA_DETAILS = {
    "Burglary": "ಮನೆಯ ಹಿಂಭಾಗದ ಕಿಟಕಿ/ಬಾಗಿಲನ್ನು ಮುರಿದು ಒಳನುಗ್ಗಿದ ಕಳ್ಳರು ಒಡವೆ ಮತ್ತು ಹಣವನ್ನು ಕದ್ದಿದ್ದಾರೆ.",
    "Robbery": "ದ್ವಿಚಕ್ರ ವಾಹನದಲ್ಲಿ ಬಂದ ಅಪರಿಚಿತರು ವೃದ್ಧೆಯ ಕುತ್ತಿಗೆಯಿಂದ ಚಿನ್ನದ ಸರವನ್ನು ಕಿತ್ತುಕೊಂಡು ಪರಾರಿಯಾಗಿದ್ದಾರೆ.",
    "Narcotics Sale": "ಕಾಲೇಜು ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಮಾದಕ ವಸ್ತುಗಳನ್ನು ವಾಟ್ಸಾಪ್ ಮೂಲಕ ಮಾರಾಟ ಮಾಡುತ್ತಿದ್ದವರನ್ನು ಬಂಧಿಸಲಾಗಿದೆ.",
    "Assault": "ಬಾರ್‌ನಲ್ಲಿ ಮಾತಿಗೆ ಮಾತು ಬೆಳೆದು ಆರೋಪಿಯು ಬೀಯರ್ ಬಾಟಲಿಯಿಂದ ಹಲ್ಲೆ ನಡೆಸಿ ತಪ್ಪಿಸಿಕೊಂಡಿದ್ದಾನೆ.",
    "Cyber Fraud": "ಬ್ಯಾಂಕ್ ಮ್ಯಾನೇಜರ್ ಎಂದು ಹೇಳಿ ನಕಲಿ ಒಟಿಪಿ ಪಡೆದು ಖಾತೆಯಿಂದ ಹಣ ವರ್ಗಾವಣೆ ಮಾಡಿಕೊಳ್ಳಲಾಗಿದೆ.",
    "Extortion": "ಗೂಂಡಾಗಳು ಕೊಲೆ ಬೆದರಿಕೆ ಹಾಕಿ ವಾರಕ್ಕೊಮ್ಮೆ ಹಫ್ತಾ ಕೊಡುವಂತೆ ಸುಲಿಗೆ ಮಾಡಿದ್ದಾರೆ.",
    "Vehicle Theft": "ರಾತ್ರಿ ಸಮಯದಲ್ಲಿ ಪಾರ್ಕಿಂಗ್ ಪ್ರದೇಶದಿಂದ ದ್ವಿಚಕ್ರ ವಾಹನವನ್ನು ಕಳ್ಳತನ ಮಾಡಲಾಗಿದೆ.",
    "Murder": "ವ್ಯಾಪಾರ ವಿವಾದದ ಹಿನ್ನೆಲೆಯಲ್ಲಿ ಸೂಪಾರಿ ಕೊಲೆಗಾರನಿಂದ ಗುಂಡಿಕ್ಕಿ ಕೊಲೆ ಮಾಡಲಾಗಿದೆ.",
}

# =========================================================================
# Offender Pool (Detailed Criminal Profiles)
# =========================================================================
OFFENDERS_POOL = [
    {"name": "Ramesh Kumar", "age": 28, "gender": "Male", "history": "2 prior arrests for mobile snatching", "gang": "Majestic Boys", "mo": "Chain snatching on two-wheelers"},
    {"name": "Syed Akbar", "age": 34, "gender": "Male", "history": "Convicted once for burglary, out on bail", "gang": "Kalyan Nagar Syndicate", "mo": "Daytime house burglaries"},
    {"name": "Manjunath 'Loco' Swamy", "age": 25, "gender": "Male", "history": "1 arrest for assault, known street fighter", "gang": "Majestic Boys", "mo": "Extortion and physical assaults"},
    {"name": "Vikram Malhotra", "age": 41, "gender": "Male", "history": "Arrested in 2024 for phishing scam", "gang": "Cyber Syndicate 404", "mo": "Phishing and bank OTP fraud"},
    {"name": "Ayesha Begum", "age": 23, "gender": "Female", "history": "No priors, suspect in money mule network", "gang": "Cyber Syndicate 404", "mo": "UPI money laundering and cash withdrawal"},
    {"name": "Preetham Shetty", "age": 30, "gender": "Male", "history": "3 arrests for narcotics peddling", "gang": "Kalyan Nagar Syndicate", "mo": "LSD/MDMA delivery to college students"},
    {"name": "Naveen 'Kariya' Gowda", "age": 29, "gender": "Male", "history": "Known gang leader, multiple extortion cases", "gang": "Majestic Boys", "mo": "Extortion, protection money rackets"},
    {"name": "Sanjay Singh", "age": 32, "gender": "Male", "history": "Burglary suspect, arrest warrant outstanding", "gang": "None", "mo": "Nighttime apartment lock breaking"},
    {"name": "Kartik Reddy", "age": 27, "gender": "Male", "history": "Arrested once for road rage, anger issues", "gang": "None", "mo": "Assault over petty arguments"},
    {"name": "Deepak 'Pinto' D'Souza", "age": 35, "gender": "Male", "history": "2 prior cases of drug trafficking", "gang": "Kalyan Nagar Syndicate", "mo": "Bulk drug supply from Goa to Bengaluru"},
    {"name": "Ananya Hegde", "age": 26, "gender": "Female", "history": "Arrested for credit card cloning in 2025", "gang": "Cyber Syndicate 404", "mo": "Cloning and online payment gateway hacks"},
    {"name": "Harish Prasad", "age": 45, "gender": "Male", "history": "White collar crime history, tax evasion", "gang": "None", "mo": "Real estate fraud, forging land documents"},
    {"name": "Shivaraj 'Katari' M.", "age": 31, "gender": "Male", "history": "Aggravated assault charges, gang member", "gang": "Majestic Boys", "mo": "Armed robbery, knife attacks"},
    {"name": "Farhan Khan", "age": 24, "gender": "Male", "history": "1 prior arrest for drug peddling", "gang": "Kalyan Nagar Syndicate", "mo": "Selling Ganja to techies"},
    {"name": "Kiran Kumar", "age": 28, "gender": "Male", "history": "Theft and housebreaking", "gang": "None", "mo": "Prying open sliding windows"},
    {"name": "Suresh 'Beedi' Naik", "age": 38, "gender": "Male", "history": "Murder accused, acquitted on technicality", "gang": "Majestic Boys", "mo": "Contract killings and intimidation"},
    {"name": "Ravi Teja", "age": 22, "gender": "Male", "history": "Vehicle theft ring operator", "gang": "None", "mo": "Two-wheeler theft using master keys"},
    {"name": "Mohammed Irfan", "age": 29, "gender": "Male", "history": "2 prior cyber fraud arrests", "gang": "Cyber Syndicate 404", "mo": "Fake investment app operations"},
    {"name": "Lakshmi Devi", "age": 33, "gender": "Female", "history": "Arrested for hawala operations", "gang": "Kalyan Nagar Syndicate", "mo": "Money laundering via shell companies"},
    {"name": "Ganesh 'Rowdy' Shettar", "age": 36, "gender": "Male", "history": "7 criminal cases, history offender", "gang": "Majestic Boys", "mo": "Land grabbing and extortion"},
]

# =========================================================================
# Victim Pool
# =========================================================================
VICTIMS_POOL = [
    {"name": "Shantha Bai", "age": 67, "gender": "Female", "occupation": "Retired Teacher"},
    {"name": "Rajesh Nambiar", "age": 38, "gender": "Male", "occupation": "Software Engineer"},
    {"name": "Dr. Sunitha Rao", "age": 45, "gender": "Female", "occupation": "Medical Professional"},
    {"name": "Anil Kulkarni", "age": 52, "gender": "Male", "occupation": "Bank Manager"},
    {"name": "Sneha Deshpande", "age": 22, "gender": "Female", "occupation": "College Student"},
    {"name": "Mohammed Yusuf", "age": 42, "gender": "Male", "occupation": "Shop Owner"},
    {"name": "Vijay Shankar", "age": 31, "gender": "Male", "occupation": "Delivery Executive"},
    {"name": "Ranganath Gowda", "age": 58, "gender": "Male", "occupation": "Real Estate Agent"},
    {"name": "Meera Sen", "age": 29, "gender": "Female", "occupation": "UX Designer"},
    {"name": "Girish Patel", "age": 35, "gender": "Male", "occupation": "Restaurant Manager"},
    {"name": "Kavitha Murthy", "age": 44, "gender": "Female", "occupation": "School Principal"},
    {"name": "Prakash Hegde", "age": 55, "gender": "Male", "occupation": "Retired Army Officer"},
    {"name": "Divya Sharma", "age": 26, "gender": "Female", "occupation": "Marketing Executive"},
    {"name": "Nagaraj S.", "age": 48, "gender": "Male", "occupation": "Auto Driver"},
    {"name": "Fatima Begum", "age": 60, "gender": "Female", "occupation": "Homemaker"},
]

# =========================================================================
# Event Contexts for Seasonal/Event-based Crime Analysis
# =========================================================================
EVENTS = [
    ("None", 0.55),
    ("Kadalekai Parishe (Groundnut Festival)", 0.08),
    ("New Year Eve Celebration", 0.08),
    ("IPL T20 Cricket Match", 0.07),
    ("Heavy Monsoon Inundation", 0.06),
    ("Dasara Festival Week", 0.06),
    ("Election Campaign Period", 0.05),
    ("Ugadi Festival", 0.05),
]

# =========================================================================
# Database Generation Function
# =========================================================================
def generate_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop existing tables
    tables = ["neighborhoods", "firs", "offenders", "victims", 
              "fir_offenders", "fir_victims", "financial_transactions"]
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")

    # Create tables with enhanced schema
    cursor.execute("""
    CREATE TABLE neighborhoods (
        name TEXT PRIMARY KEY,
        unemployment_rate REAL,
        poverty_rate REAL,
        youth_recreation_centers INTEGER,
        police_patrol_density TEXT,
        latitude REAL,
        longitude REAL
    )""")

    cursor.execute("""
    CREATE TABLE firs (
        fir_id TEXT PRIMARY KEY,
        crime_type TEXT,
        date TEXT,
        time TEXT,
        location TEXT,
        neighborhood TEXT,
        modus_operandi TEXT,
        status TEXT,
        severity TEXT,
        financial_loss REAL,
        event_context TEXT,
        details_en TEXT,
        details_kn TEXT,
        FOREIGN KEY (neighborhood) REFERENCES neighborhoods(name)
    )""")

    cursor.execute("""
    CREATE TABLE offenders (
        offender_id TEXT PRIMARY KEY,
        name TEXT,
        age INTEGER,
        gender TEXT,
        criminal_history TEXT,
        status TEXT,
        gang_affiliation TEXT,
        typical_mo TEXT,
        risk_score INTEGER,
        bank_account TEXT
    )""")

    cursor.execute("""
    CREATE TABLE victims (
        victim_id TEXT PRIMARY KEY,
        name TEXT,
        age INTEGER,
        gender TEXT,
        occupation TEXT
    )""")

    cursor.execute("""
    CREATE TABLE fir_offenders (
        fir_id TEXT,
        offender_id TEXT,
        role TEXT,
        PRIMARY KEY (fir_id, offender_id),
        FOREIGN KEY (fir_id) REFERENCES firs(fir_id),
        FOREIGN KEY (offender_id) REFERENCES offenders(offender_id)
    )""")

    cursor.execute("""
    CREATE TABLE fir_victims (
        fir_id TEXT,
        victim_id TEXT,
        PRIMARY KEY (fir_id, victim_id),
        FOREIGN KEY (fir_id) REFERENCES firs(fir_id),
        FOREIGN KEY (victim_id) REFERENCES victims(victim_id)
    )""")

    cursor.execute("""
    CREATE TABLE financial_transactions (
        transaction_id TEXT PRIMARY KEY,
        fir_id TEXT,
        sender_account TEXT,
        receiver_account TEXT,
        amount REAL,
        date TEXT,
        transaction_type TEXT,
        FOREIGN KEY (fir_id) REFERENCES firs(fir_id)
    )""")

    # Populate Neighborhoods
    cursor.executemany(
        "INSERT INTO neighborhoods VALUES (?, ?, ?, ?, ?, ?, ?)", NEIGHBORHOODS
    )

    # Populate Offenders
    offenders_data = []
    for idx, off in enumerate(OFFENDERS_POOL):
        offender_id = f"OFF-2026-{1000 + idx}"
        bank_acc = f"ACC-{random.randint(100000, 999999)}"
        risk_score = random.randint(5, 10) if off["gang"] != "None" else random.randint(1, 6)
        status = random.choice(["Arrested", "On Bail", "Absconding", "Under Trial", "Wanted"])
        offenders_data.append((
            offender_id, off["name"], off["age"], off["gender"], off["history"],
            status, off["gang"], off["mo"], risk_score, bank_acc
        ))
    cursor.executemany("INSERT INTO offenders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", offenders_data)

    # Populate Victims
    victims_data = []
    for idx, vic in enumerate(VICTIMS_POOL):
        victim_id = f"VIC-2026-{1000 + idx}"
        victims_data.append((victim_id, vic["name"], vic["age"], vic["gender"], vic["occupation"]))
    cursor.executemany("INSERT INTO victims VALUES (?, ?, ?, ?, ?)", victims_data)

    # Build ID maps
    offender_records = [o[0] for o in offenders_data]
    offender_map = {o[0]: o for o in offenders_data}
    victim_ids = [v[0] for v in victims_data]

    # Generate 120 FIRs for rich analytics
    start_date = datetime(2026, 1, 1)
    fir_list = []
    fir_offender_list = []
    fir_victim_list = []
    transaction_list = []
    valid_neighborhoods = [n[0] for n in NEIGHBORHOODS]

    for i in range(1, 121):
        fir_id = f"FIR-2026-{2000 + i}"
        crime_type = random.choice(list(OFFENSES.keys()))
        off_info = OFFENSES[crime_type]

        # Neighborhood distribution based on crime type
        if crime_type == "Narcotics Sale":
            neighborhood = random.choices(["Indiranagar", "Koramangala", "Kalyan Nagar", "Whitefield"], weights=[0.4, 0.3, 0.2, 0.1])[0]
        elif crime_type == "Cyber Fraud":
            neighborhood = random.choices(["Koramangala", "Whitefield", "Electronic City", "Indiranagar"], weights=[0.3, 0.3, 0.2, 0.2])[0]
        elif crime_type == "Burglary":
            neighborhood = random.choices(["Peenya", "Jayanagar", "Banashankari", "Yelahanka"], weights=[0.3, 0.3, 0.2, 0.2])[0]
        elif crime_type == "Extortion":
            neighborhood = random.choices(["Majestic", "Shivaji Nagar", "Peenya", "Hebbal"], weights=[0.35, 0.3, 0.2, 0.15])[0]
        elif crime_type == "Vehicle Theft":
            neighborhood = random.choices(["Electronic City", "Whitefield", "Koramangala", "Hebbal"], weights=[0.3, 0.3, 0.2, 0.2])[0]
        elif crime_type == "Murder":
            neighborhood = random.choices(["Majestic", "Peenya", "Shivaji Nagar", "Yelahanka"], weights=[0.35, 0.25, 0.25, 0.15])[0]
        else:
            neighborhood = random.choice(valid_neighborhoods)

        mo = random.choice(off_info["mo"])
        severity = random.choice(off_info["severity"])
        financial_loss = random.randint(*off_info["financial_range"])

        # Random date in first 6 months of 2026
        delta_days = random.randint(0, 175)
        crime_date = start_date + timedelta(days=delta_days)
        crime_date_str = crime_date.strftime("%Y-%m-%d")
        hour = random.randint(0, 23)
        minute = random.choice([0, 15, 30, 45])
        crime_time_str = f"{hour:02d}:{minute:02d}"

        # Assign event context
        event_name = random.choices([e[0] for e in EVENTS], weights=[e[1] for e in EVENTS])[0]
        if "New Year" in event_name:
            crime_date_str = "2026-01-01"
            hour = random.randint(0, 4)
            crime_time_str = f"{hour:02d}:{minute:02d}"

        location = f"{random.randint(1, 100)}, {random.choice(['Main Road', 'Cross Road', 'Link Road', 'Industrial Area', 'Gated Layout', '1st Stage', '2nd Block'])}, {neighborhood}"
        status = random.choices(
            ["Under Investigation", "Chargesheeted", "Arrested", "Closed", "Cold Case"],
            weights=[0.35, 0.25, 0.20, 0.12, 0.08]
        )[0]

        details_en = f"Incident at {location}. MO: {mo}. Estimated loss: Rs. {financial_loss}. Status: {status}."
        kn_mo = KANNADA_DETAILS.get(crime_type, "ಅಪರಾಧ ವಿವರಗಳು ಲಭ್ಯವಿಲ್ಲ.")
        details_kn = f"ಘಟನೆಯು {location} ನಲ್ಲಿ ನಡೆದಿದೆ. ವಿಧಾನ: {kn_mo} ಅಂದಾಜು ನಷ್ಟ ರೂ. {financial_loss}. ಸ್ಥಿತಿ: {status}."

        fir_list.append((
            fir_id, crime_type, crime_date_str, crime_time_str, location,
            neighborhood, mo, status, severity, financial_loss, event_name, details_en, details_kn
        ))

        # Link offenders to crimes based on MO matching
        relevant_offenders = []
        for off_id in offender_records:
            off_rec = offender_map[off_id]
            off_mo = off_rec[7].lower()
            if crime_type == "Narcotics Sale" and "drug" in off_mo:
                relevant_offenders.append(off_id)
            elif crime_type == "Cyber Fraud" and any(k in off_mo for k in ["phishing", "cloning", "upi", "investment"]):
                relevant_offenders.append(off_id)
            elif crime_type == "Burglary" and "burglar" in off_mo:
                relevant_offenders.append(off_id)
            elif crime_type == "Robbery" and any(k in off_mo for k in ["snatching", "robbery", "knife"]):
                relevant_offenders.append(off_id)
            elif crime_type == "Extortion" and "extortion" in off_mo:
                relevant_offenders.append(off_id)
            elif crime_type == "Vehicle Theft" and "theft" in off_mo:
                relevant_offenders.append(off_id)
            elif crime_type == "Murder" and any(k in off_mo for k in ["killing", "intimidation", "contract"]):
                relevant_offenders.append(off_id)

        if not relevant_offenders:
            relevant_offenders = random.sample(offender_records, min(5, len(offender_records)))

        # Assign 1-3 offenders per crime to build network links
        num_accused = random.choices([1, 2, 3], weights=[0.5, 0.35, 0.15])[0]
        chosen_offenders = random.sample(relevant_offenders, min(num_accused, len(relevant_offenders)))

        for o_idx, off_id in enumerate(chosen_offenders):
            role = "Mastermind" if o_idx == 0 and len(chosen_offenders) > 1 else random.choice(["Executor", "Lookout", "Accomplice"])
            fir_offender_list.append((fir_id, off_id, role))

            # Generate financial transactions between gang members
            off_rec = offender_map[off_id]
            gang = off_rec[6]
            if gang != "None" and len(chosen_offenders) > 1:
                for other_id in chosen_offenders:
                    if other_id != off_id and offender_map[other_id][6] == gang:
                        tx_id = f"TX-2026-{10000 + len(transaction_list)}"
                        tx_amount = financial_loss * random.uniform(0.1, 0.4)
                        tx_type = random.choice(["UPI Transfer", "Cash Deposit", "NEFT", "Hawala", "Crypto"])
                        transaction_list.append((
                            tx_id, fir_id, off_rec[9], offender_map[other_id][9],
                            round(tx_amount, 2), crime_date_str, tx_type
                        ))
                        break

        # Link victims
        num_vic = random.choices([1, 2], weights=[0.85, 0.15])[0]
        chosen_victims = random.sample(victim_ids, num_vic)
        for vic_id in chosen_victims:
            fir_victim_list.append((fir_id, vic_id))

    # Insert all data
    cursor.executemany("INSERT INTO firs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", fir_list)
    cursor.executemany("INSERT INTO fir_offenders VALUES (?, ?, ?)", fir_offender_list)
    cursor.executemany("INSERT INTO fir_victims VALUES (?, ?)", fir_victim_list)
    cursor.executemany("INSERT INTO financial_transactions VALUES (?, ?, ?, ?, ?, ?, ?)", transaction_list)

    conn.commit()

    # Print statistics
    cursor.execute("SELECT COUNT(*) FROM firs")
    print(f"Total FIRs: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM offenders")
    print(f"Total Offenders: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM financial_transactions")
    print(f"Total Transactions: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM fir_offenders")
    print(f"Total FIR-Offender Links: {cursor.fetchone()[0]}")

    conn.close()
    print("✅ Synthetic crime database generated successfully!")


if __name__ == "__main__":
    generate_database()
