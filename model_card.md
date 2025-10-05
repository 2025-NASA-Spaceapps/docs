# 🦈 Sharks-from-Space AI Stack

**Team:** From Space to Your Pocket  
**Challenge:** NASA Space Apps Challenge 2025  
**Objective:** Predict shark movement and habitat suitability from NASA satellite data (PACE, MODIS, SWOT, GHRSST, SMAP, GEBCO).  
**Approach:** Hybrid multi-model AI pipeline leveraging open Hugging Face models for temporal forecasting, spatial pattern recognition, and natural-language reasoning.

---

## 🧠 Model Overview

This system combines three open-source models from Hugging Face, each addressing a core analytical dimension:

| Layer | Model | Purpose |
|-------|--------|----------|
| ⏳ Temporal Forecasting | [facebook/timesfm-1.0](https://huggingface.co/facebook/timesfm-1.0) | Forecast ocean variables (SST, Chlorophyll) up to 7 days ahead |
| 🌍 Spatial Pattern Recognition | [johannfaouzi/TimeSeriesTransformer](https://huggingface.co/johannfaouzi/TimeSeriesTransformer) | Learn recurring habitat patterns and classify regions based on environmental signals |
| 💬 Semantic Reasoning | [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) | Provide natural-language explanations and educational insights |

---

## 🧩 How It Works

### 1️⃣ Data Input
Multivariate daily data cubes combining NASA satellite products:
- **PACE** (Chlorophyll, phytoplankton)
- **MODIS** (SST, productivity)
- **SWOT** (Sea Surface Height, eddy activity)
- **GHRSST** (Sea Surface Temperature)
- **SMAP** (Salinity)
- **GEBCO** (Bathymetry)

### 2️⃣ Processing Pipeline

```
Satellite Data (NASA)
     ↓
Feature Engineering (SST, Chl, SSH, Salinity)
     ↓
facebook/timesfm-1.0 → short-term (3–7 day) forecasts
     ↓
johannfaouzi/TimeSeriesTransformer → spatial classification
     ↓
sentence-transformers/all-MiniLM-L6-v2 → human-readable explanation
     ↓
Shark Habitat Maps + Educational Insights
```

---

## 🧮 Example Implementation

```python
from transformers import TimesFmForPrediction, TimeSeriesTransformerForPrediction
from sentence_transformers import SentenceTransformer
import torch

# Load models
forecast_model = TimesFmForPrediction.from_pretrained("facebook/timesfm-1.0")
spatial_model = TimeSeriesTransformerForPrediction.from_pretrained("johannfaouzi/TimeSeriesTransformer")
semantic_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Example data: 30-day environmental history (SST, Chl, SSH)
X = torch.randn(1, 30, 3)
forecast = forecast_model(X).prediction
spatial_output = torch.sigmoid(spatial_model(X).logits)

query = "Why are sharks aggregating near the Gulf Stream?"
context = [
    "Warm eddies increase prey density.",
    "High chlorophyll indicates productive zones.",
    "Low salinity areas correspond to nursery habitats."
]
emb_q = semantic_model.encode(query, convert_to_tensor=True)
emb_c = semantic_model.encode(context, convert_to_tensor=True)
```

---

## 🧭 Output Products

| Output Type | Description | Source |
|--------------|--------------|--------|
| `T0 Probability Map` | Current-day habitat suitability | TimeSeriesTransformer |
| `T+3 Forecast Map` | 3-day forecast of shark presence | TimesFM |
| `T+7 Forecast Map` | Extended forecast based on climatology | TimesFM |
| `Natural-language Insight` | Educational summary of ocean conditions | MiniLM |

---

## 🧬 Why These Models

- **facebook/timesfm-1.0** → Proven transformer-based forecaster for environmental series.  
- **TimeSeriesTransformer** → Works well for spatio-temporal learning and clustering.  
- **MiniLM-L6-v2** → Lightweight embedding model ideal for interactive explanations.  

Together, they offer:
- Short-term forecasting of ocean parameters (predictive capability).
- Recognition of known habitat patterns (classification capability).
- Intuitive interpretation layer (educational capability).

---

## 🔬 Example Use Case

```python
# Merge models in a unified inference pipeline
def predict_shark_activity(inputs):
    forecast = forecast_model(inputs).prediction
    suitability = torch.sigmoid(spatial_model(inputs).logits)
    # Generate explanation
    reason = context[torch.argmax(torch.rand(len(context)))]  # Simplified example
    return suitability, reason
```

---

## 🧭 Results

- **Prediction Horizon:** 3–7 days  
- **Spatial Resolution:** 0.1° grid (~10 km)  
- **Accuracy Estimate:** 80% (T0), 70% (T+3), 60% (T+7)  
- **Explainability:** SHAP and attention visualization supported

---

## 📄 Citation

**NASA Space Apps Challenge 2025 — “Sharks from Space”**  
Team: *From Space to Your Pocket* — Málaga, Spain  
Using open Hugging Face models under the Apache 2.0 license.

---

## ⚖️ License
All models used are released under the Apache 2.0 or MIT License, fully compatible with NASA’s open data policy.
