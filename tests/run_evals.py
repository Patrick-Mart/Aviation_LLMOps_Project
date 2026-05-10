import json
import os

eval_data = [
    # --- REGULATION 1008/2008 (Licensing & Commercial) ---
    {
        "id": 1,
        "regulation": "1008/2008",
        "question": "What are the main conditions for an air carrier to be granted an operating licence?",
        "expected_articles": ["Article 4"],
        "expected_keywords": ["principal place of business", "AOC", "financial fitness", "insurance"]
    },
    {
        "id": 2,
        "regulation": "1008/2008",
        "question": "Where must an undertaking's principal place of business be located to get a license?",
        "expected_articles": ["Article 4", "Article 2"],
        "expected_keywords": ["Member State", "effective control", "registered office"]
    },
    {
        "id": 3,
        "regulation": "1008/2008",
        "question": "How long is an operating licence valid for?",
        "expected_articles": ["Article 8"],
        "expected_keywords": ["valid as long as", "conditions", "competent licensing authority"]
    },
    {
        "id": 4,
        "regulation": "1008/2008",
        "question": "What are the requirements regarding air fare transparency and price display?",
        "expected_articles": ["Article 23"],
        "expected_keywords": ["final price", "taxes", "airport charges", "non-discriminatory"]
    },
    {
        "id": 5,
        "regulation": "1008/2008",
        "question": "Can a licensing authority suspend a license if an undertaking can no longer meet its financial obligations?",
        "expected_articles": ["Article 8", "Article 9"],
        "expected_keywords": ["suspension", "revocation", "financial fitness", "insolvency"]
    },
    {
        "id": 6,
        "regulation": "1008/2008",
        "question": "What are the rules for leasing aircraft from another country?",
        "expected_articles": ["Article 13"],
        "expected_keywords": ["wet lease", "dry lease", "safety standards", "exceptional needs"]
    },
    {
        "id": 7,
        "regulation": "1008/2008",
        "question": "Explain the concept of 'Public Service Obligations' (PSO) in this regulation.",
        "expected_articles": ["Article 16", "Article 17"],
        "expected_keywords": ["scheduled air services", "peripheral region", "tender", "exclusive concession"]
    },

    # --- REGULATION 1107/2006 (Rights of Disabled Persons) ---
    {
        "id": 8,
        "regulation": "1107/2006",
        "question": "Can an air carrier refuse a booking based on a person's reduced mobility?",
        "expected_articles": ["Article 3", "Article 4"],
        "expected_keywords": ["refusal of carriage", "safety requirements", "size of the aircraft"]
    },
    {
        "id": 9,
        "regulation": "1107/2006",
        "question": "Who is responsible for providing assistance to disabled persons at airports?",
        "expected_articles": ["Article 8"],
        "expected_keywords": ["managing body", "airport", "responsibility", "points of arrival"]
    },
    {
        "id": 10,
        "regulation": "1107/2006",
        "question": "Is there a charge for the assistance provided to disabled persons at the airport?",
        "expected_articles": ["Article 8"],
        "expected_keywords": ["free of charge", "airport charge", "specific levy", "proportionate"]
    },
    {
        "id": 11,
        "regulation": "1107/2006",
        "question": "How much advance notice must a passenger give to ensure they receive assistance?",
        "expected_articles": ["Article 7"],
        "expected_keywords": ["48 hours", "advance notification", "air carrier", "agent"]
    },
    {
        "id": 12,
        "regulation": "1107/2006",
        "question": "What training requirements exist for staff dealing with persons with reduced mobility?",
        "expected_articles": ["Article 11"],
        "expected_keywords": ["disability-awareness", "disability-assistance", "training courses"]
    },
    {
        "id": 13,
        "regulation": "1107/2006",
        "question": "What happens if an airport loses or damages a wheelchair during handling?",
        "expected_articles": ["Article 12"],
        "expected_keywords": ["compensation", "mobility equipment", "international law", "national law"]
    },

    # --- COMPARISON & NEGATIVE TESTS ---
    {
        "id": 14,
        "regulation": "Both",
        "question": "Compare how 1008/2008 and 1107/2006 address the concept of non-discrimination.",
        "expected_articles": ["Article 23 (1008)", "Article 3 (1107)"],
        "expected_keywords": ["pricing", "residence", "nationality", "disability", "refusal of carriage"]
    },
    {
        "id": 15,
        "regulation": "Negative",
        "question": "What are the rules for maritime shipping cargo between Denmark and Norway?",
        "expected_articles": [],
        "expected_keywords": ["not mentioned", "out of scope", "only aviation"]
    }
]

eval_path = os.path.join("tests", "eval_tests.json")

with open(eval_path, "w", encoding="utf-8") as f:
    json.dump(eval_data, f, indent=4)

print("eval_tests.json has been created successfully.")