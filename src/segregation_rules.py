"""
MEDIGRATOR: AI-Driven Medical Waste Detection & Intelligent Segregation
Medical Waste Segregation Rules & Regulatory Knowledge Base
Aligned with:
  - Central Pollution Control Board (CPCB) Bio-Medical Waste Management Rules (2016 / 2018 Amendments)
  - World Health Organization (WHO) Safe Management of Wastes from Health-Care Activities

Maps all 14 detection classes recognized by the YOLO11 model to standard disposal categories,
bin color codes, hazard ratings, and disposal/treatment protocols.
"""

from typing import Dict, Any, List

# Official 14 classes recognized by the trained model
CLASSES: List[str] = [
    "fluid bottle",
    "gauze",
    "glass",
    "glove",
    "mask",
    "needle",
    "needle cap",
    "paper",
    "plastic",
    "scrub",
    "test tube",
    "tube",
    "unused gauze",
    "used syringe"
]

# Knowledge base detailing regulatory guidelines for each item
SEGREGATION_RULES: Dict[str, Dict[str, Any]] = {
    "needle": {
        "class_name": "needle",
        "display_name": "Hypodermic Needle (Sharps)",
        "bin_color": "White",
        "bin_hex": "#F8FAFC",
        "bin_border": "#94A3B8",
        "bin_text_color": "#0F172A",
        "badge_bg": "bg-slate-100",
        "badge_text": "text-slate-800",
        "badge_border": "border-slate-400",
        "category_title": "White Puncture-Proof Container (Sharps)",
        "hazard_level": "Critical",
        "hazard_color": "text-red-600 bg-red-50 border-red-200",
        "risk_description": "High puncture & bloodborne pathogen transmission hazard (HIV, Hepatitis B/C).",
        "treatment": "Autoclaving or Dry Heat Sterilization followed by shredding / Sharp Pit encapsulation.",
        "handling_instructions": [
            "Never re-cap needles manually using both hands.",
            "Use a needle burner / syringe cutter if available at point-of-use.",
            "Drop directly into puncture-proof, leak-proof, tamper-proof translucent sharps container.",
            "Do not exceed 3/4 fill capacity before sealing."
        ],
        "cpcb_schedule": "Schedule I: White (Translucent) - Waste Sharps including metals"
    },
    "used syringe": {
        "class_name": "used syringe",
        "display_name": "Used Syringe Barrel / Assembly",
        "bin_color": "White",
        "bin_hex": "#F8FAFC",
        "bin_border": "#94A3B8",
        "bin_text_color": "#0F172A",
        "badge_bg": "bg-slate-100",
        "badge_text": "text-slate-800",
        "badge_border": "border-slate-400",
        "category_title": "White Container (if needle attached) / Red Bin (barrel only)",
        "hazard_level": "High",
        "hazard_color": "text-red-500 bg-red-50 border-red-200",
        "risk_description": "Contaminated with blood, bodily fluids, or intravenous medication.",
        "treatment": "Cut needle at source into White container. Segregate plastic syringe barrel into Red bin for autoclaving/recycling.",
        "handling_instructions": [
            "Mutilate syringe needle tip using needle-destroyer immediately after injection.",
            "If needle cannot be safely detached, discard the entire unit into the White Sharps Container.",
            "Decontaminate plastic barrel before authorized plastic recycling.",
            "Never compress or crush by hand."
        ],
        "cpcb_schedule": "Schedule I: White (Sharps) / Red (Contaminated Plastic Barrels)"
    },
    "needle cap": {
        "class_name": "needle cap",
        "display_name": "Plastic Needle Cap",
        "bin_color": "Red",
        "bin_hex": "#EF4444",
        "bin_border": "#DC2626",
        "bin_text_color": "#FFFFFF",
        "badge_bg": "bg-red-50",
        "badge_text": "text-red-700",
        "badge_border": "border-red-300",
        "category_title": "Red Non-Chlorinated Bag / Bin (Recyclable Plastic)",
        "hazard_level": "Low",
        "hazard_color": "text-amber-600 bg-amber-50 border-amber-200",
        "risk_description": "Non-sharp medical plastic. Low biohazard unless contaminated with fresh blood.",
        "treatment": "Autoclaving / chemical disinfection with 1-2% Sodium Hypochlorite, then mechanical shredding and recycling.",
        "handling_instructions": [
            "Ensure the cap does not contain an unsheathed needle inside.",
            "Discard into red colored non-chlorinated plastic liner.",
            "Transport to authorized Common Bio-Medical / Healthcare Waste Treatment Facility (CBWTF)."
        ],
        "cpcb_schedule": "Schedule I: Red - Contaminated Waste (Recyclable Plastics)"
    },
    "gauze": {
        "class_name": "gauze",
        "display_name": "Soiled Surgical Gauze / Swab",
        "bin_color": "Yellow",
        "bin_hex": "#EAB308",
        "bin_border": "#CA8A04",
        "bin_text_color": "#78350F",
        "badge_bg": "bg-amber-50",
        "badge_text": "text-amber-800",
        "badge_border": "border-amber-300",
        "category_title": "Yellow Non-Chlorinated Bag (Infectious / Soiled)",
        "hazard_level": "High",
        "hazard_color": "text-orange-600 bg-orange-50 border-orange-200",
        "risk_description": "Heavily soaked with blood, pus, wound exudate, or pathological specimens.",
        "treatment": "Incineration in double-chamber incinerator (>1050°C) or Plasma Pyrolysis / Deep burial where permitted.",
        "handling_instructions": [
            "Use forceps or gloved hands to handle soiled swabs.",
            "Seal in non-chlorinated yellow plastic bags with biohazard symbol.",
            "Store in cold storage if holding time exceeds 48 hours."
        ],
        "cpcb_schedule": "Schedule I: Yellow - Soiled Waste (Items contaminated with blood/fluids)"
    },
    "unused gauze": {
        "class_name": "unused gauze",
        "display_name": "Unused / Clean Gauze Pack",
        "bin_color": "Black",
        "bin_hex": "#1E293B",
        "bin_border": "#0F172A",
        "bin_text_color": "#F8FAFC",
        "badge_bg": "bg-slate-100",
        "badge_text": "text-slate-700",
        "badge_border": "border-slate-300",
        "category_title": "Black Bin / Green Bin (General Waste)",
        "hazard_level": "Minimal",
        "hazard_color": "text-emerald-600 bg-emerald-50 border-emerald-200",
        "risk_description": "Clean, unsoiled cotton material with no patient contact.",
        "treatment": "Municipal solid waste disposal or textile recycling.",
        "handling_instructions": [
            "Verify the packaging was not opened in an isolation ward or exposed to pathogen aerosols.",
            "If contaminated by room contact in COVID/ICU ward, route to Yellow bin.",
            "Otherwise, dispose into general municipal collection."
        ],
        "cpcb_schedule": "Schedule I: General Solid Waste (Non-Biohazard)"
    },
    "glove": {
        "class_name": "glove",
        "display_name": "Latex / Nitrile Examination Glove",
        "bin_color": "Red",
        "bin_hex": "#EF4444",
        "bin_border": "#DC2626",
        "bin_text_color": "#FFFFFF",
        "badge_bg": "bg-red-50",
        "badge_text": "text-red-700",
        "badge_border": "border-red-300",
        "category_title": "Red Non-Chlorinated Bag / Bin (Recyclable Plastic & Rubber)",
        "hazard_level": "Moderate",
        "hazard_color": "text-amber-600 bg-amber-50 border-amber-200",
        "risk_description": "Contact barrier waste. Contaminated with patient surface organisms or bodily fluids.",
        "treatment": "Autoclaving or microwaving followed by shredding. Never incinerate chlorinated latex/PVC.",
        "handling_instructions": [
            "Peel gloves off inside-out without touching external contaminated surfaces.",
            "Deposit directly into red non-chlorinated bag.",
            "Perform immediate hand hygiene after doffing."
        ],
        "cpcb_schedule": "Schedule I: Red - Contaminated Recyclable Waste (Gloves, catheters, IV sets)"
    },
    "mask": {
        "class_name": "mask",
        "display_name": "Surgical / N95 Disposable Mask",
        "bin_color": "Yellow",
        "bin_hex": "#EAB308",
        "bin_border": "#CA8A04",
        "bin_text_color": "#78350F",
        "badge_bg": "bg-amber-50",
        "badge_text": "text-amber-800",
        "badge_border": "border-amber-300",
        "category_title": "Yellow Bag (Infectious PPE)",
        "hazard_level": "Moderate",
        "hazard_color": "text-amber-600 bg-amber-50 border-amber-200",
        "risk_description": "Traps respiratory droplets, aerosolized bacteria, and viral pathogens.",
        "treatment": "High-temperature incineration or autoclaving at 121°C for 30 minutes.",
        "handling_instructions": [
            "Remove by ear loops without touching the front filter fabric.",
            "Cut ear loops to prevent unauthorized re-use in informal markets.",
            "Place into yellow biohazard bag and tie securely."
        ],
        "cpcb_schedule": "Schedule I: Yellow - Soiled / Expired PPE Waste"
    },
    "scrub": {
        "class_name": "scrub",
        "display_name": "Medical Scrubs / Disposable Gown",
        "bin_color": "Yellow",
        "bin_hex": "#EAB308",
        "bin_border": "#CA8A04",
        "bin_text_color": "#78350F",
        "badge_bg": "bg-amber-50",
        "badge_text": "text-amber-800",
        "badge_border": "border-amber-300",
        "category_title": "Yellow Bag (Infectious Linen / Soiled Fabric)",
        "hazard_level": "Moderate",
        "hazard_color": "text-amber-600 bg-amber-50 border-amber-200",
        "risk_description": "Non-woven protective fabric exposed to fluids during surgery or procedures.",
        "treatment": "Disinfection via steam sterilizer / autoclave before incineration or deep burial.",
        "handling_instructions": [
            "Fold contaminated outward surface inward when rolling gown for disposal.",
            "Place in yellow biohazard container.",
            "If reusable fabric linen, send for designated high-heat hospital laundry with chlorine bleach."
        ],
        "cpcb_schedule": "Schedule I: Yellow - Soiled Waste (Bedding, contaminated clothing)"
    },
    "glass": {
        "class_name": "glass",
        "display_name": "Medicine Ampoule / Glass Vial",
        "bin_color": "Blue",
        "bin_hex": "#3B82F6",
        "bin_border": "#2563EB",
        "bin_text_color": "#FFFFFF",
        "badge_bg": "bg-blue-50",
        "badge_text": "text-blue-700",
        "badge_border": "border-blue-300",
        "category_title": "Blue Cardboard Box / Bin (Glassware & Medicine Vials)",
        "hazard_level": "High",
        "hazard_color": "text-blue-600 bg-blue-50 border-blue-200",
        "risk_description": "Laceration risk and chemical toxicity from residual medications/antibiotics.",
        "treatment": "Disinfection (soaking in 1-2% Sodium Hypochlorite or autoclaving) followed by recycling.",
        "handling_instructions": [
            "Discard into puncture-proof cardboard box or plastic bin marked with Blue label.",
            "Never mix broken glassware with general municipal trash or red bags.",
            "Rinse residual chemical contents before disposal if non-cytotoxic."
        ],
        "cpcb_schedule": "Schedule I: Blue - Glassware (Medicine vials, ampoules, glassware articles)"
    },
    "test tube": {
        "class_name": "test tube",
        "display_name": "Blood Collection Tube / Vacutainer",
        "bin_color": "Blue",
        "bin_hex": "#3B82F6",
        "bin_border": "#2563EB",
        "bin_text_color": "#FFFFFF",
        "badge_bg": "bg-blue-50",
        "badge_text": "text-blue-700",
        "badge_border": "border-blue-300",
        "category_title": "Blue Box (Glass Vacutainers) / Yellow (if blood specimen intact)",
        "hazard_level": "High",
        "hazard_color": "text-red-500 bg-red-50 border-red-200",
        "risk_description": "Pathology waste containing whole blood, serum, or laboratory cultures.",
        "treatment": "Pre-treatment with autoclave or microwave on-site at lab, followed by glass decontamination & recycling.",
        "handling_instructions": [
            "Ensure tube stoppers are tightly fitted to avoid blood spills during transit.",
            "Autoclave microbiology/pathology tubes on-site prior to final dispatch.",
            "Place in rigid blue container with biohazard markings."
        ],
        "cpcb_schedule": "Schedule I: Blue / Yellow - Microbiology & Clinical Specimen Glassware"
    },
    "fluid bottle": {
        "class_name": "fluid bottle",
        "display_name": "IV Fluid Saline / Solution Bottle",
        "bin_color": "Red",
        "bin_hex": "#EF4444",
        "bin_border": "#DC2626",
        "bin_text_color": "#FFFFFF",
        "badge_bg": "bg-red-50",
        "badge_text": "text-red-700",
        "badge_border": "border-red-300",
        "category_title": "Red Bin (Recyclable Polyethylene / Polypropylene)",
        "hazard_level": "Low",
        "hazard_color": "text-amber-600 bg-amber-50 border-amber-200",
        "risk_description": "Intravenous saline / dextrose containers. Non-infectious internal surface.",
        "treatment": "Autoclaving followed by cutting/shredding for secondary plastic pelletizing.",
        "handling_instructions": [
            "Empty any residual electrolyte/saline solution into hospital effluent drain.",
            "Detach and discard IV spikes/tubing into designated bins.",
            "Place plastic bottle in Red bin. Never send to general dump."
        ],
        "cpcb_schedule": "Schedule I: Red - Recyclable Plastic Bottles & Infusion Sets"
    },
    "tube": {
        "class_name": "tube",
        "display_name": "IV Tubing / Catheter / Suction Line",
        "bin_color": "Red",
        "bin_hex": "#EF4444",
        "bin_border": "#DC2626",
        "bin_text_color": "#FFFFFF",
        "badge_bg": "bg-red-50",
        "badge_text": "text-red-700",
        "badge_border": "border-red-300",
        "category_title": "Red Bag (Contaminated Flexible Tubing)",
        "hazard_level": "Moderate",
        "hazard_color": "text-amber-600 bg-amber-50 border-amber-200",
        "risk_description": "PVC/silicone lines exposed to blood, urine, or physiological fluids.",
        "treatment": "Autoclave / Microwave / Chemical disinfection followed by industrial shredding.",
        "handling_instructions": [
            "Drain internal fluid contents thoroughly before bagging.",
            "Cut into smaller segments if required by facility protocols to prevent tangled hoppers.",
            "Deposit in Red bin container."
        ],
        "cpcb_schedule": "Schedule I: Red - Tubing, catheters, intravenous sets"
    },
    "plastic": {
        "class_name": "plastic",
        "display_name": "Non-Bottle Medical Plastic Container",
        "bin_color": "Red",
        "bin_hex": "#EF4444",
        "bin_border": "#DC2626",
        "bin_text_color": "#FFFFFF",
        "badge_bg": "bg-red-50",
        "badge_text": "text-red-700",
        "badge_border": "border-red-300",
        "category_title": "Red Bin (Rigid Contaminated Plastics)",
        "hazard_level": "Moderate",
        "hazard_color": "text-amber-600 bg-amber-50 border-amber-200",
        "risk_description": "Clinical plastic packaging, trays, specimen cups, or rigid disposable containers.",
        "treatment": "Disinfection via autoclave, followed by shredding and controlled plastic recycling.",
        "handling_instructions": [
            "Empty residues and verify no sharps (blades/needles) are hidden inside.",
            "Discard into red non-chlorinated plastic liner.",
            "Keep covered in foot-pedal operated bins."
        ],
        "cpcb_schedule": "Schedule I: Red - Contaminated Recyclable Plastics"
    },
    "paper": {
        "class_name": "paper",
        "display_name": "Medical Paper / Towels / Prescription Sheets",
        "bin_color": "Black",
        "bin_hex": "#1E293B",
        "bin_border": "#0F172A",
        "bin_text_color": "#F8FAFC",
        "badge_bg": "bg-slate-100",
        "badge_text": "text-slate-700",
        "badge_border": "border-slate-300",
        "category_title": "Black Bin / Green Bin (General Municipal Waste)",
        "hazard_level": "Minimal",
        "hazard_color": "text-emerald-600 bg-emerald-50 border-emerald-200",
        "risk_description": "General administrative or dry packaging paper without bodily fluid contamination.",
        "treatment": "Municipal recycling or sanitary landfill.",
        "handling_instructions": [
            "Ensure sheets are not soaked with blood or infectious secretions (if so, put in Yellow bin).",
            "Shred patient-identifiable medical records in compliance with medical confidentiality (HIPAA / GDPR).",
            "Place into black or green municipal bin."
        ],
        "cpcb_schedule": "General Solid Waste (Municipal / Non-hazardous)"
    }
}


