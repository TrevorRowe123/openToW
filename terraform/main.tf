terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.80"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "artifact_registry" {
  project            = var.project_id
  service            = "artifactregistry.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "compute" {
  project            = var.project_id
  service            = "compute.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "container" {
  project            = var.project_id
  service            = "container.googleapis.com"
  disable_on_destroy = false
}

# 1. Artifact Registry (To host your Docker image)
resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = "opentow-repo"
  description   = "Docker repository for openToW"
  format        = "DOCKER"

  depends_on = [google_project_service.artifact_registry]
}

# Fetch the default compute service account used by GKE
data "google_compute_default_service_account" "default" {
  project    = var.project_id
  depends_on = [google_project_service.compute]
}

# Grant GKE nodes read access to the Artifact Registry repository
resource "google_artifact_registry_repository_iam_member" "gke_reader" {
  project    = google_artifact_registry_repository.repo.project
  location   = google_artifact_registry_repository.repo.location
  repository = google_artifact_registry_repository.repo.name
  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:${data.google_compute_default_service_account.default.email}"
}

# 2. VPC Network
resource "google_compute_network" "vpc" {
  name                    = "opentow-vpc"
  auto_create_subnetworks = false

  depends_on = [google_project_service.compute]
}

resource "google_compute_subnetwork" "subnet" {
  name          = "opentow-subnet"
  region        = var.region
  network       = google_compute_network.vpc.name
  ip_cidr_range = "10.10.0.0/24"
  private_ip_google_access = true
}

# 3. GKE Cluster (Autopilot is recommended for simplicity and security)
resource "google_container_cluster" "primary" {
  name     = "opentow-cluster"
  location = var.region

  network    = google_compute_network.vpc.name
  subnetwork = google_compute_subnetwork.subnet.name

  # Enable Autopilot for fully managed nodes
  enable_autopilot = true

  depends_on = [google_project_service.container]
}