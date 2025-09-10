# Cloud Functions 設定

# Cloud Functions v2 (Cloud Run)
resource "google_cloudfunctions2_function" "seimei_handan_function" {
  name     = var.app_name
  location = var.region

  build_config {
    runtime     = "python39"
    entry_point = "seimei_handan"
    
    source {
      storage_source {
        bucket = google_storage_bucket.function_source_bucket.name
        object = google_storage_bucket_object.function_source.name
      }
    }
  }

  service_config {
    max_instance_count               = 100
    min_instance_count               = 0
    available_memory                 = "512M"
    available_cpu                    = "0.3333"
    timeout_seconds                  = 60
    max_instance_request_concurrency = 1
    
    environment_variables = {
      LOG_EXECUTION_ID = "true"
    }

    ingress_settings               = "ALLOW_ALL"
    all_traffic_on_latest_revision = true
    
    service_account_email = google_service_account.function_service_account.email
  }

  depends_on = [
    google_storage_bucket_object.function_source,
    google_project_iam_member.function_invoker
  ]
}

# Cloud Function のソースコード用バケット
resource "google_storage_bucket" "function_source_bucket" {
  name                        = "${var.app_name}-function-source-${random_id.bucket_suffix.hex}"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 7
    }
    action {
      type = "Delete"
    }
  }
}

# ソースコード用ランダムサフィックス
resource "random_id" "bucket_suffix" {
  byte_length = 8
}

# ソースコードのZIPファイル
data "archive_file" "function_source" {
  type        = "zip"
  source_dir  = var.function_source_dir
  output_path = "/tmp/${var.app_name}-source.zip"
  excludes = [
    "__pycache__",
    "*.pyc",
    ".git",
    ".venv"
  ]
}

# ソースコードをバケットにアップロード
resource "google_storage_bucket_object" "function_source" {
  name   = "function-source-${data.archive_file.function_source.output_md5}.zip"
  bucket = google_storage_bucket.function_source_bucket.name
  source = data.archive_file.function_source.output_path

  depends_on = [data.archive_file.function_source]
}

# Function Invoker権限
resource "google_cloudfunctions2_function_iam_member" "function_invoker" {
  project        = var.project_id
  location       = var.region
  cloud_function = google_cloudfunctions2_function.seimei_handan_function.name
  role           = "roles/cloudfunctions.invoker"
  member         = "allUsers"
}