"""
Load and manage water-saving tips from JSON
"""

import json
import os

# Find tips_database.json (in parent folder)
_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_script_dir)
TIPS_FILE = os.path.join(_project_root, "tips_database.json")


def load_tips():
    """Load tips from JSON file"""
    try:
        with open(TIPS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ tips_database.json not found at: {TIPS_FILE}")
        return {}


TIPS_DATABASE = load_tips()


def get_categories():
    """Return list of category names"""
    return list(TIPS_DATABASE.keys())


def get_tips_by_category(category):
    """Return all tips for one category"""
    return TIPS_DATABASE.get(category.lower(), [])


def get_tip_by_id(tip_id):
    """Find a single tip by ID"""
    for tips in TIPS_DATABASE.values():
        for tip in tips:
            if tip.get("id") == tip_id:
                return tip
    return None


def calculate_impact(completed_tip_ids):
    """Calculate total impact from completed tips"""
    litres_per_day = 0
    rupees_per_month = 0
    
    for tip_id in completed_tip_ids:
        tip = get_tip_by_id(tip_id)
        if tip:
            litres_per_day += tip.get("water_saved", 0)
            rupees_per_month += tip.get("cost_saved", 0)

    litres_per_month = litres_per_day * 30
    co2_per_month = round(litres_per_month / 1000 * 0.4, 2)

    return {
        "litres_per_day": litres_per_day,
        "litres_per_month": litres_per_month,
        "rupees_per_month": rupees_per_month,
        "co2_kg_per_month": co2_per_month,
    }