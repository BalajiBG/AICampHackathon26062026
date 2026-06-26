@echo off
REM ============================================================
REM GARUDA AI - GCP Cloud Run Deployment (Windows)
REM Project: aicamp26062026
REM Region: us-central1
REM ============================================================

SET PROJECT_ID=aicamp26062026
SET REGION=us-central1
SET SERVICE_NAME=garuda-ai-crime-platform

echo.
echo ===== GARUDA AI - Cloud Deployment =====
echo Project: %PROJECT_ID%
echo Region: %REGION%
echo.

REM Set project
echo [1/4] Setting GCP project...
gcloud config set project %PROJECT_ID%

REM Enable APIs
echo [2/4] Enabling required APIs...
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com aiplatform.googleapis.com --quiet

REM Deploy
echo [3/4] Building and deploying to Cloud Run...
gcloud run deploy %SERVICE_NAME% --source . --region %REGION% --allow-unauthenticated --set-env-vars "GCP_PROJECT=%PROJECT_ID%,GCP_LOCATION=%REGION%" --memory 2Gi --cpu 2 --timeout 300 --min-instances 0 --max-instances 3 --quiet

REM Get URL
echo [4/4] Fetching service URL...
echo.
echo ===== DEPLOYMENT COMPLETE =====
gcloud run services describe %SERVICE_NAME% --region %REGION% --format "value(status.url)"
echo.
echo Next: Ensure Cloud Run service account has 'Vertex AI User' role.
echo Run: gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" --role="roles/aiplatform.user"
pause
