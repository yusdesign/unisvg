UniSVG: Unicode Glyph to SVG Converter

A powerful Python tool that converts Unicode characters to clean, centered SVG paths using professional fonts.

✨ Features

· Multiple Font Support: Choose between historical Symbola, modern NotoSansMath, or general NotoSans
· Automatic Font Selection: Intelligently picks the best font for each character
· Perfect Centering: Mathematically precise centering within any viewBox
· Clean SVG Output: Pure path data without font rendering artifacts
· Batch Processing: Convert multiple characters at once
· Comparison Tools: See how characters render in different fonts

🚀 Quick Start

```bash
# 1. Download all fonts
python unisvg.py --download-all

# 2. Convert any Unicode character
python unisvg.py ⨳ -o symbol.svg

# 3. Batch convert math symbols
python unisvg.py "⨳★↯⊕⊗∞∫∑" --batch math_symbols/
```

📦 Font Choices

Font Best For Style
notomath Mathematical symbols Modern, clean
symbola Historical symbols Broad Unicode coverage
notosans General text Sans-serif

🎯 Examples

```bash
# Auto-select best font
python unisvg.py ⨳ --auto -o symbol.svg

# Force specific font
python unisvg.py ★ --font symbola -o star.svg

# Custom size and color
python unisvg.py ↯ -s 500 -c "#ff0000" -o fire.svg

# Path-only output (for embedding)
python unisvg.py ⊕ --path-only
```

🔍 Inspection Tools

```bash
# Check character support
python unisvg.py --check ⨳

# Compare across all fonts
python unisvg.py --compare ★

# List available fonts
python unisvg.py --list-fonts
```

🏗️ Use Cases

· Icon Systems: Generate SVG icons from Unicode symbols
· Mathematical Typesetting: Convert equations to vector graphics
· Web Development: Create resolution-independent symbols
· Design Tools: Export Unicode characters for design software
· Font Testing: Compare glyph rendering across fonts

🛠️ Technical Details

· Output: Pure SVG paths with perfect 1024×1024 viewBox
· Centering: Automatic mathematical centering
· Scaling: Configurable glyph size (default: 432 units)
· Format: Clean SVG without hinting or browser dependencies

📁 Project Structure

```
unisvg/
├── unisvg.py          # Main script
├── fonts/             # Font storage
│   ├── Symbola.ttf
│   ├── NotoSansMath-Regular.ttf
│   └── NotoSans-Regular.ttf
└── README.md          # This file
```

📄 License

MIT License - includes fonts under their respective licenses.

---

Next Steps: Consider adding font fallback chains, CSS class generation, or a web interface for this powerful conversion tool!

---

Note: This project successfully converts Unicode glyphs like ⨳ (U+2A33) to clean SVG paths, solving the common problem of inconsistent font rendering across platforms.