# Bin category metadata for summary dashboard
BIN_CATEGORIES_METADATA = {
    "Yellow": {
        "color_name": "Yellow",
        "hex": "#EAB308",
        "title": "Soiled & Infectious Waste",
        "icon": "biohazard",
        "border": "border-amber-400",
        "bg_soft": "bg-amber-50",
        "badge": "bg-amber-500 text-white",
        "treatment": "High-temperature Incineration (>1050°C) or Plasma Pyrolysis",
        "summary": "Items soaked in blood, pus, anatomical specimens, swabs, and infectious PPE."
    },
    "Red": {
        "color_name": "Red",
        "hex": "#EF4444",
        "title": "Contaminated Recyclable Plastics",
        "icon": "recycle",
        "border": "border-red-400",
        "bg_soft": "bg-red-50",
        "badge": "bg-red-600 text-white",
        "treatment": "Autoclaving / Chemical Disinfection followed by Shredding & Recycling",
        "summary": "Disposable gloves, IV bottles, tubing, catheters, plastic syringe barrels."
    },
    "White": {
        "color_name": "White (Translucent)",
        "hex": "#F1F5F9",
        "title": "Waste Sharps & Needles",
        "icon": "needle",
        "border": "border-slate-400",
        "bg_soft": "bg-slate-50",
        "badge": "bg-slate-200 text-slate-900 border border-slate-400",
        "treatment": "Autoclaving / Dry Heat Sterilization followed by Shredding / Sharp Pit",
        "summary": "Puncture-proof container for hypodermic needles, scalpels, and blades."
    },
    "Blue": {
        "color_name": "Blue",
        "hex": "#3B82F6",
        "title": "Glassware & Medicine Vials",
        "icon": "flask",
        "border": "border-blue-400",
        "bg_soft": "bg-blue-50",
        "badge": "bg-blue-600 text-white",
        "treatment": "Chemical Disinfection (Hypochlorite) / Autoclaving followed by Recycling",
        "summary": "Medicine ampoules, broken glass, vacutainers, and metallic orthopedic implants."
    },
    "Black": {
        "color_name": "Black / Green",
        "hex": "#1E293B",
        "title": "General Non-Hazardous Waste",
        "icon": "trash",
        "border": "border-slate-300",
        "bg_soft": "bg-slate-50",
        "badge": "bg-slate-800 text-white",
        "treatment": "Municipal Composting, Recycling, or Sanitary Landfill",
        "summary": "Office paper, sterile wrappers, dry packaging, and food waste."
    }
}


