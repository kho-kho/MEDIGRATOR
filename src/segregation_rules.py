"""
MEDIGRATOR: AI-Driven Medical Waste Detection & Intelligent Segregation
Medical Waste Segregation Rules & Regulatory Knowledge Base
Aligned with:
  - Central Pollution Control Board (CPCB) Bio-Medical Waste Management Rules (2016 / 2018 Amendments)
  - World Health Organization (WHO) Safe Management of Wastes from Health-Care Activities

Maps all 14 detection classes recognized by the YOLO11 model to standard disposal categories,
bin color codes, hazard ratings, and disposal/treatment protocols.
Ensures technical honesty: unverified classes display 'Mapping requires verification',
and low-confidence detections are flagged for human verification before disposal assignment.
"""

from typing import Dict, Any, List, Optional

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
        "official_category": "CPCB Schedule I - Waste Sharps (Category 4)",
        "mapping_status": "VERIFIED",
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
        "cpcb_schedule": "Schedule I: White (Translucent) - Waste Sharps including metals",
        "who_reference": "WHO Healthcare Waste Section 7.2: Sharps Management"
    },
    "used syringe": {
        "class_name": "used syringe",
        "display_name": "Used Syringe Assembly / Barrel",
        "official_category": "CPCB Schedule I - Sharps (Needle Attached) / Contaminated Plastic (Barrel)",
        "mapping_status": "VERIFIED",
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
        "cpcb_schedule": "Schedule I: White (Sharps) / Red (Contaminated Plastic Barrels)",
        "who_reference": "WHO Healthcare Waste Section 7.3: Syringes & Injections"
    },
    "needle cap": {
        "class_name": "needle cap",
        "display_name": "Plastic Needle Cap",
        "official_category": "CPCB Schedule I - Contaminated Recyclable Waste (Red Category)",
        "mapping_status": "VERIFIED",
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
        "cpcb_schedule": "Schedule I: Red - Contaminated Waste (Recyclable Plastics)",
        "who_reference": "WHO Healthcare Waste Section 7.4: Non-Sharps Plastics"
    },
    "gauze": {
        "class_name": "gauze",
        "display_name": "Soiled Surgical Gauze / Swab",
        "official_category": "CPCB Schedule I - Soiled Waste (Yellow Category)",
        "mapping_status": "VERIFIED",
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
        "cpcb_schedule": "Schedule I: Yellow - Soiled Waste (Items contaminated with blood/fluids)",
        "who_reference": "WHO Healthcare Waste Section 7.1: Infectious Waste"
    },
    "unused gauze": {
        "class_name": "unused gauze",
        "display_name": "Unused / Clean Gauze Pack",
        "official_category": "Solid Waste Management Rules - General Non-Hazardous Solid Waste",
        "mapping_status": "VERIFIED",
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
            "If contaminated by room contact in infectious ward, route to Yellow bin.",
            "Otherwise, dispose into general municipal collection."
        ],
        "cpcb_schedule": "General Solid Waste: Black/Green Bin (Non-Biohazard)",
        "who_reference": "WHO Healthcare Waste Section 7.6: Non-Risk Healthcare Waste"
    },
    "glove": {
        "class_name": "glove",
        "display_name": "Latex / Nitrile Examination Glove",
        "official_category": "CPCB Schedule I - Contaminated Recyclable Waste (Red Category)",
        "mapping_status": "VERIFIED",
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
        "cpcb_schedule": "Schedule I: Red - Contaminated Recyclable Waste (Gloves, catheters, IV sets)",
        "who_reference": "WHO Healthcare Waste Section 7.4: Contaminated Plastics & Rubber"
    },
    "mask": {
        "class_name": "mask",
        "display_name": "Surgical / N95 Disposable Mask",
        "official_category": "CPCB Schedule I - Soiled Waste / PPE (Yellow Category)",
        "mapping_status": "VERIFIED",
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
        "cpcb_schedule": "Schedule I: Yellow - Soiled / Expired PPE Waste",
        "who_reference": "WHO COVID-19 / Infectious Respiratory Waste Handling"
    },
    "scrub": {
        "class_name": "scrub",
        "display_name": "Medical Scrubs / Disposable Gown",
        "official_category": "CPCB Schedule I - Soiled Waste / Contaminated Linen (Yellow Category)",
        "mapping_status": "VERIFIED",
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
        "cpcb_schedule": "Schedule I: Yellow - Soiled Waste (Bedding, contaminated clothing)",
        "who_reference": "WHO Healthcare Waste Section 7.1: Contaminated Linen"
    },
    "glass": {
        "class_name": "glass",
        "display_name": "Medicine Ampoule / Glass Vial",
        "official_category": "CPCB Schedule I - Glassware (Blue Category)",
        "mapping_status": "VERIFIED",
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
        "cpcb_schedule": "Schedule I: Blue - Glassware (Medicine vials, ampoules, glassware articles)",
        "who_reference": "WHO Healthcare Waste Section 7.5: Pharmaceutical & Glass Packaging"
    },
    "test tube": {
        "class_name": "test tube",
        "display_name": "Blood Collection Tube / Vacutainer",
        "official_category": "CPCB Schedule I - Glassware / Specimen Waste (Blue / Yellow Category)",
        "mapping_status": "VERIFIED",
        "bin_color": "Blue",
        "bin_hex": "#3B82F6",
        "bin_border": "#2563EB",
        "bin_text_color": "#FFFFFF",
        "badge_bg": "bg-blue-50",
        "badge_text": "text-blue-700",
        "badge_border": "border-blue-300",
        "category_title": "Blue Box (Glass Vacutainers) / Yellow (if liquid specimen intact)",
        "hazard_level": "High",
        "hazard_color": "text-red-500 bg-red-50 border-red-200",
        "risk_description": "Pathology waste containing whole blood, serum, or laboratory cultures.",
        "treatment": "Pre-treatment with autoclave or microwave on-site at lab, followed by glass decontamination & recycling.",
        "handling_instructions": [
            "Ensure tube stoppers are tightly fitted to avoid blood spills during transit.",
            "Autoclave microbiology/pathology tubes on-site prior to final dispatch.",
            "Place in rigid blue container with biohazard markings."
        ],
        "cpcb_schedule": "Schedule I: Blue / Yellow - Microbiology & Clinical Specimen Glassware",
        "who_reference": "WHO Healthcare Waste Section 7.1: Laboratory Diagnostic Waste"
    },
    "fluid bottle": {
        "class_name": "fluid bottle",
        "display_name": "IV Fluid Saline / Solution Bottle",
        "official_category": "CPCB Schedule I - Contaminated Recyclable Waste (Red Category)",
        "mapping_status": "VERIFIED",
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
        "cpcb_schedule": "Schedule I: Red - Recyclable Plastic Bottles & Infusion Sets",
        "who_reference": "WHO Healthcare Waste Section 7.4: Non-Infectious Plastics"
    },
    "tube": {
        "class_name": "tube",
        "display_name": "IV Tubing / Catheter / Suction Line",
        "official_category": "CPCB Schedule I - Contaminated Recyclable Waste (Red Category)",
        "mapping_status": "VERIFIED",
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
        "cpcb_schedule": "Schedule I: Red - Tubing, catheters, intravenous sets",
        "who_reference": "WHO Healthcare Waste Section 7.4: Contaminated Tubing & Catheters"
    },
    "plastic": {
        "class_name": "plastic",
        "display_name": "Medical Plastic Packaging / Cups / Trays",
        "official_category": "CPCB Schedule I - Contaminated Recyclable Waste (Red Category)",
        "mapping_status": "VERIFIED",
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
        "cpcb_schedule": "Schedule I: Red - Contaminated Recyclable Plastics",
        "who_reference": "WHO Healthcare Waste Section 7.4: Rigid Plastic Articles"
    },
    "paper": {
        "class_name": "paper",
        "display_name": "Medical Paper / Towels / Packaging Sheets",
        "official_category": "Solid Waste Management Rules - General Non-Hazardous Solid Waste",
        "mapping_status": "VERIFIED",
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
            "Shred patient-identifiable medical records in compliance with medical confidentiality.",
            "Place into black or green municipal bin."
        ],
        "cpcb_schedule": "General Solid Waste: Black/Green Bin (Non-Hazardous)",
        "who_reference": "WHO Healthcare Waste Section 7.6: General Non-Risk Waste"
    }
}

