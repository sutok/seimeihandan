# IAM設定

# Cloud Functions用サービスアカウント
resource "google_service_account" "function_service_account" {
  account_id   = "${var.app_name}-function-sa"
  display_name = "Service Account for ${var.app_name} Cloud Function"
  description  = "姓名判断アプリのCloud Functions用サービスアカウント"
}

# Cloud Functions実行に必要な権限
resource "google_project_iam_member" "function_invoker" {
  project = var.project_id
  role    = "roles/cloudfunctions.invoker"
  member  = "serviceAccount:${google_service_account.function_service_account.email}"
}

# ストレージアクセス権限（ログ等）
resource "google_project_iam_member" "function_storage_admin" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.function_service_account.email}"
}

# ログ書き込み権限
resource "google_project_iam_member" "function_logging" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.function_service_account.email}"
}

# Cloud Functions Developer権限（デプロイ用）
resource "google_project_iam_member" "function_developer" {
  project = var.project_id
  role    = "roles/cloudfunctions.developer"
  member  = "serviceAccount:${google_service_account.function_service_account.email}"
}

# 必要なAPIの有効化
resource "google_project_service" "required_apis" {
  for_each = toset([
    "cloudfunctions.googleapis.com",
    "cloudbuild.googleapis.com",
    "storage.googleapis.com",
    "compute.googleapis.com",
    "certificatemanager.googleapis.com",
    "dns.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com",
    "apigateway.googleapis.com",
    "servicemanagement.googleapis.com",
    "servicecontrol.googleapis.com",
    "storage-component.googleapis.com",
    "endpoints.googleapis.com"
  ])

  project = var.project_id
  service = each.value

  disable_dependent_services = false
  disable_on_destroy         = false
}

# デプロイ用サービスアカウントキー（オプション）
resource "google_service_account_key" "function_key" {
  service_account_id = google_service_account.function_service_account.name
  public_key_type    = "TYPE_X509_PEM_FILE"
}

# セキュリティ強化：Cloud Functions用のカスタムロール
resource "google_project_iam_custom_role" "seimei_handan_function_role" {
  role_id     = "${replace(var.app_name, "-", "_")}_function_role"
  title       = "${var.app_name} Function Custom Role"
  description = "姓名判断アプリ専用のカスタムロール"

  permissions = [
    "logging.logEntries.create",
    "storage.objects.get",
    "storage.objects.list",
    "storage.objects.create",
    "cloudsql.instances.connect"
  ]
}

# カスタムロールをサービスアカウントに付与
resource "google_project_iam_member" "function_custom_role" {
  project = var.project_id
  role    = google_project_iam_custom_role.seimei_handan_function_role.name
  member  = "serviceAccount:${google_service_account.function_service_account.email}"
}