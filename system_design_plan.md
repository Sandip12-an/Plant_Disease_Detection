# Plant Disease Detection — System Design Plan

## 1. High-Level Architecture

```
┌─────────────┐      ┌──────────────┐      ┌──────────────────┐
│  Client App  │─────▶│   API Layer   │─────▶│  Inference Service │
│ (Web/Mobile) │◀─────│ (FastAPI/Flask)│◀─────│   (Model Server)   │
└─────────────┘      └──────┬───────┘      └──────────┬────────┘
                             │                          │
                      ┌──────▼───────┐          ┌───────▼────────┐
                      │   Database    │          │  Model Registry │
                      │ (scan history)│          │ (versioned .h5/  │
                      └──────────────┘          │  .pt weights)    │
                                                  └────────────────┘
```

---

## 2. Components

1. **Client (Frontend)**
   - Web app (React) or mobile app (Flutter/React Native)
   - Camera/upload UI, displays results and history

2. **API Gateway / Backend**
   - FastAPI or Flask REST API
   - Handles auth, request validation, routing
   - Exposes endpoints: `/predict`, `/history`, `/disease-info`

3. **Preprocessing Pipeline**
   - Image resizing (e.g., 224x224)
   - Normalization, format conversion
   - Input validation (file type, size limits)

4. **Inference Engine**
   - Loads trained CNN model
   - Runs prediction, returns class + confidence score
   - Supports batch and single-image inference

5. **Model Registry**
   - Stores versions of trained models
   - Enables rollback and A/B testing between model versions

6. **Database**
   - PostgreSQL or MongoDB
   - Stores user scan history, disease metadata, treatment info

7. **Object Storage**
   - AWS S3 or local filesystem
   - Stores uploaded images (for history/retraining)

8. **Monitoring**
   - Logs predictions and confidence distributions
   - Drift detection (flagging when model performance degrades on new data)

---

## 3. Data Flow

1. User uploads/captures leaf image on client
2. Image sent to API layer via `/predict` endpoint
3. API forwards image to preprocessing pipeline
4. Preprocessed image passed to inference engine
5. Model returns prediction (disease class + confidence)
6. API layer:
   - Fetches disease info/treatment from database
   - Logs scan (image + result) to database/storage
   - Returns combined response to client
7. Client displays diagnosis, confidence, and remedy suggestions

---

## 4. API Design (Example)

### `POST /predict`
**Request:** multipart/form-data image file

**Response:**
```json
{
  "disease": "Tomato___Late_blight",
  "confidence": 0.94,
  "healthy": false,
  "treatment": "Apply copper-based fungicide, remove affected leaves...",
  "scan_id": "abc123"
}
```

### `GET /history`
Returns paginated list of past scans for a user.

### `GET /disease-info/{disease_id}`
Returns detailed symptoms, causes, and treatment for a disease.

---

## 5. Database Schema (Example)

**users**
| Field | Type |
|---|---|
| id | UUID |
| name | String |
| email | String |
| created_at | Timestamp |

**scans**
| Field | Type |
|---|---|
| id | UUID |
| user_id | FK → users.id |
| image_url | String |
| disease_id | FK → diseases.id |
| confidence | Float |
| created_at | Timestamp |

**diseases**
| Field | Type |
|---|---|
| id | UUID |
| crop | String |
| name | String |
| symptoms | Text |
| treatment | Text |
| prevention | Text |

---

## 6. Model Serving Design

- Model exported to ONNX or TFLite for portability
- Served via TorchServe/TensorFlow Serving or embedded directly in FastAPI backend
- Versioned in model registry (e.g., simple S3 folder structure or MLflow)
- Health-check endpoint (`/health`) for the inference service
- Horizontal scaling: multiple inference service replicas behind a load balancer for concurrent requests

---

## 7. Scalability & Reliability Considerations

- **Caching:** Cache disease-info lookups (rarely change) to reduce DB load
- **Async processing:** Use async endpoints (FastAPI supports this natively) for I/O-bound operations
- **Load balancing:** Multiple backend/inference replicas behind a load balancer (e.g., NGINX, AWS ALB)
- **Rate limiting:** Prevent abuse of the `/predict` endpoint
- **Graceful degradation:** Return cached/generic advice if model service is temporarily down
- **CDN:** Serve static frontend assets via CDN for faster load times

---

## 8. Security Considerations

- Validate and sanitize all image uploads (file type, size limits, malware scanning if needed)
- Authentication (JWT/OAuth) for user-specific history features
- HTTPS everywhere
- Rate limiting and request throttling to prevent abuse
- Secure storage of images (signed URLs for access, not public buckets)

---

## 9. Deployment Architecture

- **Containerization:** Docker images for backend, inference service, and frontend
- **Orchestration:** Docker Compose (small scale) or Kubernetes (larger scale)
- **CI/CD:** GitHub Actions/GitLab CI for automated testing and deployment
- **Environments:** Separate dev/staging/production environments
- **Monitoring stack:** Prometheus + Grafana for metrics, Sentry for error tracking, centralized logging (ELK/CloudWatch)

---

## 10. Future Extensions

- Add object detection (YOLO) to localize disease regions on the leaf
- Grad-CAM visualization for explainability
- On-device (edge) inference for offline use in low-connectivity areas
- Active learning pipeline: flagged/low-confidence predictions reviewed and fed back into retraining
