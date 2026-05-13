# Model Folder

Place the trained model files here.

Expected final files:

```text
backend/models/best_model.keras
backend/models/labels.json
```

Preferred model format:

```text
best_model.keras
```

Acceptable fallback:

```text
skindisnet_efficientnetv2b3.keras
skin_model.keras
skin_model.h5
```

The backend will use dummy prediction until a real model file is placed here and TensorFlow is installed.
