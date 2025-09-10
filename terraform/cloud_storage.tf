# Cloud Storage 設定

# フロントエンド用バケット
resource "google_storage_bucket" "frontend_bucket" {
  name                        = "${var.app_name}-frontend-${random_id.frontend_suffix.hex}"
  location                    = var.region
  force_destroy               = false
  uniform_bucket_level_access = true

  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }

  # CORS設定（カスタムドメイン対応）
  cors {
    origin          = ["https://${var.domain_name}", "http://localhost:3000"]
    method          = ["GET", "HEAD", "OPTIONS"]
    response_header = ["Content-Type"]
    max_age_seconds = 3600
  }

  # 静的ファイル用の設定
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}

# フロントエンドバケットを公開設定
resource "google_storage_bucket_iam_member" "frontend_public_access" {
  bucket = google_storage_bucket.frontend_bucket.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"

  depends_on = [google_storage_bucket.frontend_bucket]
}

# デプロイ用のローカル実行リソース（オプション）
# フロントエンドファイルのアップロード
resource "null_resource" "upload_frontend_files" {
  # フロントエンドビルドファイルの変更を検知
  triggers = {
    build_hash = filemd5("${var.frontend_build_dir}/index.html")
  }

  provisioner "local-exec" {
    command = <<-EOT
      if [ -d "${var.frontend_build_dir}" ]; then
        gsutil -m rsync -r -d ${var.frontend_build_dir}/ gs://${google_storage_bucket.frontend_bucket.name}/
        gsutil web set -m index.html -e 404.html gs://${google_storage_bucket.frontend_bucket.name}
      else
        echo "Frontend build directory not found: ${var.frontend_build_dir}"
        exit 1
      fi
    EOT
  }

  depends_on = [
    google_storage_bucket.frontend_bucket,
    google_storage_bucket_iam_member.frontend_public_access
  ]
}

# バックアップ用バケット（オプション）
resource "google_storage_bucket" "backup_bucket" {
  name                        = "${var.app_name}-backup-${random_id.backup_suffix.hex}"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true

  # バックアップファイルの自動削除設定
  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type = "Delete"
    }
  }

  # バージョニング有効
  versioning {
    enabled = true
  }
}

resource "random_id" "backup_suffix" {
  byte_length = 4
}

# フロントエンドバケット用ランダムサフィックス
resource "random_id" "frontend_suffix" {
  byte_length = 4
}