def get_waste_guideline(class_name: str) -> Dict[str, Any]:
    """
    Returns full segregation guidelines for a specific detected class name.
    """
    clean_name = str(class_name).strip().lower()
    if clean_name in SEGREGATION_RULES:
        return SEGREGATION_RULES[clean_name]
    
    # Generic fallback if an unknown class appears
    return {
        "class_name": class_name,
        "display_name": class_name.title(),
        "bin_color": "Yellow",
        "bin_hex": "#EAB308",
        "bin_border": "#CA8A04",
        "bin_text_color": "#78350F",
        "badge_bg": "bg-amber-50",
        "badge_text": "text-amber-800",
        "badge_border": "border-amber-300",
        "category_title": "Default Biohazard Yellow Bag",
        "hazard_level": "Moderate",
        "hazard_color": "text-amber-600 bg-amber-50 border-amber-200",
        "risk_description": "Unclassified medical item. Default to precautionary infectious handling.",
        "treatment": "Autoclaving or controlled incineration.",
        "handling_instructions": ["Exercise precaution.", "Segregate under supervised clinical protocol."],
        "cpcb_schedule": "Schedule I: Precautionary Medical Waste"
    }


def summarize_detections(detections: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes summary metrics and actionable segregation protocols from a list of detections.
    """
    if not detections:
        return {
            "total_items": 0,
            "required_bins": [],
            "highest_hazard": "None",
            "highest_hazard_color": "text-slate-500 bg-slate-100",
            "primary_stream": "No Waste Detected",
            "bin_counts": {},
            "action_checklist": ["No objects detected above the confidence threshold."]
        }

    bin_counts: Dict[str, int] = {}
    class_counts: Dict[str, int] = {}
    has_critical = False
    has_high = False
    has_moderate = False

    for det in detections:
        bin_color = det.get("bin_color", "Yellow")
        bin_counts[bin_color] = bin_counts.get(bin_color, 0) + 1
        
        cname = det.get("class_name", "")
        class_counts[cname] = class_counts.get(cname, 0) + 1
        
        hazard = det.get("hazard_level", "")
        if hazard == "Critical":
            has_critical = True
        elif hazard == "High":
            has_high = True
        elif hazard == "Moderate":
            has_moderate = True

    if has_critical:
        highest_hazard = "Critical (Sharps Risk)"
        hazard_color = "text-red-700 bg-red-100 border-red-300"
    elif has_high:
        highest_hazard = "High (Biohazard / Infectious)"
        hazard_color = "text-orange-700 bg-orange-100 border-orange-300"
    elif has_moderate:
        highest_hazard = "Moderate (Contaminated Recyclable)"
        hazard_color = "text-amber-700 bg-amber-100 border-amber-300"
    else:
        highest_hazard = "Low / General"
        hazard_color = "text-emerald-700 bg-emerald-100 border-emerald-300"

    # Determine primary stream based on most frequent bin
    primary_bin = max(bin_counts, key=bin_counts.get)
    meta = BIN_CATEGORIES_METADATA.get(primary_bin, {})
    primary_stream = f"{primary_bin} Bin ({meta.get('title', 'Biohazard')})"

    # Generate actionable protocols
    checklist = []
    if "White" in bin_counts:
        checklist.append("⚠️ CRITICAL: White puncture-proof container required for sharps (needles/syringes).")
    if "Yellow" in bin_counts:
        checklist.append("🟡 Yellow biohazard bag required for soiled gauze, cotton, or infectious PPE.")
    if "Red" in bin_counts:
        checklist.append("🔴 Red non-chlorinated bag required for recyclable plastics (gloves, tubing, bottles).")
    if "Blue" in bin_counts:
        checklist.append("🔵 Blue rigid container required for glassware, ampoules, or test tubes.")
    if "Black" in bin_counts:
        checklist.append("⚫ Black/Green bin for general non-hazardous waste.")

    return {
        "total_items": len(detections),
        "required_bins": list(bin_counts.keys()),
        "highest_hazard": highest_hazard,
        "highest_hazard_color": hazard_color,
        "primary_stream": primary_stream,
        "bin_counts": bin_counts,
        "class_counts": class_counts,
        "action_checklist": checklist
    }

