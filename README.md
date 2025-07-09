# 🖼️ Advanced Image Editor - Python Implementation

A comprehensive image processing application that provides various image manipulation operations including filtering, transformations, and artistic effects. Built using PIL/Pillow with both interactive console interface and command-line batch processing capabilities.

## 🎨 Features Overview

This image editor implements sophisticated image processing algorithms including:

- **Color Space Conversion** (RGB ↔ Grayscale)
- **Image Filtering** (Blur, Edge Detection, Custom Kernels)
- **Geometric Transformations** (Resize, Rotate, Scale)
- **Artistic Effects** (Quantization, Cartoonification)
- **Advanced Algorithms** (Bilinear Interpolation, Adaptive Thresholding)

## 🚀 Core Capabilities

### Image Processing Operations

#### 1. **Channel Separation & Combination**
```python
def separate_channels(image: ColoredImage) -> List[SingleChannelImage]:
    """Separates RGB image into individual color channels"""

def combine_channels(channels: List[SingleChannelImage]) -> ColoredImage:
    """Combines separate channels back into RGB image"""
```

#### 2. **Color Space Conversion**
```python
def RGB2grayscale(colored_image: ColoredImage) -> SingleChannelImage:
    """Converts RGB to grayscale using standard luminance formula:
    Gray = 0.299*R + 0.587*G + 0.114*B"""
```

#### 3. **Kernel-Based Filtering**
```python
def apply_kernel(image: SingleChannelImage, kernel: Kernel) -> SingleChannelImage:
    """Applies convolution kernel for various effects:
    - Blur kernels for smoothing
    - Edge detection kernels
    - Custom filter kernels"""
```

#### 4. **Advanced Resizing with Bilinear Interpolation**
```python
def bilinear_interpolation(image: SingleChannelImage, y: float, x: float) -> int:
    """High-quality pixel interpolation for smooth resizing"""

def resize(image: SingleChannelImage, new_height: int, new_width: int) -> SingleChannelImage:
    """Resizes image maintaining quality through interpolation"""
```

#### 5. **Geometric Transformations**
```python
def rotate_90(image: Image, direction: str) -> Image:
    """Rotates image 90 degrees left or right using matrix operations"""
```

#### 6. **Edge Detection**
```python
def get_edges(image: SingleChannelImage, blur_size: int, block_size: int, c: float) -> SingleChannelImage:
    """Advanced edge detection using adaptive thresholding:
    1. Apply blur to reduce noise
    2. Calculate local adaptive threshold
    3. Apply threshold to create binary edge map"""
```

#### 7. **Color Quantization**
```python
def quantize(image: SingleChannelImage, N: int) -> SingleChannelImage:
    """Reduces color palette to N levels using mathematical quantization"""
```

## 📁 Project Structure

```
ex5/
├── image_editor.py         # Main interactive image editor
├── ex5_helper.py          # PIL interface and utility functions
├── test_image_editor.py   # Comprehensive test suite
├── test.py               # Additional testing utilities
├── examples/             # Sample images for testing
│   ├── sample1.png
│   ├── sample2.jpg
│   └── ...
└── __pycache__/          # Python compiled files
```

## 🛠️ Technical Implementation

### Advanced Algorithms

#### **Bilinear Interpolation**
High-quality image resizing using mathematical interpolation:

```python
def bilinear_interpolation(image, y, x):
    """
    Calculates new pixel value using weighted average of 4 nearest neighbors
    
    Algorithm:
    1. Find 4 surrounding pixels (top-left, top-right, bottom-left, bottom-right)
    2. Calculate distance weights (delta_x, delta_y)
    3. Compute weighted average: 
       result = a*(1-dx)*(1-dy) + b*dy*(1-dx) + c*dx*(1-dy) + d*dx*dy
    """
```

#### **Adaptive Thresholding for Edge Detection**
```python
def get_edges(image, blur_size, block_size, c):
    """
    Sophisticated edge detection algorithm:
    
    1. Pre-blur: Apply Gaussian blur to reduce noise
    2. Local threshold: Calculate adaptive threshold for each pixel
    3. Binary classification: Classify pixels as edge/non-edge
    4. Post-processing: Clean up edge map
    """
```

#### **Kernel Convolution**
```python
def apply_kernel(image, kernel):
    """
    Applies convolution operation with proper boundary handling:
    
    - Padding strategy: Mirror pixels at boundaries
    - Floating-point precision: Maintains accuracy during calculation
    - Clamping: Ensures output values stay in valid range [0, 255]
    """
```

### Image Processing Pipeline

#### **Multi-Channel Processing**
For colored images, operations are applied to each channel independently:

```python
# Example: Blur colored image
channels = separate_channels(image)
blurred_channels = []
for channel in channels:
    blurred_channels.append(apply_kernel(channel, blur_kernel(size)))
result = combine_channels(blurred_channels)
```

#### **Quality Preservation**
- **Floating-Point Arithmetic:** Intermediate calculations use float precision
- **Proper Rounding:** Mathematical rounding for pixel values
- **Boundary Handling:** Intelligent edge pixel management
- **Type Safety:** Consistent data type handling throughout pipeline

