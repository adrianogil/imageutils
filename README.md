# imageutils
Collection of small utilities for inspecting and transforming images.

## Features
- **Crop an image into a grid of tiles** (`src/crop_image.py`).
- **Report image sizes in a folder** and list image files per resolution (`src/list_images.py`).
- **Crop a single region by bounding box** (`src/python/dip/crop.py`).
- **Measure maximum width/height in a folder** (`src/python/dip/grid.py`).
- **Replace exact colors (optionally inverted)** (`src/python/dip/switch_color.py`).
- **Replace colors within a distance threshold** (`src/python/dip/switch_color_distance.py`).
- **Print a color histogram** (`src/python/dip/color_histogram.py`).
- **Create a flat-color image** (`src/python/dip/create_image.py`).
- **Convert images to LEGO color palettes** and generate a build map (`src/python/dip/lego/conv_lego_image.py`).
- **Open a simple image inspection GUI** with tooltip pixel data (`src/python/dip/gui/imtool.py`).
- **Convert base64-encoded images to PNG** (`src/python/imageutils/conv/conv_from_base64.py`).

## Requirements
Most scripts rely on:
- Python 3 (some legacy scripts also run on Python 2 if needed)
- [Pillow](https://python-pillow.org/)

Specific scripts need extra dependencies:
- `src/python/dip/create_image.py` and `src/python/dip/gui/imtool.py` require `numpy` and `opencv-python`.
- `src/python/dip/gui/imtool.py` requires `PySide2` and `matplotlib`.

## Command-line usage
Run all scripts from the repository root.

### Crop an image into tiles
Split an image into a grid of `COLUMNS x ROWS` tiles.
```bash
python src/crop_image.py <image_path> <columns> <rows>
```
Example:
```bash
python src/crop_image.py images/sample.png 3 2
```

### List images by resolution
Scan a folder and group images by size. Add `-v` to list file paths.
```bash
python src/list_images.py [path] [-v]
```
Example:
```bash
python src/list_images.py ./photos -v
```

### Crop a bounding box
```bash
python src/python/dip/crop.py <input> <output> <x0,y0,x1,y1>
```
Example:
```bash
python src/python/dip/crop.py in.png out.png 10,20,200,180
```

### Report max width/height in a folder
Prints the max width and max height among images in a folder.
```bash
python src/python/dip/grid.py <folder>
```

### Replace exact colors
Replace pixels matching a color with a new color. Use `-i` to invert the match.
```bash
python src/python/dip/switch_color.py <input> <output> <r,g,b[,a]> <r,g,b[,a]> [-i]
```
Example:
```bash
python src/python/dip/switch_color.py in.png out.png 255,0,0 0,0,0
```

### Replace colors within a distance
Replace pixels within a distance of a target color.
```bash
python src/python/dip/switch_color_distance.py <input> <output> <r,g,b[,a]> <distance> <r,g,b[,a]>
```
Example:
```bash
python src/python/dip/switch_color_distance.py in.png out.png 255,0,0 25 0,0,0
```

### Print a color histogram
Outputs colors sorted by frequency (ascending).
```bash
python src/python/dip/color_histogram.py <input>
```

### Create a flat-color image
Create an image of size `<width> x <height>` with BGR values.
```bash
python src/python/dip/create_image.py <output> <width> <height> <b> <g> <r>
```
Example:
```bash
python src/python/dip/create_image.py solid.png 256 256 0 128 255
```

### Convert an image to LEGO colors
Produces a LEGO palette image and a build map text file.
```bash
python src/python/dip/lego/conv_lego_image.py --image <input.png> --out <out_dir> [--colors colors.csv] [--xlen W --ylen H] [--scale S] [--block-size N]
```
Example:
```bash
python src/python/dip/lego/conv_lego_image.py --image input.png --out output --scale 0.25 --block-size 2
```

### Open the GUI image tool
```bash
python src/python/dip/gui/imtool.py <input>
```

### Convert base64 text to image
Reads a text file with base64 data and writes `output_image.png`.
```bash
python src/python/imageutils/conv/conv_from_base64.py <base64_file>
```
