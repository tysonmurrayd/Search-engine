#!/usr/bin/env python3

CISA = [("Chemical Sector", ["chemicals", "petroleum", "oil and gas", "life sciences"]),
("Commercial Facilites Sector", ["advertisement", "entertainment and media", "entertainment", "media", "real estate", "retail"]),
("Communications Sector", ["telecommunications", "communications", "technology", "media"]),
("Critical Manufacturing Sector", ["metals and mining", "automation", "automotive", "oil and gas", "energy", "manufacturing", "metal", "metal manufacturing"]),
("Dams Sector", ["dams"]),
("Defense Industrial Base Sector", ["military", "private security", "security", "defence"]),
("Emergency Services Sector", ["emergency", "fire and rescue", "law enforcement", "emergency medical services"]),
("Energy Sector", ["energy", "oil and gas", "petrolium", "energy : oil and gas"]),
("Financial Services Sector", ["insurance", "financial services"]),
("Food And Agriculture Sector", ["agribusiness", "processed food", "food industry", "agriculture", "food"]),
("Government Facilities Sector", ["education", "courts", "electricity", "healthcare", "mail", "military", "public"]),
("Healthcare and Public Health Sector", ["health insurance", "managed healthcare", "pharmacy", "pharmaceutical", "healthcare", "health", "hospitals"]),
("Information Technology Sector", ["semiconductors", "computer hardware", "consumer electronics", "software and online services", "information technology", "technology", "software", "computer software", "cloud computing", "computer hardware"]),
("Nuclear Reactors, Materials, and Waste Sector", ["basic materials", "nuclear", "nuclear energy", "waste",
"waste disposal"]),
("Transportation Systems Sector", ["courier", "transportation", "motor transportation", "trucking", "transport"]),
("Water and Wastewater Systems Sector", ["environmental services", "water", "wastewater"])]

def find_cisa(dict):
	sectors = []
	try:
		industries = dict["Industry"]
	except Exception:
		print("no Industry field to work with")
		dict["CISA"] = sectors
		return dict

	if not isinstance(industries, list):
		industries = industries.split(",")

	if isinstance(industries, list):
		for industry in industries:
			for t in CISA:
				if industry.lower().strip() in t[1]:
					if t[0] not in sectors:
						sectors.append(t[0])
	else:
		for t in CISA:
			if industries.lower() in t[1]:
				if t[0] not in sectors:
					sectors.append(t[0])
	dict["CISA"] = sectors
	return dict