# Bin category metadata for summary dashboard
BIN_CATEGORIES_METADATA: Dict[str, Dict[str, Any]] = {
    "Yellow": {
        "color_name": "Yellow",
        "hex": "#EAB308",
        "title": "Soiled & Infectious Waste",
        "icon": "biohazard",
        "border": "border-amber-400",
        "bg_soft": "bg-amber-50 dark:bg-amber-950/20",
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
        "bg_soft": "bg-red-50 dark:bg-red-950/20",
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
        "bg_soft": "bg-slate-50 dark:bg-slate-900/40",
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
        "bg_soft": "bg-blue-50 dark:bg-blue-950/20",
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
        "bg_soft": "bg-slate-50 dark:bg-slate-900/30",
        "badge": "bg-slate-800 text-white",
        "treatment": "Municipal Composting, Recycling, or Sanitary Landfill",
        "summary": "Office paper, sterile wrappers, dry packaging, and non-clinical waste."
    }
}


def get_waste_guideline(class_name: str) -> Dict[str, Any]:
    """
    Returns full segregation guidelines for a specific detected class name.
    If unverified or unrecognized, returns an honest 'Mapping requires verification' record.
    """
    clean_name = str(class_name).strip().lower()
    if clean_name in SEGREGATION_RULES:
        return SEGREGATION_RULES[clean_name]
    
    # Strictly honest fallback: do not invent categories or bin colors
    return {
        "class_name": class_name,
        "display_name": f"{class_name.title()} (Unverified Class)",
        "official_category": "Mapping requires verification",
        "mapping_status": "UNVERIFIED",
        "bin_color": "Unassigned",
        "bin_hex": "#64748B",
        "bin_border": "#94A3B8",
        "bin_text_color": "#F8FAFC",
        "badge_bg": "bg-slate-100",
        "badge_text": "text-slate-700",
        "badge_border": "border-slate-300",
        "category_title": "Mapping requires verification",
        "hazard_level": "Undetermined",
        "hazard_color": "text-slate-600 bg-slate-100 border-slate-300",
        "risk_description": "Detected object label has no verified mapping in CPCB/WHO regulatory schedules.",
        "treatment": "Clinical safety supervisor must inspect the object before disposal.",
        "handling_instructions": [
            "Do not discard into municipal or clinical bins without manual verification.",
            "Hold item safely until infection prevention supervisor inspects it.",
            "Update institutional waste classification ontology if this is a novel item."
        ],
        "cpcb_schedule": "Mapping requires verification",
        "who_reference": "WHO Healthcare Waste Section 7: Unclassified Items"
    }


