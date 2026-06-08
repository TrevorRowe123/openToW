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

# Define the GKE cluster as a deployment target
resource "google_clouddeploy_target" "gke_target" {
  location = var.region
  name     = "opentow-gke"

  gke {
    cluster = google_container_cluster.primary.id
  }
  depends_on = [google_project_service.clouddeploy]
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