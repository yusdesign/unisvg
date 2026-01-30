#!/usr/bin/env python3
"""
Unicode Glyph to SVG Path Converter
Supports Symbola.ttf (historical) and NotoSansMath (modern) fonts
"""

import argparse
import sys
import os
import zipfile
import tempfile
import urllib.request
import shutil
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

# Font configurations
FONTS = {
    'symbola': {
        'name': 'Symbola.ttf',
        'url': 'https://archive.org/download/Symbola/Symbola613.ttf',
        'type': 'ttf',
        'description': 'Historical Unicode symbol font (broad coverage)'
    },
    'notomath': {
        'name': 'NotoSansMath-Regular.ttf',
        'url': 'https://github.com/notofonts/math/releases/download/NotoSansMath-v3.000/NotoSansMath-v3.000.zip',
        'type': 'zip',
        'zip_path': 'NotoSansMath-v3.000/NotoSansMath-Regular.ttf',
        'description': 'Modern Noto Sans Math font (clean design)'
    },
    'notosans': {
        'name': 'NotoSans-Regular.ttf',
        'url': 'https://github.com/notofonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Regular.ttf',
        'type': 'ttf',
        'description': 'General purpose sans-serif font'
    }
}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(SCRIPT_DIR, "fonts")

class UnicodeGlyphConverter:
    def __init__(self, font_name='symbola', auto_download=True):
        """
        Initialize converter with selected font.
        
        Args:
            font_name: 'symbola', 'notomath', or 'notosans'
            auto_download: Download font if not found
        """
        if font_name not in FONTS:
            raise ValueError(f"Unknown font: {font_name}. Choose from: {', '.join(FONTS.keys())}")
        
        self.font_config = FONTS[font_name]
        self.font_name = font_name
        self.font_path = os.path.join(FONTS_DIR, self.font_config['name'])
        self.font = None
        self.glyph_set = None
        self.unicode_map = {}
        
        # Ensure fonts directory exists
        os.makedirs(FONTS_DIR, exist_ok=True)
        
        # Download font if needed
        if not os.path.exists(self.font_path):
            if auto_download:
                self.download_font()
            else:
                raise FileNotFoundError(
                    f"Font '{font_name}' not found at {self.font_path}\n"
                    f"Run: python {os.path.basename(__file__)} --download {font_name}"
                )
        
        self.load_font()
    
    def download_font(self):
        """Download and extract font."""
        print(f"Downloading {self.font_config['name']}...", file=sys.stderr)
        print(f"Source: {self.font_config['url']}", file=sys.stderr)
        
        try:
            if self.font_config['type'] == 'zip':
                # Download ZIP file
                zip_temp = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
                zip_path = zip_temp.name
                zip_temp.close()
                
                def report_progress(block_num, block_size, total_size):
                    if total_size > 0:
                        percent = (block_num * block_size / total_size) * 100
                        sys.stderr.write(f"\r  Downloading: {percent:.1f}%")
                        sys.stderr.flush()
                
                urllib.request.urlretrieve(self.font_config['url'], zip_path, report_progress)
                print(f"\n  Extracting...", file=sys.stderr)
                
                # Extract specific file from ZIP
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    # Try to find the font file in ZIP
                    target_file = None
                    for file_info in zip_ref.infolist():
                        if file_info.filename.endswith(self.font_config['name']):
                            target_file = file_info.filename
                            break
                        elif 'zip_path' in self.font_config and file_info.filename == self.font_config['zip_path']:
                            target_file = file_info.filename
                            break
                    
                    if target_file:
                        # Extract to fonts directory
                        with zip_ref.open(target_file) as source, open(self.font_path, 'wb') as target:
                            shutil.copyfileobj(source, target)
                        print(f"  Extracted: {target_file}", file=sys.stderr)
                    else:
                        # List files in ZIP for debugging
                        print(f"  Files in ZIP:", file=sys.stderr)
                        for file_info in zip_ref.infolist()[:10]:
                            print(f"    {file_info.filename}", file=sys.stderr)
                        raise ValueError(f"Font file not found in ZIP archive")
                
                # Clean up
                os.unlink(zip_path)
                
            else:  # Direct TTF download
                def report_progress(block_num, block_size, total_size):
                    if total_size > 0:
                        percent = (block_num * block_size / total_size) * 100
                        sys.stderr.write(f"\r  Downloading: {percent:.1f}%")
                        sys.stderr.flush()
                
                urllib.request.urlretrieve(self.font_config['url'], self.font_path, report_progress)
                print(f"\n", file=sys.stderr)
            
            print(f"✓ Downloaded to: {self.font_path}", file=sys.stderr)
            file_size = os.path.getsize(self.font_path)
            print(f"  File size: {file_size:,} bytes", file=sys.stderr)
            
        except Exception as e:
            if os.path.exists(self.font_path):
                os.unlink(self.font_path)
            raise RuntimeError(f"Download failed: {e}")
    
    def load_font(self):
        """Load font and build Unicode mapping."""
        try:
            print(f"\nLoading {self.font_config['name']}...", file=sys.stderr)
            self.font = TTFont(self.font_path)
            self.glyph_set = self.font.getGlyphSet()
            
            # Build Unicode mapping
            self.unicode_map = {}
            for table in self.font['cmap'].tables:
                for code, name in table.cmap.items():
                    if name in self.glyph_set:
                        self.unicode_map[code] = name
            
            print(f"✓ Font loaded successfully", file=sys.stderr)
            print(f"  Glyphs: {len(self.glyph_set):,}", file=sys.stderr)
            print(f"  Unicode characters: {len(self.unicode_map):,}", file=sys.stderr)
            
            # Show supported ranges
            self.show_supported_ranges()
            
        except Exception as e:
            raise RuntimeError(f"Failed to load font: {e}")
    
    def show_supported_ranges(self):
        """Display supported Unicode ranges."""
        if not self.unicode_map:
            return
        
        # Define Unicode blocks relevant for symbols
        unicode_blocks = [
            ('Basic Latin', 0x0000, 0x007F),
            ('Latin-1 Supplement', 0x0080, 0x00FF),
            ('Mathematical Operators', 0x2200, 0x22FF),
            ('Misc Math Symbols-A', 0x27C0, 0x27EF),
            ('Misc Math Symbols-B', 0x2980, 0x29FF),
            ('Supplemental Math Operators', 0x2A00, 0x2AFF),
            ('Misc Symbols and Arrows', 0x2B00, 0x2BFF),
            ('Arrows', 0x2190, 0x21FF),
            ('Geometric Shapes', 0x25A0, 0x25FF),
            ('Misc Symbols', 0x2600, 0x26FF),
            ('Dingbats', 0x2700, 0x27BF),
            ('Letterlike Symbols', 0x2100, 0x214F),
            ('Currency Symbols', 0x20A0, 0x20CF),
            ('Number Forms', 0x2150, 0x218F),
            ('Superscripts and Subscripts', 0x2070, 0x209F),
        ]
        
        print(f"\nSupported Unicode ranges:", file=sys.stderr)
        for block_name, start, end in unicode_blocks:
            count = sum(1 for code in self.unicode_map if start <= code <= end)
            if count > 0:
                total_chars = end - start + 1
                percentage = (count / total_chars) * 100
                print(f"  {block_name:30} {count:4} / {total_chars:4} ({percentage:5.1f}%)", file=sys.stderr)
    
    def check_character_support(self, char):
        """Check if character is supported."""
        char_code = ord(char)
        
        if char_code in self.unicode_map:
            glyph_name = self.unicode_map[char_code]
            return True, glyph_name, char_code
        else:
            return False, None, char_code
    
    def try_multiple_fonts(self, char, fonts_to_try=None):
        """
        Try character in multiple fonts.
        Returns (font_name, glyph_name, char_code) for first successful match.
        """
        if fonts_to_try is None:
            fonts_to_try = ['notomath', 'symbola', 'notosans']
        
        for font_name in fonts_to_try:
            try:
                converter = UnicodeGlyphConverter(font_name, auto_download=False)
                supported, glyph_name, char_code = converter.check_character_support(char)
                if supported:
                    return font_name, glyph_name, char_code
            except:
                continue
        
        return None, None, ord(char)
    
    def get_glyph_bbox(self, glyph):
        """Get glyph bounding box with multiple fallback methods."""
        try:
            # Method 1: From glyf table
            if 'glyf' in self.font:
                if hasattr(glyph, 'name'):
                    glyf_glyph = self.font['glyf'].glyphs.get(glyph.name)
                    if glyf_glyph and hasattr(glyf_glyph, 'xMin'):
                        return (glyf_glyph.xMin, glyf_glyph.yMin, glyf_glyph.xMax, glyf_glyph.yMax)
            
            # Method 2: Direct attributes
            if hasattr(glyph, 'xMin'):
                return (glyph.xMin, glyph.yMin, glyph.xMax, glyph.yMax)
            
            # Method 3: Estimate
            width = getattr(glyph, 'width', 500)
            return (0, -150, width, 700)
            
        except Exception:
            return (0, -150, 500, 700)
    
    def glyph_to_path_data(self, char, target_size=432):
        """Convert character to SVG path data."""
        if not self.font:
            raise ValueError("Font not loaded")
        
        char_code = ord(char)
        if char_code not in self.unicode_map:
            raise ValueError(f"Character '{char}' (U+{char_code:04X}) not in {self.font_config['name']}")
        
        glyph_name = self.unicode_map[char_code]
        glyph = self.glyph_set[glyph_name]
        
        # Get bounding box
        bbox = self.get_glyph_bbox(glyph)
        glyph_width = bbox[2] - bbox[0]
        glyph_height = bbox[3] - bbox[1]
        
        if glyph_width <= 0 or glyph_height <= 0:
            return "", bbox, 1.0, glyph_name
        
        # Calculate scale
        max_dimension = max(glyph_width, glyph_height)
        scale = target_size / max_dimension if max_dimension > 0 else 1.0
        
        # Create transform: scale and flip Y
        transform = Transform().scale(scale, -scale).translate(-bbox[0], -bbox[3])
        
        # Draw to path
        svg_pen = SVGPathPen(self.glyph_set)
        transform_pen = TransformPen(svg_pen, transform)
        glyph.draw(transform_pen)
        
        return svg_pen.getCommands(), bbox, scale, glyph_name
    
    def create_centered_svg(self, char, viewbox_size=1024, target_size=432, 
                           fill_color="black", stroke_color="none", stroke_width=0):
        """Create SVG with centered glyph."""
        try:
            # Check support
            supported, glyph_name, char_code = self.check_character_support(char)
            
            if not supported:
                # Try other fonts
                alt_font, alt_glyph_name, char_code = self.try_multiple_fonts(char)
                if alt_font:
                    print(f"⚠ '{char}' not in {self.font_name}, using {alt_font} instead", file=sys.stderr)
                    # Create converter for alternative font
                    alt_converter = UnicodeGlyphConverter(alt_font, auto_download=False)
                    return alt_converter.create_centered_svg(
                        char, viewbox_size, target_size, fill_color, stroke_color, stroke_width
                    )
                else:
                    raise ValueError(f"Character '{char}' not found in any available font")
            
            # Get path data
            path_data, bbox, scale, glyph_name = self.glyph_to_path_data(char, target_size)
            
            # Calculate centering
            glyph_width = bbox[2] - bbox[0]
            glyph_height = bbox[3] - bbox[1]
            scaled_width = glyph_width * scale
            scaled_height = glyph_height * scale
            
            center_x = (viewbox_size - scaled_width) / 2
            center_y = (viewbox_size - scaled_height) / 2
            
            # Build stroke attributes
            stroke_attrs = ""
            if stroke_width > 0:
                stroke_attrs = f' stroke="{stroke_color}" stroke-width="{stroke_width}"'
            
            # Build SVG
            svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     viewBox="0 0 {viewbox_size} {viewbox_size}"
     width="{viewbox_size}" 
     height="{viewbox_size}">
  <!-- Font: {self.font_name} -->
  <!-- Character: {char} (U+{char_code:04X}) -->
  <g transform="translate({center_x:.2f} {center_y:.2f})">
    <path d="{path_data}" fill="{fill_color}"{stroke_attrs}/>
  </g>
