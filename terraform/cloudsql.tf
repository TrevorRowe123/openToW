# 1. Enable Required APIs
resource "google_project_service" "sqladmin" {
  project            = var.project_id
  service            = "sqladmin.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "servicenetworking" {
  project            = var.project_id
  service            = "servicenetworking.googleapis.com"
  disable_on_destroy = false
}

# 2. Set up Private IP for Cloud SQL (VPC Peering)
resource "google_compute_global_address" "private_ip_address" {
  name          = "opentow-private-ip"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.vpc.id
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.vpc.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
  depends_on              = [google_project_service.servicenetworking]
}

# 3. Generate a secure random password
resource "random_password" "db_password" {
  length           = 16
  special          = false
  override_special = "_%@"
}

# 4. Create the Cloud SQL Instance
resource "google_sql_database_instance" "instance" {
  name             = "opentow-postgres-db"
  region           = var.region
  database_version = "POSTGRES_15"

  # Keep false for easy cleanup during testing, switch to true for production!
  deletion_protection = false

  depends_on = [google_service_networking_connection.private_vpc_connection, google_project_service.sqladmin]

  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.vpc.id
    }
  }
}

# 5. Create Database and User
resource "google_sql_database" "database" {
  name     = "opentowdb"
  instance = google_sql_database_instance.instance.name
}

resource "google_sql_user" "user" {
  name     = "opentow"
  instance = google_sql_database_instance.instance.name
  password = random_password.db_password.result
}