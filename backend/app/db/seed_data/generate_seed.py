import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]
LABELS_PATH = BASE_DIR / "ml" / "model_registry" / "class_labels.json"
OUTPUT_PATH = Path(__file__).resolve().parent / "diseases_data.json"

with open(LABELS_PATH, "r") as f:
    class_labels = json.load(f)

treatment_templates = {
    "healthy": {
        "desc": "The foliage exhibits vigorous vitality, uniform chlorophyll distribution, and no evidence of fungal, bacterial, or viral pathogen infection.",
        "symptoms": "Intact leaf structure, consistent green pigmentation, absence of lesions, spots, curling, or necrosis.",
        "causes": "Optimal watering, balanced N-P-K nutrient availability, and good air circulation.",
        "organic": "Continue regular organic fertilization (compost tea, fish emulsion). Maintain balanced drip irrigation.",
        "chemical": "No chemical fungicide or pesticide required. Maintain balanced micronutrient foliar sprays if needed.",
        "prevention": "Ensure proper spacing between crops to promote air circulation and avoid overhead leaf wetting."
    },
    "Early_blight": {
        "desc": "Fungal disease caused primarily by Alternaria species, producing characteristic concentric target-board lesions on foliage.",
        "symptoms": "Brown to black spots with concentric rings surrounded by yellow chlorotic halos, beginning on lower/older leaves and advancing upward.",
        "causes": "Alternaria solani spores surviving in infected plant debris; favored by alternating wet and dry conditions with high humidity.",
        "organic": "Apply cold-pressed neem oil (0.5%) or bio-fungicide containing Bacillus subtilis / Trichoderma harzianum weekly.",
        "chemical": "Foliar application of Chlorothalonil, Mancozeb, or Copper hydroxide sprays at 7–10 day intervals.",
        "prevention": "Practice 3-year crop rotation with non-solanaceous crops. Apply organic mulch around base to stop soil splash."
    },
    "Late_blight": {
        "desc": "Devastating oomycete pathogen caused by Phytophthora infestans that rapidly spreads and can destroy entire fields within days under cool, humid conditions.",
        "symptoms": "Large irregular water-soaked pale-green to dark-brown lesions with fuzzy white sporulation on leaf undersides in humid mornings.",
        "causes": "Phytophthora infestans favored by prolonged leaf moisture (>10 hours) and temperatures between 15°C and 22°C.",
        "organic": "Apply fixed copper sprays (Bordeaux mixture) preventively. Remove and deeply bury or burn severely infected leaves immediately.",
        "chemical": "Systemic fungicides: Metalaxyl + Mancozeb, Cymoxanil, or Dimethomorph applied preventively or upon first symptom.",
        "prevention": "Use certified pathogen-free seeds/tubers. Avoid overhead irrigation and ensure rapid foliage drying through wide row spacing."
    },
    "Bacterial_spot": {
        "desc": "Bacterial infection caused by Xanthomonas species attacking leaves, stems, and fruit under warm, rainy weather.",
        "symptoms": "Small, water-soaked circular lesions that turn dark brown or black with a distinct yellow halo, giving leaves a ragged appearance.",
        "causes": "Xanthomonas campestris spread via rain splash, overhead sprinklers, contaminated equipment, and seed.",
        "organic": "Spray copper octanoate (copper soap) combined with Bacillus amyloliquefaciens foliar inoculants.",
        "chemical": "Copper hydroxide + Mancozeb tank mix; streptomycin sulfate sprays in non-bearing crops where permitted.",
        "prevention": "Disinfect pruning tools with 70% isopropyl alcohol between plants. Avoid working in fields when foliage is wet."
    },
    "Powdery_mildew": {
        "desc": "Widespread fungal infection characterized by talcum powder-like white mycelial growth on leaf surfaces.",
        "symptoms": "White to light gray powdery patches on the upper and lower leaf surfaces, leading to leaf yellowing, curling, and premature leaf drop.",
        "causes": "Podosphaera / Erysiphe fungal species flourishing in warm, dry weather accompanied by high ambient relative humidity and shade.",
        "organic": "Potassium bicarbonate (3g/L) or diluted milk spray (40% milk, 60% water) exposed to sunlight. Horticultural neem oil.",
        "chemical": "Sulfur-based dusts or systemic fungicides like Myclobutanil or Azoxystrobin applied every 10–14 days.",
        "prevention": "Select resistant cultivars, prune dense foliage to maximize sunlight penetration and airflow."
    },
    "Black_rot": {
        "desc": "Destructive fungal disease affecting apples and grapes causing necrotic leaf lesions and fruit mummification.",
        "symptoms": "Circular reddish-brown spots that develop tiny black specks (pycnidia) in the center; infected leaves turn yellow and drop.",
        "causes": "Botryosphaeria obtusa / Guignardia bidwellii overwintering in mummified fruit, dead wood, and fallen cankers.",
        "organic": "Thorough dormant-season sanitation; apply liquid copper or sulfur sprays at bud break.",
        "chemical": "Captan, Mancozeb, or Myclobutanil fungicides applied from early bud stage through post-bloom.",
        "prevention": "Prune out dead canes and cankers during winter; destroy all mummified fruits left on the vine/tree."
    },
    "Rust": {
        "desc": "Fungal disease producing powdery rust-colored pustules on leaf undersides.",
        "symptoms": "Small, raised orange, yellow, or cinnamon-brown pustules that break through leaf epidermis, releasing powdery spores.",
        "causes": "Puccinia species spores carried by wind over long distances; favored by moderate temperatures and dew.",
        "organic": "Foliar application of sulfur dust or neem oil; bio-control with Ampelomyces quisqualis.",
        "chemical": "Triazole fungicides (Propiconazole, Tebuconazole) or Strobilurins (Azoxystrobin).",
        "prevention": "Plant resistant hybrids. Remove alternate host weeds (like juniper for cedar apple rust) nearby."
    },
    "Leaf_Mold": {
        "desc": "Foliar fungal pathogen caused by Passalora fulva common in high-humidity greenhouse environments.",
        "symptoms": "Pale green to yellowish spots on upper leaf surface, with olive-green to grayish velvety mold on the underside.",
        "causes": "Relative humidity above 85% with temperatures around 21°C–24°C.",
        "organic": "Copper fungicides and bio-fungicides; improve greenhouse ventilation and exhaust fan circulation.",
        "chemical": "Chlorothalonil, Copper sulfate, or Difenoconazole.",
        "prevention": "Maintain greenhouse relative humidity below 80% with heated airflow and drip irrigation."
    },
    "Septoria_leaf_spot": {
        "desc": "Fungal disease caused by Septoria lycopersici causing numerous small circular leaf spots with dark borders.",
        "symptoms": "Numerous small (1.5-3mm) circular spots with gray or tan centers and dark brown margins with black pycnidia.",
        "causes": "Septoria lycopersici surviving on solanaceous weeds and crop residue, splashed by raindrops.",
        "organic": "Copper soap fungicides applied at 7-day intervals; bottom pruning lower 12 inches of foliage.",
        "chemical": "Chlorothalonil or Mancozeb sprays immediately after first bottom lesions appear.",
        "prevention": "Crop rotation, drip irrigation, and heavy straw mulching to prevent soil splashing onto leaves."
    },
    "Spider_mites": {
        "desc": "Arachnid pests (Tetranychus urticae) that suck plant sap and cause chlorotic stippling.",
        "symptoms": "Fine white/yellow stippling on upper leaf surface, bronze discoloration, and fine silken webbing on leaf undersides.",
        "causes": "Hot, dry, dusty environmental conditions accelerating the mite reproduction cycle to just 5 days.",
        "organic": "Insecticidal soap or horticultural mineral oil sprays; release predatory mites (Phytoseiulus persimilis).",
        "chemical": "Miticide sprays containing Abamectin, Bifenazate, or Spiromesifen; avoid broad-spectrum pyrethroids that kill natural predators.",
        "prevention": "Keep foliage and access pathways misted or watered to reduce dust; inspect undersides of leaves weekly."
    },
    "Virus": {
        "desc": "Systemic viral infections causing severe stunted growth, chlorosis, and leaf deformation.",
        "symptoms": "Mottled yellow-green mosaic patterns, upward leaf curling, crinkling, stunted internodes, and brittle foliage.",
        "causes": "Transmitted by insect vectors like whiteflies (Bemisia tabaci), aphids, thrips, or mechanical contact.",
        "organic": "Vector control with reflective silver mulches, yellow sticky traps, and neem-based insecticidal sprays.",
        "chemical": "Control insect vectors with Imidacloprid, Acetamiprid, or Flonicamid. Note: Viral infections cannot be cured with fungicides.",
        "prevention": "Rogue out and destroy infected plants immediately; install 50-mesh insect screens in greenhouses."
    }
}