</svg>'''
            
            # Print info
            print(f"\n✓ Conversion successful", file=sys.stderr)
            print(f"  Character: {char} (U+{char_code:04X})", file=sys.stderr)
            print(f"  Font: {self.font_name}", file=sys.stderr)
            print(f"  Glyph: {glyph_name}", file=sys.stderr)
            print(f"  Size: {scaled_width:.1f} × {scaled_height:.1f}", file=sys.stderr)
            print(f"  Position: ({center_x:.1f}, {center_y:.1f})", file=sys.stderr)
            
            return svg
            
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return self.create_error_svg(viewbox_size, str(e))
    
    def create_error_svg(self, viewbox_size, error_msg):
        """Create error SVG."""
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {viewbox_size} {viewbox_size}">
  <rect width="100%" height="100%" fill="#fff3cd"/>
  <text x="50%" y="50%" text-anchor="middle" dy="0" font-size="60" fill="#856404">
    <tspan x="50%" dy="-30">⚠ Error</tspan>
    <tspan x="50%" dy="40" font-size="40">{error_msg[:50]}</tspan>
  </text>
</svg>'''
    
    def create_path_only(self, char, target_size=432, fill_color="black"):
        """Return only the centered path element."""
        try:
            path_data, bbox, scale, glyph_name = self.glyph_to_path_data(char, target_size)
            
            if not path_data.strip():
                return f'<!-- Empty glyph -->'
            
            # Calculate centering
            glyph_width = bbox[2] - bbox[0]
            glyph_height = bbox[3] - bbox[1]
            scaled_width = glyph_width * scale
            scaled_height = glyph_height * scale
            
            center_x = (1024 - scaled_width) / 2
            center_y = (1024 - scaled_height) / 2
            
            return f'<path d="{path_data}" transform="translate({center_x:.2f} {center_y:.2f})" fill="{fill_color}"/>'
            
        except Exception as e:
            return f'<!-- Error: {e} -->'

