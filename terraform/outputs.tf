output "artifact_registry_url" {
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.repo.repository_id}"
  description = "The base URL for your Docker images"
}

output "cluster_name" {
  value       = google_container_cluster.primary.name
  description = "The name of the GKE cluster"
}