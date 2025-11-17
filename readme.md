# Product Image Generator

Automated 7-image set generation system for product listings (Amazon-style).

## Features

- Upload product images
- Automatic background removal
- Generate 7 professional product images:
  1. Main product (white background)
  2. Lifestyle scene
  3. Feature callouts with arrows
  4. Usage demonstration
  5. Dimensions/measurements
  6. Packaging/details
  7. Comparison/highlights
- Automatic logo placement
- Template-based system
- React frontend with drag-and-drop
- Async image generation with Celery

## Tech Stack

- **Backend**: Django 4.2 + DRF
- **Frontend**: React 18 + Vite + Tailwind CSS
- **Database**: PostgreSQL
- **Cache/Queue**: Redis + Celery
- **Image Processing**: Pillow + OpenCV + rembg
- **Deployment**: Docker + Docker Compose

## Quick Start

### 1. Clone Repository

```bash
git clone <your-repo>
cd product-image-generator