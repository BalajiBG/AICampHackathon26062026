#!/bin/bash
# ============================================================
# GARUDA AI - One-Click GCP Cloud Run Deployment Script
# Project: aicamp26062026
# Region: us-central1
# ============================================================

set -e

PROJECT_ID="aicamp26062026"
REGION="us-central1"
SERVICE_NAME="garuda-ai-crime-platform"

echo "🛡️ GARUDA AI - Deploying to Google Cloud Run"
echo "=============================================="
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Service: $SERVICE_NAME"
echo ""

# Step 1: Set project
echo "📌 Setting GCP project..."
gcloud config set project $PROJECT_ID

# Step 2: Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    aiplatform.googleapis.com \
    --quiet

# Step 3: Deploy directly from source (Cloud Build + Cloud Run)
echo "🚀 Building and deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --source . \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars "GCP_PROJECT=$PROJECT_ID,GCP_LOCATION=$REGION" \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --min-instances 0 \
    --max-instances 3 \
    --quiet

# Step 4: Get the service URL
echo ""
echo "=============================================="
echo "✅ DEPLOYMENT SUCCESSFUL!"
echo "=============================================="
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')
echo "🌐 Live URL: $SERVICE_URL"
echo ""
echo "📋 Post-deployment checklist:"
echo "   1. Ensure service account has 'Vertex AI User' role"
echo "   2. Test the chatbot with sample queries"
echo "   3. Verify voice input works in Chrome browser"
echo ""
echo "🔐 To add Vertex AI permissions:"
echo "   gcloud projects add-iam-policy-binding $PROJECT_ID \\"
echo "     --member='serviceAccount:$(gcloud run services describe $SERVICE_NAME --region $REGION --format=\"value(spec.template.spec.serviceAccountName)\")' \\"
echo "     --role='roles/aiplatform.user'"