def main():
    parser = argparse.ArgumentParser(
        description='Convert Unicode glyphs to SVG using multiple fonts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f'''
Available fonts:
  symbola   - Historical Unicode symbol font (broadest coverage)
  notomath  - Modern Noto Sans Math (clean mathematical symbols)
  notosans  - General purpose sans-serif font

Examples:
  # Download all fonts
  python {os.path.basename(__file__)} --download-all
  
  # Convert with specific font
  python {os.path.basename(__file__)} ⨳ --font notomath -o math.svg
  python {os.path.basename(__file__)} ★ --font symbola -o star.svg
  
  # Auto-select font (tries notomath → symbola → notosans)
  python {os.path.basename(__file__)} ⨳ --auto -o symbol.svg
  
  # Batch conversion
  python {os.path.basename(__file__)} "⨳★↯⊕⊗" --batch symbols/
        '''
    )
    
    # Font management
    font_group = parser.add_argument_group('Font Management')
    font_group.add_argument('--download', choices=list(FONTS.keys()) + ['all'],
                          help='Download specific font or all fonts')
    font_group.add_argument('--list-fonts', action='store_true',
                          help='List available fonts')
    font_group.add_argument('--font-info', metavar='FONT',
                          help='Show information about font')
    
    # Conversion
    conv_group = parser.add_argument_group('Conversion')
    conv_group.add_argument('char', nargs='?', help='Unicode character to convert')
    conv_group.add_argument('-o', '--output', help='Output SVG file')
    conv_group.add_argument('--font', choices=list(FONTS.keys()), default='symbola',
                          help='Font to use (default: symbola)')
    conv_group.add_argument('--auto', action='store_true',
                          help='Auto-select font (notomath → symbola → notosans)')
    
    # Output settings
    output_group = parser.add_argument_group('Output Settings')
    output_group.add_argument('-s', '--size', type=int, default=432,
                            help='Glyph size within viewBox (default: 432)')
    output_group.add_argument('-v', '--viewbox', type=int, default=1024,
                            help='SVG viewBox size (default: 1024)')
    output_group.add_argument('-c', '--color', default='black',
                            help='Fill color (default: black)')
    output_group.add_argument('--stroke', default='none',
                            help='Stroke color (default: none)')
    output_group.add_argument('--stroke-width', type=float, default=0,
                            help='Stroke width (default: 0)')
    
    # Output format
    format_group = parser.add_argument_group('Output Format')
    format_group.add_argument('-p', '--path-only', action='store_true',
                            help='Output only path element')
    format_group.add_argument('-m', '--minimal', action='store_true',
                            help='Minimal SVG without comments')
    
    # Information
    info_group = parser.add_argument_group('Information')
    info_group.add_argument('--check', metavar='CHAR',
                          help='Check character support in all fonts')
    info_group.add_argument('--compare', metavar='CHAR',
                          help='Compare character in all fonts')
    
    # Batch operations
    batch_group = parser.add_argument_group('Batch Operations')
    batch_group.add_argument('--batch', metavar='STRING',
                           help='Convert all characters in string')
    batch_group.add_argument('--batch-dir', metavar='DIR', default='glyphs',
                           help='Output directory for batch (default: glyphs)')
    
    args = parser.parse_args()
    
    # Font management commands
    if args.list_fonts:
        print("Available fonts:", file=sys.stderr)
        for font_id, config in FONTS.items():
            exists = os.path.exists(os.path.join(FONTS_DIR, config['name']))
            status = "✓" if exists else "✗"
            print(f"  {font_id:10} {status} {config['description']}", file=sys.stderr)
        return
    
    if args.download:
        if args.download == 'all':
            for font_id in FONTS:
                try:
                    print(f"\n=== Downloading {font_id} ===", file=sys.stderr)
                    converter = UnicodeGlyphConverter(font_id, auto_download=True)
                except Exception as e:
                    print(f"  Failed: {e}", file=sys.stderr)
        else:
            try:
                converter = UnicodeGlyphConverter(args.download, auto_download=True)
                print(f"\n✓ {args.download} downloaded successfully", file=sys.stderr)
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
        return
    
    if args.font_info:
        if args.font_info not in FONTS:
            print(f"Unknown font: {args.font_info}", file=sys.stderr)
            return
        
        font_path = os.path.join(FONTS_DIR, FONTS[args.font_info]['name'])
        if os.path.exists(font_path):
            try:
                converter = UnicodeGlyphConverter(args.font_info, auto_download=False)
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
        else:
            print(f"Font not downloaded: {font_path}", file=sys.stderr)
        return
    
    # Check character in all fonts
    if args.check:
        char = args.check[0] if args.check else '⨳'
        print(f"Checking '{char}' (U+{ord(char):04X}):", file=sys.stderr)
        
        for font_id in FONTS:
            font_path = os.path.join(FONTS_DIR, FONTS[font_id]['name'])
            if os.path.exists(font_path):
                try:
                    converter = UnicodeGlyphConverter(font_id, auto_download=False)
                    supported, glyph_name, char_code = converter.check_character_support(char)
                    status = "✓" if supported else "✗"
                    print(f"  {font_id:10} {status} {glyph_name or 'Not supported'}", file=sys.stderr)
                except Exception as e:
                    print(f"  {font_id:10} ✗ Error: {e}", file=sys.stderr)
            else:
                print(f"  {font_id:10} ✗ Not downloaded", file=sys.stderr)
        return
    
    # Compare character in all fonts
    if args.compare:
        char = args.compare[0] if args.compare else '⨳'
        char_code = ord(char)
        
        print(f"\nComparing '{char}' (U+{char_code:04X}) across fonts:", file=sys.stderr)
        print("-" * 60, file=sys.stderr)
        
        converters = {}
        for font_id in FONTS:
            font_path = os.path.join(FONTS_DIR, FONTS[font_id]['name'])
            if os.path.exists(font_path):
                try:
                    converters[font_id] = UnicodeGlyphConverter(font_id, auto_download=False)
                except:
                    pass
        
        if not converters:
            print("No fonts available. Download fonts first.", file=sys.stderr)
            return
        
        # Create comparison SVG
        viewbox_size = 1024
        columns = min(3, len(converters))
        rows = (len(converters) + columns - 1) // columns
        cell_size = viewbox_size // max(columns, rows)
        
        svg_parts = []
        svg_parts.append(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     viewBox="0 0 {viewbox_size} {viewbox_size}"
     width="{viewbox_size}" 
     height="{viewbox_size}">''')
        
        svg_parts.append(f'  <text x="50%" y="5%" text-anchor="middle" font-size="60">')
        svg_parts.append(f'    {char} (U+{char_code:04X})')
        svg_parts.append(f'  </text>')
        
        for i, (font_id, converter) in enumerate(converters.items()):
            col = i % columns
            row = i // columns
            
            center_x = (col + 0.5) * cell_size
            center_y = (row + 0.5) * cell_size + 100
            
            supported, glyph_name, _ = converter.check_character_support(char)
            
            if supported:
                try:
                    path_data, bbox, scale, _ = converter.glyph_to_path_data(char, cell_size * 0.6)
                    
                    glyph_width = bbox[2] - bbox[0]
                    glyph_height = bbox[3] - bbox[1]
                    scaled_width = glyph_width * scale
                    scaled_height = glyph_height * scale
                    
                    path_x = center_x - scaled_width / 2
                    path_y = center_y - scaled_height / 2
                    
                    svg_parts.append(f'  <g transform="translate({path_x:.1f} {path_y:.1f})">')
                    svg_parts.append(f'    <path d="{path_data}" fill="black"/>')
                    svg_parts.append(f'  </g>')
                    
                    # Font label
                    svg_parts.append(f'  <text x="{center_x}" y="{center_y + cell_size*0.4}"')
                    svg_parts.append(f'        text-anchor="middle" font-size="30">')
                    svg_parts.append(f'    {font_id} ✓')
                    svg_parts.append(f'  </text>')
                    
                except Exception as e:
                    svg_parts.append(f'  <text x="{center_x}" y="{center_y}"')
                    svg_parts.append(f'        text-anchor="middle" font-size="40" fill="red">')
                    svg_parts.append(f'    Error')
                    svg_parts.append(f'  </text>')
            else:
                svg_parts.append(f'  <text x="{center_x}" y="{center_y}"')
                svg_parts.append(f'        text-anchor="middle" font-size="60" fill="#ccc">')
                svg_parts.append(f'    ✗')
                svg_parts.append(f'  </text>')
                
                svg_parts.append(f'  <text x="{center_x}" y="{center_y + cell_size*0.4}"')
                svg_parts.append(f'        text-anchor="middle" font-size="30" fill="#999">')
                svg_parts.append(f'    {font_id}')
                svg_parts.append(f'  </text>')
        
        svg_parts.append('</svg>')
        
        output_file = f"compare_{char}.svg"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(svg_parts))
        
        print(f"Comparison saved to: {output_file}", file=sys.stderr)
        return
    
    # Batch conversion
    if args.batch:
        chars = args.batch
        output_dir = args.batch_dir
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"Batch converting: {chars}", file=sys.stderr)
        
        for i, char in enumerate(chars):
            try:
                if args.auto:
                    # Auto-select font
                    converter = None
                    for font_id in ['notomath', 'symbola', 'notosans']:
                        font_path = os.path.join(FONTS_DIR, FONTS[font_id]['name'])
                        if os.path.exists(font_path):
                            try:
                                temp_conv = UnicodeGlyphConverter(font_id, auto_download=False)
                                if temp_conv.check_character_support(char)[0]:
                                    converter = temp_conv
                                    break
                            except:
                                continue
                    
                    if not converter:
                        print(f"  {i+1:3d}. {char}: No font supports this character", file=sys.stderr)
                        continue
                else:
                    converter = UnicodeGlyphConverter(args.font, auto_download=False)
                
                svg = converter.create_centered_svg(
                    char, args.viewbox, args.size,
                    args.color, args.stroke, args.stroke_width
                )
                
                # Create filename
                hex_code = f"U{ord(char):04X}"
                font_suffix = f"_{converter.font_name}" if args.auto else ""
                filename = f"{i:03d}_{hex_code}{font_suffix}.svg"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(svg)
                
                print(f"  {i+1:3d}. {char} → {filename}", file=sys.stderr)
                
            except Exception as e:
                print(f"  {i+1:3d}. {char}: ERROR - {e}", file=sys.stderr)
        
        print(f"\nBatch complete. Files in: {output_dir}/", file=sys.stderr)
        return
    
    # Single character conversion
    if not args.char:
        parser.print_help()
        return
    
    char = args.char[0] if len(args.char) > 1 else args.char
    
    try:
        if args.auto:
            # Try fonts in order: notomath → symbola → notosans
            font_used = None
            converter = None
            
            for font_id in ['notomath', 'symbola', 'notosans']:
                font_path = os.path.join(FONTS_DIR, FONTS[font_id]['name'])
                if os.path.exists(font_path):
                    try:
                        temp_conv = UnicodeGlyphConverter(font_id, auto_download=False)
                        if temp_conv.check_character_support(char)[0]:
                            converter = temp_conv
                            font_used = font_id
                            break
                    except:
                        continue
            
            if not converter:
                # Try any available font
                for font_id in FONTS:
                    font_path = os.path.join(FONTS_DIR, FONTS[font_id]['name'])
                    if os.path.exists(font_path):
                        try:
                            converter = UnicodeGlyphConverter(font_id, auto_download=False)
                            font_used = font_id
                            break
                        except:
                            continue
            
            if not converter:
                raise ValueError("No fonts available. Download fonts first.")
            
            print(f"Auto-selected font: {font_used}", file=sys.stderr)
        else:
            converter = UnicodeGlyphConverter(args.font, auto_download=False)
        
        if args.path_only:
            path = converter.create_path_only(char, args.size, args.color)
            print(path)
        else:
            svg = converter.create_centered_svg(
                char, args.viewbox, args.size,
                args.color, args.stroke, args.stroke_width
            )
            
            if args.minimal:
                import re
                svg = re.sub(r'<!--.*?-->', '', svg, flags=re.DOTALL)
                svg = re.sub(r'\n\s*\n', '\n', svg)
                svg = svg.strip()
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(svg)
                print(f"\nSVG saved to: {args.output}", file=sys.stderr)
            else:
                print(svg)
                
    except FileNotFoundError as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        print(f"\nDownload fonts first:", file=sys.stderr)
        print(f"  python {os.path.basename(__file__)} --download-all", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()
