# magicraster

Generate magic eye (autostereogram) raster GeoTIFF images! 👁️✨

## What is a Magic Eye?

A magic eye picture, also known as an autostereogram or Single Image Random Dot Stereogram (SIRDS), is a 2D image that creates a 3D visual effect when viewed with a specific technique. By focusing your eyes as if looking through the image, a hidden 3D shape emerges!

## Features

- Generate stereogram images with various depth patterns (sine waves, circles, pyramids, random terrain)
- Save output as georeferenced GeoTIFF files
- Customizable image dimensions, depth, and viewing parameters
- Command-line interface for easy use
- Python API for programmatic generation

## Installation

```bash
pip install -e .
```

Or with development dependencies:

```bash
pip install -e ".[dev]"
```

## Quick Start

### Command Line

Generate a basic magic eye image:

```bash
magicraster output.tif
```

Generate with custom pattern and size:

```bash
magicraster circles.tif --pattern circles --width 1024 --height 768 --depth 60
```

Generate with geographic bounds:

```bash
magicraster geo.tif --bounds="-122.5,37.5,-122.0,38.0" --crs EPSG:4326
```

### Python API

```python
from magicraster import generate_stereogram, save_as_geotiff

# Generate a stereogram
stereogram = generate_stereogram(
    width=800,
    height=600,
    pattern_type="sine",  # 'sine', 'circles', 'pyramid', or 'random'
    depth_amplitude=50.0,
)

# Save as GeoTIFF
save_as_geotiff(
    stereogram,
    "output.tif",
    bounds=(-122.5, 37.5, -122.0, 38.0),  # Optional geographic bounds
    crs="EPSG:4326",  # Coordinate reference system
)
```

## How to View Magic Eye Images

1. **Hold the image close** to your face (almost touching your nose)
2. **Focus your eyes** as if you're looking at something far away, through the image
3. **Slowly move the image away** from your face while maintaining that distant focus
4. **Be patient!** The 3D shape should emerge as your eyes adjust
5. Alternatively, try the "cross-eyed" method by crossing your eyes slightly

## Available Patterns

- **sine**: Sinusoidal wave pattern creating wave-like 3D surfaces
- **circles**: Concentric circles creating a bulls-eye 3D effect
- **pyramid**: A pyramid or cone shape emerging from the background
- **random**: Smooth random terrain-like surface
- **dinosaur**: A dinosaur silhouette with an embedded "DMC" logo for the Dinosaur Magic Company

## Command Line Options

```
positional arguments:
  output                Output GeoTIFF file path

optional arguments:
  --width WIDTH         Width of the image in pixels (default: 800)
  --height HEIGHT       Height of the image in pixels (default: 600)
  --pattern {sine,circles,pyramid,random,dinosaur}
                         Depth pattern type (default: sine)
  --depth DEPTH         Depth amplitude (0-100, default: 50.0)
  --strip-width STRIP_WIDTH
                        Width of the random pattern strip (default: 100)
  --bounds BOUNDS       Geographic bounds as 'minx,miny,maxx,maxy'
  --crs CRS             Coordinate reference system (default: EPSG:4326)
  --eye-separation EYE_SEPARATION
                        Eye separation factor (default: 0.12)
  --depth-scale DEPTH_SCALE
                        Depth scale factor (default: 0.3)
```

## Examples

Run the example script to generate multiple stereograms:

```bash
cd examples
python generate_examples.py
```

This creates several example files in the `output/` directory demonstrating different patterns and settings.

## Requirements

- Python >= 3.8
- numpy >= 1.20.0
- pillow >= 9.0.0
- rasterio >= 1.3.0

## How It Works

The magic eye effect is created using a stereogram algorithm:

1. A **depth map** is generated based on the chosen pattern (sine, circles, etc.)
2. A **random pattern strip** is created as the starting point
3. For each pixel, the algorithm calculates a horizontal shift based on the depth value
4. Pixels are copied from previous positions with this shift, creating the stereoscopic effect
5. When viewed correctly, your brain fuses the repeated patterns at different depths, creating a 3D image

The output is saved as a GeoTIFF, which means it includes geographic metadata and can be used in GIS applications like QGIS, ArcGIS, or with libraries like GDAL.

## License

MIT

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Credits

Inspired by the magic eye books and autostereogram art that fascinated people in the 1990s!