## 🎮 Interactive Interface

### Console-Based Menu System
```
Image Editor Options:
1. Convert to Grayscale
2. Apply Blur Filter
3. Resize Image
4. Rotate 90 Degrees
5. Edge Detection
6. Quantize Colors
7. Show Current Image
8. Save and Exit
```

### Usage Examples

#### **Basic Operations**
```bash
# Start image editor
python image_editor.py sample_image.png

# Interactive session:
> choose the option you would like to implement: 2
> please choose kernel size: 5
> Image blurred successfully!

> choose the option you would like to implement: 3
> please choose row, col: 800,600
> Image resized successfully!
```

#### **Advanced Processing**
```bash
# Edge detection with custom parameters
> choose the option you would like to implement: 5
> Select 3 comma separated values: blur_size, block_size, c: 3,5,10
> Edges detected successfully!

# Color quantization
> choose the option you would like to implement: 6
> Enter number of tones: 8
> Image quantized to 8 colors!
```

## 🧪 Testing Framework

### Comprehensive Test Coverage
```python
# Example test cases
@pytest.mark.parametrize("image, expected", [
    ([[255, 0], [0, 255]], [[127.5, 127.5], [127.5, 127.5]]),
    # More test cases...
])
def test_blur_kernel():
    """Tests blur kernel generation and application"""

def test_bilinear_interpolation():
    """Tests interpolation accuracy and boundary conditions"""

def test_edge_detection():
    """Tests edge detection with various threshold parameters"""
```

### Test Categories
- **Unit Tests:** Individual function validation
- **Integration Tests:** Complete processing pipeline
- **Edge Cases:** Boundary conditions and error handling
- **Performance Tests:** Processing time and memory usage

## 🔧 Configuration & Customization

### Kernel Customization
```python
# Custom blur kernel
def blur_kernel(size):
    """Creates NxN averaging kernel for blur effect"""
    return [[1.0/(size**2) for _ in range(size)] for _ in range(size)]

# Custom edge detection kernels
sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
sobel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
```

### Processing Parameters
- **Blur Size:** Kernel size for smoothing (odd integers: 3, 5, 7, ...)
- **Block Size:** Local threshold window size for edge detection
- **Threshold Constant:** Fine-tuning parameter for edge sensitivity
- **Quantization Levels:** Number of color levels (2-256)

## 🎯 Advanced Features

### **Cartoonify Effect** (Available in extended version)
```python
def cartoonify(image, blur_size, th_block_size, th_c, quant_num_shades):
    """
    Creates cartoon-like effect by combining:
    1. Edge detection for outlines
    2. Color quantization for flat colors
    3. Mask blending for final result
    """
```

### **Scale-Down with Aspect Ratio Preservation**
```python
def scale_down_colored_image(image, max_size):
    """
    Intelligently scales down large images:
    - Maintains aspect ratio
    - Uses high-quality interpolation
    - Applies to each color channel independently
    """
```

### **Batch Processing Support**
The framework supports batch processing multiple images with consistent parameters.

## 💻 Technical Requirements

- **Python 3.9+**
- **PIL/Pillow** for image I/O operations
- **NumPy** (optional) for enhanced performance
- **pytest** for running test suite

### Installation
```bash
pip install Pillow pytest
python image_editor.py your_image.png
```

## 🚀 Performance Optimizations

### **Memory Efficiency**
- **In-place Operations:** Where possible, minimizes memory copying
- **Channel Processing:** Processes channels independently for memory management
- **Lazy Loading:** Loads images only when needed

### **Algorithm Optimizations**
- **Kernel Separation:** Uses separable kernels when possible
- **Boundary Optimization:** Efficient edge pixel handling
- **Type Optimization:** Uses appropriate data types for calculations

## 🎓 Educational Value

This project demonstrates:

- **Digital Signal Processing:** Convolution, filtering, sampling theory
- **Computer Graphics:** Geometric transformations, interpolation algorithms
- **Mathematical Concepts:** Linear algebra, discrete mathematics
- **Algorithm Design:** Optimization techniques, boundary condition handling
- **Software Engineering:** Modular design, testing practices, documentation
- **Image Processing Theory:** Color spaces, spatial domain filtering
- **User Interface Design:** Interactive console applications

### **Key Algorithms Implemented**
1. **Bilinear Interpolation** - Smooth image resizing
2. **Convolution** - Kernel-based filtering
3. **Adaptive Thresholding** - Context-aware edge detection
4. **Matrix Operations** - Rotation and transformation
5. **Color Space Conversion** - RGB to grayscale mapping
6. **Quantization** - Color palette reduction

## 🔍 Code Quality Features

- **Type Hints:** Complete type annotations for better code clarity
- **Documentation:** Comprehensive docstrings for all functions
- **Error Handling:** Robust input validation and error management
- **Modular Design:** Clean separation of concerns
- **Testing:** Extensive test coverage with pytest framework

---

*This image editor showcases professional-level image processing implementation, demonstrating both theoretical understanding of computer vision concepts and practical software development skills. Perfect for demonstrating algorithmic thinking, mathematical computation, and user interface design capabilities.*
