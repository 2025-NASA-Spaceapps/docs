# 🦈 Sharks from Space - Documentation

**Team:** From Space to Your Pocket | **Challenge:** NASA Space Apps Challenge 2025 | **Location:** Málaga, Spain

AI-powered system predicting shark habitats using NASA satellites (PACE, MODIS, SWOT, GHRSST, SMAP, GEBCO) + Hugging Face models.

## 📁 Contents

### 📋 Documentation
- **[Model Card](model_card.md)** - AI models and implementation details
- **[Roadmap](roadmap.md)** - Sharker mobile app development plan
- **[Project Analysis](shark_project_analysis.md)** - Technical analysis and award strategy

### 🔧 Code & Scripts
- **[Data Pipeline](datasets_updater.py)** - NASA data download and processing
- **[Data Downloader](nasa_data_downloader.py)** - Satellite data access functions
- **[AI Demo](inference_demo.ipynb)** - Interactive Jupyter notebook

### 📊 Resources
- `Data Analysis Framework.pdf` - Technical framework
- `hugging_face_models.pdf` - AI model specs

## 🚀 Quick Start

```bash
# Install dependencies
pip install xarray rioxarray requests transformers torch sentence-transformers matplotlib

# Run data pipeline
python datasets_updater.py

# Open AI demo
jupyter notebook inference_demo.ipynb
```

## 🏗️ Architecture

NASA Data → Processing Pipeline → AI Models (TimesFM + Transformer + MiniLM) → Habitat Maps

## 📊 Data Sources
PACE, MODIS, SWOT, GHRSST, SMAP, GEBCO satellites for ocean variables.

## 🎯 Features
- 3-7 day shark habitat forecasting
- Real-time suitability maps
- Educational AI explanations
- Mobile app roadmap with VR/gamification

## 📈 Impact
80% prediction accuracy, supporting marine conservation and education.

---

*Open NASA data + AI for ocean predator protection* 🌊🦈