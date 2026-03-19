import os
import glob

def build_presentation(base_dir):
    slides_dir = os.path.join(base_dir, 'slides')
    template_dir = os.path.join(base_dir, 'template')
    output_path = os.path.join(base_dir, 'index.html')
    
    if not os.path.exists(slides_dir) or not os.path.exists(template_dir):
        return

    with open(os.path.join(template_dir, 'header.html'), 'r', encoding='utf-8') as f:
        content = f.read()
        
    slide_files = sorted(glob.glob(os.path.join(slides_dir, '*.html')))
    
    for slide_file in slide_files:
        with open(slide_file, 'r', encoding='utf-8') as f:
            content += f"\n    " + f.read().replace("\n", "\n    ").strip() + "\n"
            
    with open(os.path.join(template_dir, 'footer.html'), 'r', encoding='utf-8') as f:
        content += f.read()
        
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Built {output_path} from {len(slide_files)} slides.")

if __name__ == '__main__':
    build_presentation('apresentacao')
    build_presentation('apresentacao/parte2')
