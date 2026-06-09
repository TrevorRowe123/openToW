# Enable CI/CD APIs
resource "google_project_service" "cloudbuild" {
  project            = var.project_id
  service            = "cloudbuild.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "clouddeploy" {
  project            = var.project_id
  service            = "clouddeploy.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "secretmanager" {
  project            = var.project_id
  service            = "secretmanager.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "developerconnect" {
  project            = var.project_id
  service            = "developerconnect.googleapis.com"
  disable_on_destroy = false
}

# Define the GKE cluster as a deployment target
resource "google_clouddeploy_target" "gke_target" {
  location = var.region
  name     = "opentow-gke"

  gke {
    cluster = google_container_cluster.primary.id
  }
  depends_on = [google_project_service.clouddeploy]
}

# Get project info to dynamically find the Cloud Build service account
data "google_project" "project" {
  project_id = var.project_id
}

# Grant the Compute Engine SA permission to create Cloud Deploy releases
resource "google_project_iam_member" "cloudbuild_deployer" {
  project = var.project_id
  role    = "roles/clouddeploy.releaser"
  member  = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
  depends_on = [google_project_service.cloudbuild]
}

# Grant the Compute Engine SA permission to read tokens from Developer Connect
resource "google_project_iam_member" "developerconnect_read_token" {
  project = var.project_id
  role    = "roles/developerconnect.readTokenAccessor"
  member  = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
  depends_on = [google_project_service.developerconnect]
}

# Grant the Compute Engine SA permission to access Secret Manager (Required for 2nd Gen Repos)
resource "google_project_iam_member" "cloudbuild_secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
  depends_on = [google_project_service.secretmanager]
}

# Grant the Compute Engine SA permission to actually execute Cloud Build jobs
resource "google_project_iam_member" "cloudbuild_builder" {
  project = var.project_id
  role    = "roles/cloudbuild.builds.builder"
  member  = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
  depends_on = [google_project_service.cloudbuild]
}

# Grant the Compute Engine SA permission to act as the service account needed for the deployment
resource "google_project_iam_member" "cloudbuild_sa_user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
  depends_on = [google_project_service.cloudbuild]
}

# Grant the Compute Engine SA permission to write logs (Required to create the trigger)
resource "google_project_iam_member" "cloudbuild_logs" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
  depends_on = [google_project_service.cloudbuild]
}

# Grant the Compute Engine SA permission to push Docker images to Artifact Registry
resource "google_project_iam_member" "cloudbuild_artifact_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
  depends_on = [google_project_service.cloudbuild]
}

# Define the Delivery Pipeline
resource "google_clouddeploy_delivery_pipeline" "pipeline" {
  location = var.region
  name     = "opentow-pipeline"
  serial_pipeline {
    stages {
      target_id = google_clouddeploy_target.gke_target.name
    }
  }
  depends_on = [google_project_service.clouddeploy]
}