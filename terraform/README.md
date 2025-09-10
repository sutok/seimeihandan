# 姓名判断アプリ - Terraform実行手順書

## 📋 概要

このTerraformファイルセットは、姓名判断アプリの全GCP設定を管理します：

- **Cloud Functions**: バックエンドAPI
- **Cloud Storage**: フロントエンドホスティング
- **Load Balancer**: HTTPS + カスタムドメイン（seimei.shinyudo.com）
- **SSL証明書**: Google-managed証明書
- **IAM**: セキュリティ設定

## 🚀 実行手順

### 1. 事前準備

```bash
# Terraformのインストール確認
terraform --version

# GCPアカウント認証
gcloud auth application-default login
gcloud config set project ai-tools-471505

# 必要なAPIの有効化（手動で実行）
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable compute.googleapis.com
```

### 2. フロントエンドビルド

```bash
cd ../frontend
npm run build
# buildディレクトリが生成されることを確認
ls -la build/
```

### 3. Terraform実行

```bash
# Terraformディレクトリに移動
cd terraform

# 初期化
terraform init

# プラン確認
terraform plan

# 適用（実際のデプロイ）
terraform apply
# "yes" を入力して実行
```

### 4. DNS設定

Terraform実行後に表示される情報をもとに、shinyudo.comのDNS管理画面で設定：

```
Name: seimei
Type: A
Value: [表示されたIPアドレス]
TTL: 300
```

### 5. 確認

```bash
# DNS伝播確認
nslookup seimei.shinyudo.com

# HTTPS接続確認
curl -I https://seimei.shinyudo.com

# SSL証明書確認
terraform output ssl_certificate_status
```

## 📁 ファイル構成

```
terraform/
├── main.tf              # プロバイダー設定
├── variables.tf         # 変数定義
├── cloud_functions.tf   # Cloud Functions設定
├── cloud_storage.tf     # Cloud Storage設定
├── load_balancer.tf     # Load Balancer + SSL設定
├── iam.tf              # IAM設定
├── outputs.tf          # 出力設定
└── README.md           # この手順書
```

## 🔧 カスタマイズ

### 変数の変更

`terraform.tfvars`ファイルを作成して変数をオーバーライド：

```hcl
# terraform.tfvars
project_id = "your-project-id"
domain_name = "your-domain.com"
region = "asia-northeast1"
```

### ドメイン変更

```bash
# 新しいドメインで再デプロイ
terraform apply -var="domain_name=new-domain.com"
```

## 🛠️ トラブルシューティング

### SSL証明書の問題

```bash
# 証明書ステータス確認
terraform output ssl_certificate_status

# DNS設定が正しいか確認
nslookup your-domain.com
```

### Cloud Functions デプロイ失敗

```bash
# ソースコードの確認
ls -la ../functions/

# 手動でZIPファイル確認
cd ../functions && zip -r function.zip . -x "__pycache__/*" "*.pyc"
```

### バケットアクセス権限の問題

```bash
# バケット権限確認
gsutil iam get gs://seimei-handan-frontend-storage

# 手動で権限付与
gsutil iam ch allUsers:objectViewer gs://seimei-handan-frontend-storage
```

## 📊 リソース管理

### コスト確認

```bash
# 現在のリソース状況
terraform show

# リソース削除（開発時のみ）
terraform destroy
```

### バックアップ

```bash
# Terraformステート をバックアップ
cp terraform.tfstate terraform.tfstate.backup
```

## 🔒 セキュリティ注意事項

1. **サービスアカウントキー**: 絶対にGitリポジトリにコミットしない
2. **terraform.tfstate**: 秘匿情報が含まれるため適切に管理
3. **IAM権限**: 最小権限の原則を遵守

## 📝 更新履歴

- 2025-09-10: 初版作成
- カスタムドメイン（seimei.shinyudo.com）対応
- SSL証明書自動管理対応
- セキュリティ強化（Phase A対策組み込み）