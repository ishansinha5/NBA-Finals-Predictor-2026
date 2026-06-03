def get_base64_bg(img_name):
    """Helper function to hunt down the image file across directories."""
    import base64
    import os
    
    # Search paths: Current directory, Parent directory, Root directory
    search_paths = [
        os.path.join(os.getcwd(), img_name),
        os.path.join(os.path.dirname(__file__), img_name),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), img_name)
    ]
    
    for img_path in search_paths:
        if os.path.exists(img_path):
            with open(img_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/jpg;base64,{encoded_string}"
            
    print(f"WARNING: Could not locate background image: {img_name}")
    return ""