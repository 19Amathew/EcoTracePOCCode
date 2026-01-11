from google.cloud import vision

def image_attributes(client, image_path='../rec/image.png'):
    """
    Analyse image and return structured data for use in prompts.
    
    Returns:
        dict: {
            'labels': list of (description, confidence) tuples,
            'dominant_colors': list of RGB tuples,
            'raw_labels': list of label descriptions,
            'top_label': str
        }
    """
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
        
    image = vision.Image(content=content)

    print("\n label detection")
    response = client.label_detection(image=image)
    labels = response.label_annotations
    
    labels_data = []
    for label in labels:
        print(f"- {label.description}: {label.score:.2%} confidence")
        labels_data.append((label.description, label.score))
    
    print("\n image properties")
    response = client.image_properties(image=image)
    props = response.image_properties_annotation

    colours_data = []
    print("dominant colours:")
    for color in props.dominant_colors.colors[:5]:
        rgb = color.color
        rgb_tuple = (int(rgb.red), int(rgb.green), int(rgb.blue))
        colours_data.append(rgb_tuple)
        print(f"  RGB{rgb_tuple} - "
              f"Score: {color.score:.2f}, Pixel Fraction: {color.pixel_fraction:.2%}")
    
    return {
        'labels': labels_data,
        'dominant_colours': colours_data,
        'raw_labels': [desc for desc, _ in labels_data],
        'top_label': labels_data[0][0] if labels_data else 'Unknown',
        'confidence': labels_data[0][1] if labels_data else 0.0
    }