import re
import os
import shutil

def process_presentation(base_dir):
    index_path = os.path.join(base_dir, 'index.html')
    if not os.path.exists(index_path):
        print(f"File not found: {index_path}")
        return

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    slides_start_match = re.search(r'<div class="slides">\s*', content)
    if not slides_start_match:
        print(f"Could not find <div class=\"slides\"> in {index_path}")
        return

    slides_start_idx = slides_start_match.end()
    
    # Header is everything up to <div class="slides">
    header_content = content[:slides_start_idx]

    # Find where the slides end. Usually the closing </div> of <div class="slides">
    # We can search for the last </section>
    last_section_end = content.rfind('</section>')
    if last_section_end == -1:
        print(f"Could not find </section> in {index_path}")
        return
        
    slides_end_idx = last_section_end + len('</section>')
    
    # We also need to capture any trailing spaces/newlines before the </div>
    # Actually, the footer starts right after the last </section>
    footer_content = "\n  " + content[slides_end_idx:].lstrip()
    
    slides_content = content[slides_start_idx:slides_end_idx]

    # Split slides based on <!-- ===
    slide_chunks = re.split(r'(?=<!-- ======================================================)', slides_content)
    
    # Filter empty chunks
    slide_chunks = [chunk.strip() for chunk in slide_chunks if chunk.strip()]

    # Create directories
    slides_dir = os.path.join(base_dir, 'slides')
    template_dir = os.path.join(base_dir, 'template')
    os.makedirs(slides_dir, exist_ok=True)
    os.makedirs(template_dir, exist_ok=True)

    with open(os.path.join(template_dir, 'header.html'), 'w', encoding='utf-8') as f:
        f.write(header_content)

    with open(os.path.join(template_dir, 'footer.html'), 'w', encoding='utf-8') as f:
        f.write(footer_content)

    slide_files = []

    for chunk in slide_chunks:
        # Extract title from comment block
        title_match = re.search(r'SLIDE ([\d\.]+) — ([^\n]+)', chunk)
        if title_match:
            num = title_match.group(1).replace('.', '_')
            name = title_match.group(2).strip()
            # sanitize name
            safe_name = re.sub(r'[^a-zA-Z0-9]', '_', name).strip('_').lower()
            safe_name = re.sub(r'_+', '_', safe_name)
            
            # Pad the number with zero if needed
            if len(num) == 1 or ('.' not in num and len(num) == 1):
                num_str = f"{int(num):02d}"
            else:
                num_str = num
                
            filename = f"{num_str}_{safe_name}.html"
        else:
            filename = f"slide_{len(slide_files)+1:02d}.html"

        filepath = os.path.join(slides_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(chunk + "\n")
        slide_files.append(filename)

    print(f"Processed {base_dir}: Extracted {len(slide_files)} slides.")

# Process both presentations
process_presentation('apresentacao')
process_presentation('apresentacao/parte2')

# Create builder script
builder_script = """import os
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
            content += f"\\n    " + f.read().replace("\\n", "\\n    ").strip() + "\\n"
            
    with open(os.path.join(template_dir, 'footer.html'), 'r', encoding='utf-8') as f:
        content += f.read()
        
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Built {output_path} from {len(slide_files)} slides.")

if __name__ == '__main__':
    build_presentation('apresentacao')
    build_presentation('apresentacao/parte2')
"""

with open('build_apresentacao.py', 'w', encoding='utf-8') as f:
    f.write(builder_script)
    
print("Created build_apresentacao.py")
