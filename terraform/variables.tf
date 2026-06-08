variable "project_id" {
  description = "Your Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "The GCP Region to deploy resources into"
  type        = string
  default     = "us-central1"
}