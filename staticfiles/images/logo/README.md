# Logo Directory

Place your Banbas Resort logo file here.

## Single Logo File Needed:

### Main Logo
- **Filename**: `logo.png` (required)
- **Size**: 200-300px width × 45px height recommended
- **Background**: Transparent (PNG with alpha channel)
- **Usage**: 
  - Navigation bar (adapts automatically to light/dark backgrounds)
  - Footer (converted to white automatically)
  - Favicon

## Smart Logo System:
The system automatically:
- **Transparent Navbar**: Inverts logo to white using CSS filters
- **White Navbar**: Shows logo in original colors  
- **Footer**: Converts logo to white for dark background
- **Fallback**: Shows "Banbas Resort" text if logo fails to load

## File Format Recommendations:
- **SVG**: Best for scalability and crisp display on all devices
- **PNG**: Good alternative with transparency support
- **Avoid**: JPEG (no transparency support)

## Colors to Match New Theme:
- **Primary Green**: #134a39
- **Secondary Green**: #1e6b54
- **Accent Green**: #2d8f6f
- **White/Light**: #ffffff for dark backgrounds

## Usage in Templates:
After adding your logo files, they will be automatically used in:
- Navigation bar (logo.png/svg)
- Footer (logo-footer.png/svg) 
- Transparent navbar (logo-white.png/svg)
- Favicon (logo-icon.png/svg)

The templates are already configured to look for these files!