def evaluate_detection(
    class_name: str,
    confidence: float,
    bbox: List[float],
    detection_id: int,
    conf_threshold: float = 0.25,
    verification_threshold: float = 0.50,
    track_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Evaluates an individual computer vision detection:
      - Validates against regulatory knowledge base
      - Distinguishes model confidence from mapping status
      - Flags low-confidence (< verification_threshold) and unknown classes for human verification
      - Prevents automatic assignment to a disposal category when uncertain
    """
    guideline = get_waste_guideline(class_name)
    is_verified_mapping = (guideline.get("mapping_status") == "VERIFIED")
    
    # Model confidence level
    conf_pct = round(confidence * 100, 1)
    is_high_confidence = (confidence >= verification_threshold)
    
    # Human verification requirement logic
    requires_human_verification = False
    verification_reasons = []

    if not is_verified_mapping:
        requires_human_verification = True
        verification_reasons.append("Mapping requires verification: object class not in verified regulatory schedule.")
    
    if not is_high_confidence:
        requires_human_verification = True
        verification_reasons.append(
            f"Low model confidence ({conf_pct}% < {int(verification_threshold*100)}%). Manual visual confirmation required before disposal."
        )

    # Category assignment: Only assign if verified AND high confidence
    if requires_human_verification:
        if not is_verified_mapping:
            assigned_category = "Mapping requires verification"
            assigned_bin = "Unassigned"
            assigned_bin_hex = "#64748B"
        else:
            assigned_category = "Pending Human Verification (Unassigned)"
            assigned_bin = "Pending Review"
            assigned_bin_hex = "#F59E0B"
    else:
        assigned_category = guideline.get("category_title", "Unassigned")
        assigned_bin = guideline.get("bin_color", "Yellow")
        assigned_bin_hex = guideline.get("bin_hex", "#EAB308")

    return {
        "id": detection_id,
        "track_id": track_id,
        "class_name": class_name,
        "display_name": guideline.get("display_name", class_name.title()),
        "official_category": guideline.get("official_category", "Mapping requires verification"),
        "mapping_status": guideline.get("mapping_status", "UNVERIFIED"),
        "confidence": round(confidence, 4),
        "confidence_percent": conf_pct,
        "confidence_level": "High Confidence" if is_high_confidence else "Low / Borderline",
        "requires_human_verification": requires_human_verification,
        "verification_reason": " | ".join(verification_reasons) if verification_reasons else "Automated mapping verified",
        "assigned_category": assigned_category,
        "assigned_bin": assigned_bin,
        "bin_color": guideline.get("bin_color", "Yellow"),
        "bin_hex": assigned_bin_hex,
        "hazard_level": guideline.get("hazard_level", "Moderate"),
        "treatment": guideline.get("treatment", "Supervised clinical segregation"),
        "handling_instructions": guideline.get("handling_instructions", []),
        "cpcb_schedule": guideline.get("cpcb_schedule", "Mapping requires verification"),
        "who_reference": guideline.get("who_reference", "WHO Healthcare Waste"),
        "bbox": bbox
    }


def summarize_detections(detections: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes genuine metrics from actual model detections:
      - Total objects detected
      - Detected object classes
      - Verified category assignments
      - Count and list of objects requiring human verification
      - True hazard and disposal streams
    No fabricated or static mock values.
    """
    if not detections:
        return {
            "total_items": 0,
            "detected_classes": [],
            "unique_classes_count": 0,
            "verified_assignments_count": 0,
            "pending_verification_count": 0,
            "required_bins": [],
            "highest_hazard": "None",
            "highest_hazard_color": "text-slate-400 bg-slate-800/40 border-slate-700",
            "primary_stream": "No Waste Detected",
            "bin_counts": {},
            "class_counts": {},
            "verification_items": [],
            "action_checklist": ["No objects detected above the confidence threshold. Adjust threshold slider if items are present."]
        }

    bin_counts: Dict[str, int] = {}
    class_counts: Dict[str, int] = {}
    verified_assignments_count = 0
    pending_verification_count = 0
    verification_items: List[Dict[str, Any]] = []

    has_critical = False
    has_high = False
    has_moderate = False

    for det in detections:
        cname = det.get("class_name", "")
        class_counts[cname] = class_counts.get(cname, 0) + 1

        if det.get("requires_human_verification", False):
            pending_verification_count += 1
            verification_items.append({
                "id": det.get("id"),
                "class_name": cname,
                "confidence_percent": det.get("confidence_percent"),
                "reason": det.get("verification_reason")
            })
        else:
            verified_assignments_count += 1
            bin_color = det.get("assigned_bin", "Yellow")
            bin_counts[bin_color] = bin_counts.get(bin_color, 0) + 1

            hazard = det.get("hazard_level", "")
            if hazard == "Critical":
                has_critical = True
            elif hazard == "High":
                has_high = True
            elif hazard == "Moderate":
                has_moderate = True

    # Determine highest hazard level
    if has_critical:
        highest_hazard = "Critical (Sharps Puncture Risk)"
        hazard_color = "text-rose-400 bg-rose-950/40 border-rose-800"
    elif has_high:
        highest_hazard = "High (Biohazard / Infectious)"
        hazard_color = "text-amber-400 bg-amber-950/40 border-amber-800"
    elif has_moderate:
        highest_hazard = "Moderate (Contaminated Recyclable)"
        hazard_color = "text-yellow-400 bg-yellow-950/40 border-yellow-800"
    elif verified_assignments_count > 0:
        highest_hazard = "Low / General Solid Waste"
        hazard_color = "text-emerald-400 bg-emerald-950/40 border-emerald-800"
    else:
        highest_hazard = "Pending Human Verification"
        hazard_color = "text-amber-400 bg-amber-950/40 border-amber-800"

    # Primary disposal stream based on highest count of verified bins
    if bin_counts:
        primary_bin = max(bin_counts, key=bin_counts.get)
        meta = BIN_CATEGORIES_METADATA.get(primary_bin, {})
        primary_stream = f"{primary_bin} Bin ({meta.get('title', 'Biohazard')})"
    elif pending_verification_count > 0:
        primary_stream = "Pending Human Verification"
    else:
        primary_stream = "No Waste Stream Assigned"

    # Action checklist based on real detected items
    checklist = []
    if "White" in bin_counts:
        checklist.append("⚠️ CRITICAL: White translucent puncture-proof container required for sharps (needles/syringes). Never recap needles manually.")
    if "Yellow" in bin_counts:
        checklist.append("🟡 Yellow biohazard bag required for soiled gauze, contaminated masks, or clinical fabrics. Disinfect or incinerate as per CPCB norms.")
    if "Red" in bin_counts:
        checklist.append("🔴 Red non-chlorinated bag required for recyclable plastics (gloves, tubing, bottles). Autoclave/microwave before shredding.")
    if "Blue" in bin_counts:
        checklist.append("🔵 Blue rigid cardboard box / bin required for medicine vials, glassware, or vacutainers.")
    if "Black" in bin_counts:
        checklist.append("⚫ Black / Green municipal bin for general, uncontaminated administrative or packaging waste.")
    if pending_verification_count > 0:
        checklist.append(f"🔍 HUMAN VERIFICATION: {pending_verification_count} item(s) flagged due to low confidence or unverified classification. Confirm visually before disposal.")

    return {
        "total_items": len(detections),
        "detected_classes": sorted(list(class_counts.keys())),
        "unique_classes_count": len(class_counts),
        "verified_assignments_count": verified_assignments_count,
        "pending_verification_count": pending_verification_count,
        "required_bins": list(bin_counts.keys()),
        "highest_hazard": highest_hazard,
        "highest_hazard_color": hazard_color,
        "primary_stream": primary_stream,
        "bin_counts": bin_counts,
        "class_counts": class_counts,
        "verification_items": verification_items,
        "action_checklist": checklist
    }
