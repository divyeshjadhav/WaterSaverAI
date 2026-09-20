"""
Fallback answers when Ollama is offline
"""

FALLBACK = {
    "bathroom": """🚿 **Bathroom tips for a {family_size} household**

1. **5-minute showers** – saves ~40 L/day per person (₹120/month). Set a phone timer.
2. **Bucket bath** – 20-30 L instead of 100 L for a long shower (~50 L/day saved).
3. **Tap off while brushing** – a running tap wastes 6 L/minute (~15 L/day saved).

💡 Bathrooms use about 35% of home water, so this is the best place to start!

Would you like tips for the toilet flush as well?""",

    "kitchen": """🍽️ **Kitchen tips for your {housing_type}**

1. **Two-tub method** – one tub to wash, one to rinse. Saves ~35 L/day vs running tap (₹105/month).
2. **Tap aerator (₹100)** – cuts flow by 50% with the same pressure (~15 L/day).
3. **Reuse rinse water** – water from washing rice/vegetables is perfect for plants (~10 L/day).

Do you wash utensils by hand or use a dishwasher?""",

    "laundry": """👕 **Laundry tips for {family_size}**

1. **Full loads only** – half loads waste almost as much water (~30 L/day saved).
2. **Fixed wash days** – e.g. Mon / Thu / Sat instead of daily (~50 L/day, ₹150/month).
3. **Reuse final rinse water** – great for mopping floors (~25 L/day).

Each machine load uses 100-150 L, so fewer loads = big savings.

How many loads do you run per week right now?""",

    "leak": """🔧 **Leaks – fix these FIRST!**

- One dripping tap wastes **30-90 L/day** (up to 2,700 L/month).
- A silent toilet leak can waste **100-400 L/day**.

**Toilet leak test:** put a few drops of food colour in the tank. If colour appears in the bowl within 10 minutes, it leaks.

**Fix cost:** tap washer ₹10-20 (DIY) or plumber ₹150-300.
**Payback:** less than one month.

Have you noticed any dripping taps at home?""",

    "outdoor": """🌱 **Garden / outdoor tips**

1. **Water before 8 AM** – evaporation drops by ~40% (~30 L/day saved).
2. **Bucket car wash** – 40 L instead of 150 L with a hose.
3. **Mulch around plants** – dry leaves keep soil moist longer (~20 L/day).

For apartments: use leftover kitchen rinse water for balcony plants.

Do you have a garden, or mainly balcony plants?""",

    "challenge": """🏆 **Your 7-Day Bucket Challenge**

- **Duration:** 7 days
- **Daily action:** Replace ONE shower with a bucket bath for every family member.
- **Expected saving:** ~350 L/week for a {family_size} household (≈ ₹150/month).
- **Reward:** +1 conservation score when you finish!

Ready to start today?""",

    "progress": """📊 **Your progress**

- Conservation score: **{score}/10**
- Water saved: **{water_saved} L/day** (≈ {monthly} L/month)
- That's about **{buckets} buckets** of water every month!

**Next step:** click "Mark done" on one more tip below to raise your score.

Which area would you like to tackle next?""",

    "general": """💧 **Top 3 quick wins for your home**

1. **Fix any dripping tap** – up to 90 L/day saved.
2. **5-minute showers / bucket baths** – ~40-50 L/day per person.
3. **Two-tub utensil washing** – ~35 L/day.

Together that's roughly **100+ L/day = ₹300+/month** for a {family_size} household.

Which of these would you like to try first?""",
}


def fallback_response(intent, user_profile, stats):
    """Return a pre-written answer"""
    template = FALLBACK.get(intent, FALLBACK["general"])
    litres = stats.get("litres_per_day", 0)
    return template.format(
        family_size=user_profile.get("family_size", "3-4 people"),
        housing_type=user_profile.get("housing_type", "home"),
        score=stats.get("score", 5),
        water_saved=litres,
        monthly=litres * 30,
        buckets=(litres * 30) // 15 if litres > 0 else 0,
    )