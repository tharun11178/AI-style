# Trained Models

This folder stores model artifacts used by the backend ML helpers.

Current files:

- `face_shape_model.json`: local face shape classifier configuration.
- `style_rules.json`: recommendation rules, palettes, accessories, and face-shape styling data.

You can later add real exported files such as `.onnx`, `.pkl`, `.joblib`, `.h5`, or `.tflite`. The `/api/admin/ml-assets` endpoint will include them automatically.
