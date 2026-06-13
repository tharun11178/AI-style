# AI Personal Style & Wellness Advisor

Working full-stack MVP based on:

- `AI_Style_Wellness_Full_Master_Guide.pdf`
- `Final_Combined_AI_Style_Wellness_Master_Guide.pdf`

## What Works

- React dashboard for users and admins
- Register, login, logout, and token-based sessions
- Face photo upload with deterministic MVP analysis
- Personalized hairstyle, outfit, glasses, color palette, and wellness recommendations
- SQLite recommendation history
- Admin analytics
- Profile and feedback screens
- Full guide and planning guide PDFs embedded in the app
- Guide-style `ml_models/` structure for later OpenCV/MediaPipe upgrades

## Implemented API

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/users/profile
PUT  /api/users/profile
POST /api/analyze-face
GET  /api/recommend/hairstyle
GET  /api/recommend/outfits
GET  /api/recommend/colors
GET  /api/history
POST /api/feedback
GET  /api/admin/users
GET  /api/admin/analytics
```

## Demo Accounts

```text
User:  demo@example.com / demo123
Admin: admin@example.com / admin123
```

## Backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.\run_backend.cmd
```

API docs:

```text
http://127.0.0.1:8002/docs
```

## Backend File Structure

```text
backend/
  app/
    routers/
      auth.py
      users.py
      analysis.py
      recommendations.py
      admin.py
    models/
      user_model.py
      analysis_model.py
      recommendation_model.py
      feedback_model.py
    schemas/
      user_schema.py
      auth_schema.py
      recommendation_schema.py
    services/
      auth_service.py
      face_service.py
      recommendation_service.py
      history_service.py
    utils/
      jwt_handler.py
      image_utils.py
      file_handler.py
      response_handler.py
    database.py
    config.py
    main.py
  ml_models/
    datasets/
    trained_models/
    face_detection.py
    landmark_detection.py
    face_shape_classifier.py
    recommendation_engine.py
    outfit_matcher.py
    hairstyle_matcher.py
    color_analysis.py
```

## Frontend

```powershell
cd frontend
npm.cmd install
npm.cmd run build
.\run_frontend.cmd
```

App:

```text
http://127.0.0.1:5175
```

## Frontend File Structure

```text
frontend/
  public/
    logo.png
    favicon.ico
  src/
    components/
      Navbar.jsx
      Footer.jsx
      Sidebar.jsx
      Loader.jsx
      ImageUploader.jsx
      OutfitCard.jsx
      HairstyleCard.jsx
      ProtectedRoute.jsx
    pages/
      Home.jsx
      Login.jsx
      Register.jsx
      Dashboard.jsx
      UploadPhoto.jsx
      FaceAnalysis.jsx
      OutfitRecommendations.jsx
      HairstyleRecommendations.jsx
      ColorPalette.jsx
      History.jsx
      Profile.jsx
    services/
      api.js
      authService.js
      analysisService.js
      recommendationService.js
    App.js
    main.jsx
    index.css
```

## Next ML Upgrade

The current analyzer is a working local MVP that produces deterministic recommendations from the uploaded image and user preferences. Replace the analyzer in `backend/app/main.py` with OpenCV/MediaPipe landmark extraction and a trained face-shape classifier when model files and datasets are ready.
