"""Core stereogram generation algorithms."""

import numpy as np
from typing import Optional, Tuple

# Constants
GRAYSCALE_RANGE = 256
GRAYSCALE_MID = 128


def generate_depth_map(
    width: int,
    height: int,
    pattern: str = "sine",
    amplitude: float = 50.0,
) -> np.ndarray:
    """Generate a depth map for the stereogram.
    
    Args:
        width: Width of the depth map in pixels
        height: Height of the depth map in pixels
        pattern: Type of pattern ('sine', 'circles', 'pyramid', 'random', 'dinosaur')
        amplitude: Amplitude of the depth variation (0-255)
    
    Returns:
        A 2D numpy array with depth values (0-255)
    """
    if pattern == "sine":
        # Create a sinusoidal wave pattern
        x = np.linspace(0, 4 * np.pi, width)
        y = np.linspace(0, 4 * np.pi, height)
        X, Y = np.meshgrid(x, y)
        depth = (np.sin(X) + np.sin(Y)) * amplitude / 2 + GRAYSCALE_MID
        
    elif pattern == "circles":
        # Create concentric circles
        center_x, center_y = width // 2, height // 2
        y, x = np.ogrid[:height, :width]
        distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        depth = (np.sin(distance / 10) * amplitude + GRAYSCALE_MID)
        
    elif pattern == "pyramid":
        # Create a pyramid shape
        y, x = np.ogrid[:height, :width]
        center_x, center_y = width // 2, height // 2
        depth = amplitude * (1 - np.maximum(
            np.abs(x - center_x) / center_x,
            np.abs(y - center_y) / center_y
        )) + GRAYSCALE_MID - amplitude / 2
        
    elif pattern == "random":
        # Create smooth random terrain
        # Simple implementation without scipy dependency
        # Use multiple passes of averaging for smoothing effect
        depth = np.random.rand(height, width) * amplitude + GRAYSCALE_MID - amplitude / 2
        
        # Apply simple smoothing by averaging with neighbors
        kernel_size = 5
        smoothed = depth.copy()
        for _ in range(3):  # Multiple passes for smoother result
            for y in range(kernel_size // 2, height - kernel_size // 2):
                for x in range(kernel_size // 2, width - kernel_size // 2):
                    neighborhood = depth[
                        y - kernel_size // 2:y + kernel_size // 2 + 1,
                        x - kernel_size // 2:x + kernel_size // 2 + 1
                    ]
                    smoothed[y, x] = np.mean(neighborhood)
            depth = smoothed.copy()
    elif pattern == "dinosaur":
        from PIL import Image, ImageDraw, ImageFont

        base = np.full((height, width), GRAYSCALE_MID, dtype=np.uint8)
        img = Image.fromarray(base)
        draw = ImageDraw.Draw(img)

        foreground = int(np.clip(GRAYSCALE_MID + amplitude * 0.6, 0, GRAYSCALE_RANGE - 1))
        logo_depth = int(np.clip(GRAYSCALE_MID - amplitude * 0.4, 0, GRAYSCALE_RANGE - 1))

        body_box = (
            int(width * 0.1),
            int(height * 0.5),
            int(width * 0.7),
            int(height * 0.8),
        )
        draw.ellipse(body_box, fill=foreground)

        tail_points = [
            (int(width * 0.1), int(height * 0.65)),
            (int(width * 0.02), int(height * 0.55)),
            (int(width * 0.15), int(height * 0.6)),
        ]
        draw.polygon(tail_points, fill=foreground)

        draw.rectangle(
            [
                (int(width * 0.65), int(height * 0.3)),
                (int(width * 0.75), int(height * 0.55)),
            ],
            fill=foreground,
        )
        draw.ellipse(
            [
                (int(width * 0.73), int(height * 0.25)),
                (int(width * 0.83), int(height * 0.35)),
            ],
            fill=foreground,
        )

        leg_width = int(width * 0.06)
        leg_height = int(height * 0.18)
        leg_y = int(height * 0.78)
        for offset in (0.25, 0.5):
            x_start = int(width * offset)
            draw.rectangle(
                [
                    (x_start, leg_y),
                    (x_start + leg_width, leg_y + leg_height),
                ],
                fill=foreground,
            )

        font = ImageFont.load_default()
        text = "DMC"
        draw.text(
            (int(width * 0.55), int(height * 0.15)),
            text,
            font=font,
            fill=logo_depth,
        )
        depth = np.array(img, dtype=np.uint8)
    else:
        raise ValueError(f"Unknown pattern: {pattern}")
    
    # Clip values to valid range
    return np.clip(depth, 0, GRAYSCALE_RANGE - 1).astype(np.uint8)


def generate_random_pattern(width: int, height: int, pattern_width: int) -> np.ndarray:
    """Generate a random pattern strip for the stereogram.
    
    Args:
        width: Total width of the image
        height: Height of the image
        pattern_width: Width of the repeating pattern strip
    
    Returns:
        A 2D numpy array with random grayscale pattern
    """
    # Generate random pattern strip
    pattern = np.random.randint(0, GRAYSCALE_RANGE, (height, pattern_width), dtype=np.uint8)
    return pattern


def generate_stereogram(
    width: int = 800,
    height: int = 600,
    pattern_type: str = "sine",
    depth_amplitude: float = 50.0,
    strip_width: int = 100,
    eye_separation: float = 0.12,
    depth_scale: float = 0.3,
) -> np.ndarray:
    """Generate a magic eye stereogram image.
    
    This creates a single-image random-dot stereogram (SIRDS) where a 3D shape
    can be perceived when viewed with the proper technique (parallel or cross-eyed viewing).
    
    Args:
        width: Width of the output image in pixels
        height: Height of the output image in pixels
        pattern_type: Type of depth pattern ('sine', 'circles', 'pyramid', 'random', 'dinosaur')
        depth_amplitude: Amplitude of depth variation (higher = more depth)
        strip_width: Width of the initial random pattern strip
        eye_separation: Eye separation as fraction of width (affects viewing distance)
        depth_scale: Scale factor for depth effect (0-1)
    
    Returns:
        A 2D numpy array containing the stereogram image (grayscale, 0-255)
    """
    # Generate depth map
    depth_map = generate_depth_map(width, height, pattern_type, depth_amplitude)
    
    # Create output image
    stereogram = np.zeros((height, width), dtype=np.uint8)
    
    # Generate initial random pattern strip
    pattern = generate_random_pattern(width, height, strip_width)
    stereogram[:, :strip_width] = pattern
    
    # Generate stereogram using the depth map
    # This implements the basic stereogram algorithm
    for x in range(strip_width, width):
        for y in range(height):
            # Calculate the shift based on depth
            # Depth affects how far we look back in the image
            depth_value = int(depth_map[y, x])
            shift = int((depth_value - GRAYSCALE_MID) * depth_scale * eye_separation * width / GRAYSCALE_RANGE)
            
            # Reference pixel position
            ref_x = x - strip_width - shift
            
            if ref_x >= 0 and ref_x < x:
                stereogram[y, x] = stereogram[y, ref_x]
            else:
                # If reference is out of bounds, use random value
                stereogram[y, x] = np.random.randint(0, GRAYSCALE_RANGE, dtype=np.uint8)
    
    return stereogram


def save_as_geotiff(
    stereogram: np.ndarray,
    output_path: str,
    bounds: Optional[Tuple[float, float, float, float]] = None,
    crs: str = "EPSG:4326",
) -> None:
    """Save the stereogram as a GeoTIFF file.
    
    Args:
        stereogram: The stereogram image array
        output_path: Path to save the GeoTIFF file
        bounds: Geographic bounds as (min_x, min_y, max_x, max_y).
                If None, uses default bounds (0, 0, width, height)
        crs: Coordinate reference system (default: WGS84)
    """
    import rasterio
    from rasterio.transform import from_bounds
    
    height, width = stereogram.shape
    
    # Set default bounds if not provided
    if bounds is None:
        bounds = (0.0, 0.0, float(width), float(height))
    
    # Calculate transform from bounds
    transform = from_bounds(*bounds, width, height)
    
    # Save as GeoTIFF
    with rasterio.open(
        output_path,
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=1,
        dtype=stereogram.dtype,
        crs=crs,
        transform=transform,
        compress='lzw',
    ) as dst:
        dst.write(stereogram, 1)
        # Add description
        dst.update_tags(1, DESCRIPTION='Magic Eye Stereogram')
        dst.set_band_description(1, 'Magic Eye Stereogram')
