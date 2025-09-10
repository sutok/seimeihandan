# 変数定義

variable "project_id" {
  description = "GCPプロジェクトID"
  type        = string
  default     = "ai-tools-471505"
}

variable "region" {
  description = "GCPリージョン"
  type        = string
  default     = "asia-northeast1"
}

variable "domain_name" {
  description = "カスタムドメイン名"
  type        = string
  default     = "seimei.shinyudo.com"
}

variable "app_name" {
  description = "アプリケーション名"
  type        = string
  default     = "seimei-handan"
}

variable "function_source_dir" {
  description = "Cloud Functions ソースコードディレクトリ"
  type        = string
  default     = "../functions"
}

variable "frontend_build_dir" {
  description = "フロントエンド ビルドディレクトリ"
  type        = string
  default     = "../frontend/build"
}