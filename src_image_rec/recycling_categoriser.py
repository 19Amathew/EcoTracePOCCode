import vertexai
from vertexai.generative_models import GenerativeModel

def categorise_with_gemini(image_data, project_id="metal-shift-480710-p1"):
    """
    Use Gemini to categorise recyclable items based on Vision API data.
    
    Args:
        image_data: dict from image_attributes() containing labels and colors
        
    Returns:
        dict with category, material, recyclable status, instructions, and reasoning
    """
    vertexai.init(project=project_id, location="us-central1")
    model = GenerativeModel("gemini-2.0-flash-exp")
    
    prompt = f"""You are a recycling expert assistant. Analyse the following item and determine which recycling bin it should go into.

ITEM DETECTED: {image_data['top_label']}
CONFIDENCE: {image_data['confidence']:.2%}
OTHER POSSIBLE ITEMS: {', '.join(image_data['raw_labels'][1:5])}
DOMINANT COLORS: {', '.join([f'RGB{c}' for c in image_data['dominant_colours'][:3]])}

Based on this information, determine:

1. RECYCLING CATEGORY (choose ONE):
   - Plastic (bottles, containers, packaging)
   - Paper (cardboard, newspapers, office paper)
   - Metal (aluminum cans, steel cans)
   - Glass (bottles, jars)
   - E-waste (electronics, batteries)
   - Organic (food waste, yard waste)
   - Non-recyclable (contaminated, mixed materials)

2. MATERIAL TYPE: Specify the exact material (e.g., PET plastic, corrugated cardboard, aluminum)

3. RECYCLABLE: Yes or No

4. INSTRUCTIONS: Brief recycling instructions (e.g., "rinse before recycling", "remove cap", "flatten box")

5. REASONING: Explain why this item belongs in this category

Provide your response in this exact format:
CATEGORY: [category name]
MATERIAL: [material type]
RECYCLABLE: [Yes/No]
INSTRUCTIONS: [recycling instructions]
REASONING: [explanation]"""
    
    response = model.generate_content(prompt)
    response_text = response.text.strip()
    result = {
        'category': '',
        'material': '',
        'recyclable': '',
        'instructions': '',
        'reasoning': '',
        'raw_response': response_text
    }
    
    lines = response_text.split('\n')
    for line in lines:
        if line.startswith('CATEGORY:'):
            result['category'] = line.replace('CATEGORY:', '').strip()
        elif line.startswith('MATERIAL:'):
            result['material'] = line.replace('MATERIAL:', '').strip()
        elif line.startswith('RECYCLABLE:'):
            result['recyclable'] = line.replace('RECYCLABLE:', '').strip()
        elif line.startswith('INSTRUCTIONS:'):
            result['instructions'] = line.replace('INSTRUCTIONS:', '').strip()
        elif line.startswith('REASONING:'):
            result['reasoning'] = line.replace('REASONING:', '').strip()
    
    return result
