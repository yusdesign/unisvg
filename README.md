UniSVG: Unicode Glyph to SVG Converter

A powerful Python tool that converts Unicode characters to clean, centered SVG paths using professional fonts.

✨ Features

# UniSVG: Unicode Glyph to SVG Converter

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Fonts](https://img.shields.io/badge/fonts-3%20included-orange.svg)
![Unicode](https://img.shields.io/badge/unicode-full%20support-purple.svg)

A powerful Python tool that converts Unicode characters to clean, centered SVG paths using professional fonts. Perfect for creating resolution-independent symbols, mathematical typesetting, and icon systems.

## 🎯 Quick Example

Here's what ⨳ (U+2A33) SMASH PRODUCT SIGN looks like converted with NotoSansMath:

<img src="smash_noto.svg" width="128" height="128" alt="⨳ symbol example">  

* *this svg xml*
```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     viewBox="0 0 1024 1024"
     width="1024" 
     height="1024">
  <!-- Font: notomath -->
  <!-- Character: ⨳ (U+2A33) -->
  <g transform="translate(342.50 296.00) scale(1)">
    <path d="M82.84235294117646 386.25882352941176 57.43058823529411 360.8470588235294 143.8305882352941 274.4470588235294 109.27058823529411 239.8870588235294 51.33176470588235 298.3341176470588 25.919999999999998 272.9223529411765 83.85882352941175 214.47529411764705 25.919999999999998 155.52 51.33176470588235 130.10823529411766 109.27058823529411 188.55529411764707 143.8305882352941 153.99529411764706 57.43058823529411 67.59529411764709 82.84235294117646 42.18352941176471 169.24235294117645 128.58352941176472 256.1505882352941 42.18352941176471 281.5623529411764 67.59529411764709 195.16235294117644 153.99529411764706 229.2141176470588 188.55529411764707 287.6611764705882 130.10823529411766 313.0729411764706 155.52 254.62588235294115 214.47529411764705 313.0729411764706 272.9223529411765 287.6611764705882 298.3341176470588 229.2141176470588 239.8870588235294 195.16235294117644 274.4470588235294 281.5623529411764 360.8470588235294 256.1505882352941 386.25882352941176 169.24235294117645 299.8588235294118ZM169.24235294117645 248.52705882352942 203.2941176470588 214.47529411764705 169.24235294117645 179.91529411764705 135.19058823529411 214.47529411764705Z" fill="olive" stroke="black"/>
  </g>
</svg>
```

```bash
# Convert ⨳ to SVG in one command
python unisvg.py ⨳ -o smash_noto.svg
```

✨ Features

· Multiple Font Support: Choose between historical Symbola, modern NotoSansMath, or general NotoSans
· Automatic Font Selection: Intelligently picks the best font for each character
· Perfect Centering: Mathematically precise centering within any viewBox
· Clean SVG Output: Pure path data without font rendering artifacts
· Batch Processing: Convert multiple characters at once
· Comparison Tools: See how characters render in different fonts

🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yusdesign/unisvg.git
cd unisvg

# Install dependencies
pip install fonttools

# Download all fonts
python unisvg.py --download-all

# Convert your first symbol
python unisvg.py ⨳ -o symbol.svg
```

📦 Font Choices

Font Best For Style Example
#### notomath  
Mathematical symbols Modern, clean <img src="smash_noto.svg" width="64" height="64" align="middle">  
#### symbola  
Historical symbols Broad Unicode <img src="examples/smash_symbola.svg" width="64" height="64" align="middle">  
#### notosans  
General text Sans-serif <img src="examples/fire.svg" width="64" height="64" align="middle">  

🎯 Usage Examples

Basic Conversion

```bash
# Convert any Unicode character
python unisvg.py ★ -o star.svg
python unisvg.py ♥ -o heart.svg
python unisvg.py ∞ -o infinity.svg
```

Advanced Options

```bash
# Auto-select best font
python unisvg.py ⨳ --auto -o symbol.svg

# Custom size and color
python unisvg.py ↯ -s 500 -c "#ff0000" -o fire.svg

# Path-only output (for embedding)
python unisvg.py ⊕ --path-only

# Batch convert symbols
python unisvg.py "⨳★↯⊕⊗∞∫∑∏√" --batch symbols/
```

🔍 Inspection & Comparison

```bash
# Check character support across all fonts
python unisvg.py --check ⨳

# Compare rendering in different fonts
python unisvg.py --compare ★

# List available fonts
python unisvg.py --list-fonts

# Get font statistics
python unisvg.py --font-info notomath
```

🏗️ Use Cases

1. Icon Systems

Generate SVG icons from Unicode symbols for web/app development:

```bash
python unisvg.py "★♥♠♣♦" --batch icons/ --size 512
```

2. Mathematical Publishing

Convert equations to vector graphics for papers/presentations:

```bash
python unisvg.py "∑∏∫∂∇±×÷√∞≈≠≤≥" --batch math/ --font notomath
```

3. Web Development

Create resolution-independent symbols:

```html
<!-- Generated SVG can be embedded directly -->
<svg viewBox="0 0 1024 1024" width="32" height="32">
  <path d="M..." fill="currentColor"/>
</svg>
```

4. Design Assets

Export Unicode characters for design software:

```bash
# Create design system symbols
python unisvg.py "→←↑↓↔↕↻↺" --batch arrows/ --size 1024
```

📁 Project Structure

```
unisvg/
├── unisvg.py                 # Main converter script
├── fonts/                    # Font storage
│   ├── Symbola.ttf          # Historical Unicode font
│   ├── NotoSansMath-Regular.ttf  # Modern math symbols
│   └── NotoSans-Regular.ttf # General sans-serif
├── examples/                 # Example outputs
│   ├── smash_noto.svg       # ⨳ in NotoSansMath
│   ├── smash_symbola.svg    # ⨳ in Symbola
│   └── smash_notosans.svg   # ⨳ in NotoSans
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

🔧 Installation

Requirements

· Python 3.7+
· fonttools library

Setup

```bash
# Install from PyPI (coming soon)
# pip install unisvg

# Or install dependencies manually
pip install fonttools
```

Font Management

Fonts are automatically downloaded on first use, or manually:

```bash
# Download all fonts
python unisvg.py --download-all

# Download specific font
python unisvg.py --download notomath
```

🧩 Technical Details

Output Specifications

· ViewBox: 1024×1024 (configurable)
· Glyph Size: 432 units by default (fits perfectly in viewBox)
· Centering: Mathematical precision to pixel grid
· Format: Pure SVG paths, no external dependencies

How It Works

1. Loads Unicode character from selected font
2. Extracts glyph outline as mathematical paths
3. Applies precise scaling and Y-axis flipping (fonts vs SVG)
4. Calculates exact centering within viewBox
5. Outputs clean SVG with transform matrix

📊 Performance

Operation Time Output Size
Single character ~0.1s 1-2 KB
Batch (10 chars) ~1s 10-20 KB
Batch (100 chars) ~10s 100-200 KB

🤝 Contributing

Contributions welcome! Here are some ideas:

1. Add More Fonts: Additional Unicode fonts
2. Web Interface: Flask/Django web app
3. CLI Improvements: More output formats
4. Performance: Optimize batch processing
5. Documentation: More examples and tutorials

Development Setup

```bash
git clone https://github.com/yusdesign/unisvg.git
cd unisvg
pip install -r requirements.txt
# Start developing!
```

📄 License

· Code: MIT License
· Fonts: Respective font licenses (SIL OFL, etc.)
· Symbols: Unicode Standard

🙏 Acknowledgments

· Unicode Consortium for character standards
· Google Fonts for Noto Sans family
· George Douros for Symbola font
· FontTools developers for Python library

📚 Resources

· Unicode Character Database
· Noto Fonts Project
· Symbola Font
· FontTools Documentation

---

Star this repo if you find it useful! ⭐

Created for designers and developers who need clean, scalable Unicode symbols without font rendering issues.


```bash
# Generate samples SVGs
python unisvg.py ⨳ --font notomath -o smash_noto.svg
python unisvg.py ⨳ --font symbola -o smash_symbola.svg
python unisvg.py ⨳ --font notosans -o smash_notosans.svg
```
