# GCP プロジェクト変数
variable "project_id" {
  description = "GCPプロジェクトID"
  type        = string
  # デフォルト値を削除して、terraform.tfvarsで設定するようにする
}

variable "region" {
  description = "デプロイするリージョン"
  type        = string
  default     = "asia-northeast1"
}

variable "location" {
  description = "リソースのロケーション"
  type        = string
  default     = "asia-northeast1"
}

# アプリケーション変数
variable "app_name" {
  description = "アプリケーション名"
  type        = string
  default     = "seimei-handan"
}

variable "function_name" {
  description = "Cloud Functionの名前"
  type        = string
  default     = "seimei-handan-api"
}

# ドメイン変数
variable "domain_name" {
  description = "カスタムドメイン名"
  type        = string
  default     = "seimei.shinyudo.com"
}