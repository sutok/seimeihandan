# Terraform設定

このディレクトリには、姓名判断アプリのGCPインフラストラクチャをTerraformで管理するための設定ファイルが含まれています。

## 設定手順

### 1. 必要なツールのインストール

```bash
# Terraformのインストール
brew install terraform

# Google Cloud CLIのインストール
brew install --cask google-cloud-sdk
```

### 2. GCPプロジェクトの設定

```bash
# GCPにログイン
gcloud auth login

# アプリケーションデフォルト認証を設定
gcloud auth application-default login

# プロジェクトIDを設定（例：ai-tools-471505）
gcloud config set project YOUR_PROJECT_ID
```

### 3. Terraform設定ファイルの作成

`terraform.tfvars.example`をコピーして`terraform.tfvars`ファイルを作成し、プロジェクト固有の値を設定してください。

```bash
cp terraform.tfvars.example terraform.tfvars
```

`terraform.tfvars`ファイルを編集して、以下の値を設定：

```hcl
# GCPプロジェクト設定
project_id = "your-gcp-project-id"

# アプリケーション設定
app_name = "seimei-handan"

# ドメイン設定（必要に応じて変更）
domain_name = "seimei.shinyudo.com"

# ロケーション設定（必要に応じて変更）
region = "asia-northeast1"
location = "asia-northeast1"

# Cloud Functions設定（必要に応じて変更）
function_name = "seimei-handan-api"
```

### 4. Terraformの初期化と実行

```bash
# Terraformの初期化
terraform init

# プランの確認
terraform plan

# インフラストラクチャの適用
terraform apply
```

## 注意事項

- `terraform.tfvars`ファイルはGitに含まれません（`.gitignore`で除外）
- プロジェクト固有の情報は`terraform.tfvars`で設定し、デフォルト値は`variables.tf`で定義しています
- 初回デプロイ時は、必要なGCP APIが自動的に有効化されます
- SSL証明書は Google 管理の証明書が自動的に作成されます

## ファイル構成

- `variables.tf` - 変数定義
- `terraform.tfvars.example` - 設定例ファイル
- `terraform.tfvars` - プロジェクト固有設定（作成が必要）
- `.gitignore` - Git除外ファイル設定

## トラブルシューティング

### API有効化エラー
必要なGCP APIが有効化されていない場合は、自動的に有効化されるまで少し時間がかかる場合があります。

### バケット名の競合
Cloud Storageバケット名はランダムサフィックスが自動付加されるため、通常は競合しません。

### タイムアウトエラー
大規模なリソース作成時にタイムアウトが発生する場合は、再度`terraform apply`を実行してください。