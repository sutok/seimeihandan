# 出力設定

# フロントエンド関連
output "frontend_bucket_name" {
  description = "フロントエンド用Cloud Storageバケット名"
  value       = google_storage_bucket.frontend_bucket.name
}

output "frontend_bucket_url" {
  description = "フロントエンド用Cloud StorageバケットURL"
  value       = "gs://${google_storage_bucket.frontend_bucket.name}"
}

output "frontend_domain" {
  description = "カスタムドメイン"
  value       = var.domain_name
}

output "frontend_ip_address" {
  description = "グローバルIPアドレス"
  value       = google_compute_global_address.frontend_ip.address
}

# Load Balancer関連
output "load_balancer_ip" {
  description = "Load BalancerのIPアドレス"
  value       = google_compute_global_address.frontend_ip.address
}

output "ssl_certificate_status" {
  description = "SSL証明書のステータス"
  value       = google_compute_managed_ssl_certificate.frontend_ssl.managed[0]
}

# Cloud Functions関連
output "cloud_function_name" {
  description = "Cloud Function名"
  value       = google_cloudfunctions2_function.seimei_handan_function.name
}

output "cloud_function_url" {
  description = "Cloud Function URL"
  value       = google_cloudfunctions2_function.seimei_handan_function.service_config[0].uri
}

output "cloud_function_trigger_url" {
  description = "Cloud Function トリガーURL"
  value       = "https://${var.region}-${var.project_id}.cloudfunctions.net/${var.app_name}"
}

# サービスアカウント関連
output "function_service_account_email" {
  description = "Cloud Functions用サービスアカウント"
  value       = google_service_account.function_service_account.email
}

# バックアップバケット
output "backup_bucket_name" {
  description = "バックアップ用バケット名"
  value       = google_storage_bucket.backup_bucket.name
}

# DNS設定情報
output "dns_instructions" {
  description = "DNS設定手順"
  value = <<-EOT
  DNS設定:
  
  shinyudo.comのDNS管理画面で以下のレコードを追加してください：
  
  Name: seimei
  Type: A
  Value: ${google_compute_global_address.frontend_ip.address}
  TTL: 300
  
  設定後、以下のコマンドで確認:
  nslookup seimei.shinyudo.com
  curl -I https://seimei.shinyudo.com
  EOT
}

# プロジェクト情報
output "project_id" {
  description = "GCPプロジェクトID"
  value       = var.project_id
}

output "region" {
  description = "使用リージョン"
  value       = var.region
}

# デプロイ後の確認URL
output "verification_urls" {
  description = "デプロイ後の確認URL"
  value = {
    frontend_storage = "https://storage.googleapis.com/${google_storage_bucket.frontend_bucket.name}/index.html"
    custom_domain    = "https://${var.domain_name}"
    function_api     = google_cloudfunctions2_function.seimei_handan_function.service_config[0].uri
  }
}