diseases_data = []

for raw_cls in class_labels:
    parts = raw_cls.split("___")
    crop_name = parts[0].replace("_", " ").replace("(including sour)", "").strip()
    disease_suffix = parts[1] if len(parts) > 1 else "healthy"
    disease_display = disease_suffix.replace("_", " ").strip()
    is_healthy = "healthy" in disease_suffix.lower()

    if is_healthy:
        tpl = treatment_templates["healthy"]
    elif "early_blight" in disease_suffix.lower():
        tpl = treatment_templates["Early_blight"]
    elif "late_blight" in disease_suffix.lower():
        tpl = treatment_templates["Late_blight"]
    elif "bacterial" in disease_suffix.lower():
        tpl = treatment_templates["Bacterial_spot"]
    elif "powdery" in disease_suffix.lower() or "mildew" in disease_suffix.lower():
        tpl = treatment_templates["Powdery_mildew"]
    elif "black_rot" in disease_suffix.lower() or "esca" in disease_suffix.lower():
        tpl = treatment_templates["Black_rot"]
    elif "rust" in disease_suffix.lower():
        tpl = treatment_templates["Rust"]
    elif "mold" in disease_suffix.lower():
        tpl = treatment_templates["Leaf_Mold"]
    elif "septoria" in disease_suffix.lower():
        tpl = treatment_templates["Septoria_leaf_spot"]
    elif "spider_mites" in disease_suffix.lower():
        tpl = treatment_templates["Spider_mites"]
    elif "virus" in disease_suffix.lower() or "curl" in disease_suffix.lower() or "mosaic" in disease_suffix.lower():
        tpl = treatment_templates["Virus"]
    else:
        tpl = treatment_templates["Early_blight"]

    entry = {
        "id": raw_cls,
        "crop": crop_name,
        "name": f"{crop_name} - {disease_display}",
        "scientific_name": f"Pathogen affecting {crop_name}",
        "is_healthy": is_healthy,
        "description": f"{crop_name} foliage affected by {disease_display}. {tpl['desc']}",
        "symptoms": tpl["symptoms"],
        "causes": tpl["causes"],
        "organic_treatment": tpl["organic"],
        "chemical_treatment": tpl["chemical"],
        "prevention": tpl["prevention"]
    }
    diseases_data.append(entry)

with open(OUTPUT_PATH, "w") as f:
    json.dump(diseases_data, f, indent=2)

print(f"Generated {len(diseases_data)} records into {OUTPUT_PATH}")
