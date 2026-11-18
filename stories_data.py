# Story data for the FINAL edition of news-image-20261118.
# Every story was reported on Wednesday 18 November 2026 by the cited wires
# (Reuters, AP, AFP, BBC, Al Jazeera and others); full-day collection with
# sources lives in the research notes. Figures are as reported that day.

REGIONS = {
    "NA": ("NORTH AMERICA", (29, 111, 184)),
    "SA": ("SOUTH AMERICA", (46, 158, 91)),
    "EU": ("EUROPE", (123, 79, 166)),
    "AF": ("AFRICA", (224, 138, 0)),
    "AS": ("ASIA", (192, 57, 43)),
    "OC": ("OCEANIA", (14, 149, 148)),
    "GL": ("GLOBAL", (90, 90, 90)),
}

# Leads: (region, topic, headline, summary, lat, lon, tile, caption)
LEADS = [
    ("AS", "WAR & SECURITY", "US and Iran Trade Fire Over the Gulf",
     "US fighter jets struck an IRGC missile launch site on Iran's Qeshm Island; "
     "Iran answered with drones on a US radar site in Bahrain — its third attack in "
     "a week — and on Kuwait's Ali al-Salem base. Hormuz shipping runs at just 43% "
     "of normal traffic.",
     26.8, 55.9, "gulf", "QESHM ISLAND · STRAIT OF HORMUZ"),
    ("EU", "WAR & SECURITY", "Kerch Bridge Span Falls Into the Sea",
     "A Ukrainian drone-and-missile strike, prepared over weeks and carried out in "
     "seven stages, partially collapsed the road span of the bridge linking Russia "
     "to annexed Crimea. Moscow hit bridges in Kyiv in reply and vowed to rebuild "
     "the 19 km crossing.",
     45.3, 36.5, "bridge", "KERCH STRAIT · 19 KM CROSSING"),
    ("AS", "POLITICS", "Xi Hosts Putin in Shenzhen; Trump to Join",
     "Xi Jinping received Vladimir Putin at the APEC summit in Shenzhen, pitching "
     "free trade and a multipolar order. Donald Trump, fresh from Manila, joins "
     "them on Thursday for the first summit ever held between the three leaders.",
     22.5, 114.1, "summit", "SHENZHEN · APEC SUMMIT"),
]

# Secondaries: (region, topic, headline, summary, lat, lon, viz)
# viz: None or ("bars", [(label, value, color), ...], max) or ("gauge", frac, label)
SECONDARIES = [
    ("NA", "ECONOMY & TECH", "Nvidia Beats Forecasts, Guides $130bn",
     "A very solid quarter; Q4 revenue forecast at $130 billion. The board ruled "
     "out founder Jensen Huang's return as CEO.",
     37.4, -121.9, None),
    ("AS", "POLITICS", "Knesset Elects Kahana Speaker, 66 of 120",
     "Matan Kahana, an Eisenkot ally, won with backing from Arab parties — a "
     "setback for the Netanyahu camp.",
     31.8, 35.2, ("fillbar", 66, 120, "66 OF 120 SEATS")),
    ("AF", "HEALTH", "Ebola Cases More Than Double Past 11,000",
     "DR Congo's outbreak passes 11,000 cases and 5,400 deaths in three months, "
     "the UN said. Under-fives are hit hardest.",
     0.5, 29.5, None),
    ("NA", "HEALTH", "US Loses Measles-Free Status After 26 Years",
     "A record 5,400+ cases and 10 deaths — a first since the early 1990s — "
     "ended US measles elimination status.",
     38.9, -77.0, None),
    ("OC", "CLIMATE", "Cyclone Xavier Hits the Cooks at Category 5",
     "Gusts reached 315 km/h over Manihiki as Xavier crossed the Northern Cook "
     "Islands at Category 5.",
     -10.4, -161.0, ("gauge", 315 / 320, "315 KM/H GUSTS")),
    ("GL", "MARKETS", "Stocks Slide as Gulf Fire Rattles Markets",
     "The S&P 500 fell 1.03% to 7,340.53; the VIX jumped 11% to 25.46. Brent "
     "$91.55; gold fell 2.31% to $3,775.",
     40.7, -74.0, None),
    ("NA", "POLITICS", "Peltola Flips Alaska; Senate Goes 56–44",
     "Mary Peltola beat incumbent Dan Sullivan, capping the midterm rout: "
     "Democrats hold the Senate 56–44 from January.",
     58.3, -134.4, ("bars", [("DEM", 56, (29, 111, 184)), ("REP", 44, (178, 34, 52))], 100)),
    ("AS", "POLITICS", "Mongolia's President to Quit in Rail Scandal",
     "President Khurelsukh announced his resignation over $25m railway-contract "
     "accusations he denies.",
     47.9, 106.9, None),
    ("AS", "POLITICS", "Trump Opens Asia Trip With Manila Deals",
     "Trump met Philippine and Quad partners, announced a 'very large' "
     "Philippines deal and a zero-tariff Thailand pact.",
     14.6, 121.0, None),
]

