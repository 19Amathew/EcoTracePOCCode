from google.cloud import vision
from image_rec import image_attributes
from recycling_categoriser import categorise_with_gemini
import os
import glob

def main():
    print("Initialising Google Vision API...")
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../rec/metal-shift-480710-p1-4478f1a5b24c.json'
    client = vision.ImageAnnotatorClient()

    image_files = glob.glob('../rec/*.png')
    if not image_files:
        print("No PNG images found in ../rec/ directory")
        return
    
    print(f"Found {len(image_files)} images to process\n")
    
    results = []
    
    for image_path in image_files:
        print("\n" + "="*80)
        print(f"PROCESSING: {os.path.basename(image_path)}")
        print("="*80)
        
        try:
            # Get image attributes
            data = image_attributes(client, image_path)
            
            # Use gemini to categorise
            print("\n" + "="*60)
            print("GEMINI RECYCLING CATEGORISATION")
            print("="*60)
            
            result = categorise_with_gemini(data)
            result['image_file'] = os.path.basename(image_path)
            
            print(f"\nImage: {result['image_file']}")
            print(f"Category: {result['category']}")
            print(f"Material: {result['material']}")
            print(f"Recyclable: {result['recyclable']}")
            print(f"Instructions: {result['instructions']}")
            print(f"Reasoning: {result['reasoning']}")
            
            results.append(result)
            
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY OF ALL IMAGES")
    print("="*80)
    for result in results:
        print(f"\n{result['image_file']}:")
        print(f"  Category: {result['category']}")
        print(f"  Recyclable: {result['recyclable']}")
    
    return results

if __name__ == '__main__':
    main()