# By the Numbers: (figure, caption)
NUMBERS = [
    ("66 of 120", "votes elect Kahana as Knesset speaker"),
    ("$130bn", "Nvidia's Q4 revenue forecast"),
    ("315 km/h", "Cyclone Xavier's peak gusts, Cook Islands"),
    ("11,000+", "Ebola cases in DR Congo, 5,400 dead"),
]

TICKER = ("S&P 500 -1.03%  |  BRENT $91.55  |  GOLD $3,775  |  VIX 25.46 (+11%)  |  "
          "HORMUZ TRAFFIC 43% OF NORMAL  |  BTC $64,649")

DECK = ("Strikes in the Gulf and on the Kerch Bridge, a three-way summit in Shenzhen "
        "and a chipmaker guiding $130bn")

# Also-list: (region, lead-in, clause, lat, lon)
ALSO = [
    ("NA", "Waymo halts freeway robotaxis", "DMV cites zone entries", 37.8, -122.4),
    ("NA", "Anthropic to list on Nasdaq", "debut set for Nov 19", 37.7, -122.3),
    ("NA", "27 years for Iran-backed plot", "Merchant sentenced in NY", 40.8, -73.9),
    ("SA", "Amazon group emerges hungry", "20 Awá leave isolation", -4.5, -45.5),
    ("SA", "Argentina rout Costa Rica 7–0", "three players score twice", -34.6, -58.4),
    ("SA", "Venezuela props up bolívar", "$12bn oil revenue spent", 10.5, -66.9),
    ("EU", "146,000 join French protests", "CGT claims 500,000", 48.9, 2.3),
    ("EU", "UK inflation rises to 3.6%", "fuel pushes factory costs up", 51.5, -0.1),
    ("EU", "Deutsche Bank leak: 15m files", "blind eye to crime alleged", 50.1, 8.7),
    ("EU", "Five EU states plan Rwanda hubs", "HRW denounces plan", -1.9, 30.1),
    ("EU", "England beat Spain 3–2", "ends a 43-match unbeaten run", 40.4, -3.7),
    ("AF", "Uganda targets $2.97bn rail", "272 km Kenya line", 0.3, 32.6),
    ("AF", "Africa loses $125bn a year", "AU counts illicit flows", 9.0, 38.7),
    ("AF", "Cassava seeks $1bn for AI centres", "GPU build-out", -17.8, 31.1),
    ("AF", "Fela Kuti enters Rock Hall", "first African inductee", 6.5, 3.4),
    ("AS", "ASEAN sees sea code by next year", "talks 80% agreed", -6.2, 106.8),
    ("AS", "An-12 crash kills 19 in Siberia", "military transport down", 55.3, 86.1),
    ("AS", "World Court to rule on Myanmar", "Rohingya verdict Thu", 16.8, 96.2),
    ("AS", "India beat Pakistan 2–1", "record 10th SAFF title, Dhaka", 23.8, 90.4),
    ("OC", "Fiji declares drought disaster", "El Niño grip tightens", -18.1, 178.4),
    ("OC", "M6.0 quake hits Papua New Guinea", "Wednesday tremor", -9.5, 147.2),
]

# Markets box: (name, level, change, down?)
MARKETS = [
    ("S&P 500", "7,340.53", "-1.03%", True),
    ("NASDAQ", "24,328.38", "-0.74%", True),
    ("FTSE 100", "10,689.87", "-1.76%", True),
    ("DAX", "26,045.37", "-2.08%", True),
    ("NIKKEI 225", "59,024.28", "+0.28%", False),
    ("BRENT", "$91.55", "-1.71%", True),
    ("GOLD", "$3,775", "-2.31%", True),
    ("VIX", "25.46", "+11.13%", False),
    ("BITCOIN", "$64,649", "+0.08%", False),
    ("ETHEREUM", "$1,811.81", "-0.88%", True),
]

FOOTER = ("Every story happened or was first reported on Wednesday 18 November 2026. "
          "Disputed claims are attributed, not stated as fact. Sources: Reuters · AP · AFP · "
          "BBC · Al Jazeera · UN · WHO · Der Spiegel · Le Monde. Original drawings.")
