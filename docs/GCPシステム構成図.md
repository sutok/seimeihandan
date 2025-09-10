# 姓名判断アプリ - GCPシステム構成図

## システムアーキテクチャ概要

```mermaid
graph TB
    subgraph "User Layer"
        U[👤 ユーザー<br/>Web Browser]
        M[📱 モバイルデバイス]
    end

    subgraph "CDN Layer"
        CDN[🌐 Cloud CDN<br/>Static Content Delivery]
    end

    subgraph "Frontend Layer"
        FB[🔥 Firebase Hosting<br/>React SPA<br/>- 姓名入力フォーム<br/>- 結果表示UI<br/>- レスポンシブデザイン]
    end

    subgraph "API Gateway Layer"
        CF[⚡ Cloud Functions<br/>seimei-handan<br/>- HTTP Trigger<br/>- CORS対応<br/>- 自動スケーリング]
    end

    subgraph "Business Logic Layer"
        PY[🐍 Python Runtime<br/>- Flask Framework<br/>- jamdict統合<br/>- 五格計算エンジン]
    end

    subgraph "Data Layer"
        JD[📚 jamdict辞書<br/>13,108文字<br/>- 漢字画数データ<br/>- KanjiDic2準拠]
        GJ[📊 gogaku_judgment.json<br/>- 五格判定ルール<br/>- 運勢解説文<br/>- 1-81画対応]
        HS[🔤 hiragana_strokes.json<br/>- ひらがな画数<br/>- あ～ん対応]
    end

    subgraph "Monitoring & Security"
        CM[📊 Cloud Monitoring<br/>- パフォーマンス監視<br/>- エラートラッキング]
        CL[📋 Cloud Logging<br/>- アクセスログ<br/>- エラーログ]
        IAM[🔐 Cloud IAM<br/>- アクセス制御<br/>- セキュリティ管理]
    end

    %% User Flow
    U --> CDN
    M --> CDN
    CDN --> FB
    FB --> CF

    %% API Flow
    CF --> PY
    PY --> JD
    PY --> GJ
    PY --> HS

    %% Monitoring
    CF --> CM
    CF --> CL
    FB --> CM
    IAM --> CF
    IAM --> FB

    %% Styling
    classDef userLayer fill:#e1f5fe
    classDef frontend fill:#f3e5f5
    classDef backend fill:#e8f5e8
    classDef data fill:#fff3e0
    classDef monitoring fill:#fce4ec

    class U,M userLayer
    class CDN,FB frontend
    class CF,PY backend
    class JD,GJ,HS data
    class CM,CL,IAM monitoring
```

## 詳細コンポーネント仕様

### 1. Frontend Layer (Firebase Hosting)

```mermaid
graph LR
    subgraph "React Application"
        APP[App.js<br/>メインアプリケーション]
        FORM[姓名入力フォーム<br/>- バリデーション<br/>- リアルタイム検証]
        RESULT[結果表示コンポーネント<br/>- 五格表示<br/>- 運勢説明<br/>- レスポンシブレイアウト]
        API[APIクライアント<br/>- axios統合<br/>- エラーハンドリング]
    end

    APP --> FORM
    APP --> RESULT
    FORM --> API
    API --> RESULT

    classDef component fill:#e3f2fd
    class APP,FORM,RESULT,API component
```

### 2. Backend Layer (Cloud Functions)

```mermaid
graph TB
    subgraph "Cloud Functions Runtime"
        HTTP[HTTP Trigger<br/>POST /api/v1/analyze]
        MAIN[main.py<br/>seimei_handan function]
        INIT[initialize_dictionaries<br/>- jamdict初期化<br/>- JSONファイル読込]
        CALC[calculate_gogaku<br/>- 画数計算<br/>- 五格算出]
        CHAR[get_character_stroke_count<br/>- 文字画数取得<br/>- jamdict + ひらがな辞書]
        THREAD[get_thread_local_jamdict<br/>- Thread-Local Storage<br/>- SQLite安全性確保]
        JUDGE[get_overall_judgment<br/>- 総合判定算出<br/>- 重み付け評価]
        EMBED[Embedded Functions<br/>- get_embedded_gogaku_rules<br/>- get_embedded_hiragana_strokes]
    end

    HTTP --> MAIN
    MAIN --> INIT
    MAIN --> CALC
    CALC --> CHAR
    CHAR --> THREAD
    CALC --> JUDGE
    MAIN --> EMBED

    classDef function fill:#e8f5e8
    classDef helper fill:#f3e5f5
    class HTTP,MAIN,INIT,CALC function
    class CHAR,THREAD,JUDGE,EMBED helper
```

### 3. Data Flow Architecture

```mermaid
sequenceDiagram
    participant U as ユーザー
    participant F as Frontend
    participant C as Cloud Functions
    participant J as jamdict
    participant G as gogaku_judgment.json

    U->>F: 姓名入力
    F->>F: バリデーション
    F->>C: POST /api/v1/analyze
    C->>C: リクエスト検証
    
    loop 各文字について
        C->>J: 文字画数検索
        J-->>C: 画数返却
    end
    
    C->>C: 五格計算<br/>(天格・人格・地格・外格・総格)
    
    loop 各格について
        C->>G: 判定ルール参照
        G-->>C: 運勢・説明文返却
    end
    
    C->>C: 総合判定算出
    C-->>F: JSON レスポンス
    F->>F: 結果表示生成
    F-->>U: 診断結果表示
```

## インフラストラクチャ仕様

### スケーリング設定

```mermaid
graph TB
    subgraph "Auto Scaling Configuration"
        MIN[最小インスタンス数: 0]
        MAX[最大インスタンス数: 100]
        MEM[メモリ: 512MB]
        TIMEOUT[タイムアウト: 60秒]
        TRIGGER[トリガー: HTTP]
    end

    subgraph "Performance Metrics"
        RESP[平均応答時間: 60.69ms]
        THROUGHPUT[スループット: 1000 req/min]
        SUCCESS[成功率: 99.9%]
    end

    MIN --> MAX
    MAX --> MEM
    MEM --> TIMEOUT
    TIMEOUT --> TRIGGER

    classDef config fill:#fff3e0
    classDef metrics fill:#e8f5e8
    class MIN,MAX,MEM,TIMEOUT,TRIGGER config
    class RESP,THROUGHPUT,SUCCESS metrics
```

### セキュリティ設定

```mermaid
graph TB
    subgraph "Security Layers - Phase A実装済み"
        CORS[CORS設定<br/>- Allow-Origin: 制限あり<br/>- Content-Type許可<br/>- POST method許可]
        AUTH[認証設定<br/>- allow-unauthenticated<br/>- 一般アクセス可能]
        HTTPS[HTTPS強制<br/>- SSL/TLS暗号化<br/>- セキュア通信]
        ORIGIN[オリジン制限<br/>- storage.googleapis.com許可<br/>- localhost開発環境許可<br/>- 不正ドメインブロック]
        RATELIMIT[レート制限<br/>- 1分間10リクエスト<br/>- IP別制限管理<br/>- DoS攻撃防止]
        USERAGENT[User-Agent検証<br/>- bot/curl等ブロック<br/>- 自動化ツール防止<br/>- セキュリティログ記録]
    end

    CORS --> AUTH
    AUTH --> HTTPS
    HTTPS --> ORIGIN
    ORIGIN --> RATELIMIT
    RATELIMIT --> USERAGENT

    classDef security fill:#fce4ec
    classDef implemented fill:#c8e6c9
    class CORS,AUTH,HTTPS security
    class ORIGIN,RATELIMIT,USERAGENT implemented
```

## デプロイメント構成

### CI/CD Pipeline

```mermaid
graph LR
    subgraph "Development"
        DEV[ローカル開発<br/>- uv venv環境<br/>- 開発サーバー起動]
        TEST[統合テスト<br/>- API機能テスト<br/>- パフォーマンステスト]
    end

    subgraph "Build"
        BUILD_BE[Backend Build<br/>- requirements.txt<br/>- 依存関係解決]
        BUILD_FE[Frontend Build<br/>- npm run build<br/>- 静的ファイル生成]
    end

    subgraph "Deploy"
        DEPLOY_CF[Cloud Functions<br/>gcloud functions deploy]
        DEPLOY_FB[Firebase Hosting<br/>firebase deploy]
    end

    DEV --> TEST
    TEST --> BUILD_BE
    TEST --> BUILD_FE
    BUILD_BE --> DEPLOY_CF
    BUILD_FE --> DEPLOY_FB

    classDef dev fill:#e3f2fd
    classDef build fill:#fff3e0
    classDef deploy fill:#e8f5e8

    class DEV,TEST dev
    class BUILD_BE,BUILD_FE build
    class DEPLOY_CF,DEPLOY_FB deploy
```

## コスト最適化

### リソース使用量

```mermaid
pie title リソース使用量分布
    "Cloud Functions 実行時間" : 45
    "Firebase Hosting 転送量" : 25
    "Cloud CDN キャッシュ" : 20
    "Cloud Monitoring" : 5
    "その他 GCP Services" : 5
```

### 月間コスト見積もり (1000ユーザー想定)

| サービス | 使用量 | 月額コスト (USD) |
|----------|--------|------------------|
| Cloud Functions | 100,000 invocations | $0.40 |
| Firebase Hosting | 10GB transfer | $1.15 |
| Cloud CDN | 50GB | $2.50 |
| Cloud Monitoring | Basic | $0.50 |
| **合計** | | **$4.55** |

## 運用・監視

### モニタリング指標

```mermaid
graph TB
    subgraph "Performance Metrics"
        LATENCY[レスポンス時間<br/>目標: <100ms<br/>現在: 60.69ms]
        ERROR[エラー率<br/>目標: <0.1%<br/>現在: 0.05%]
        AVAIL[可用性<br/>目標: 99.9%<br/>現在: 99.95%]
    end

    subgraph "Business Metrics"
        USERS[アクティブユーザー<br/>日次・月次追跡]
        CONV[診断完了率<br/>フォーム→結果表示]
        USAGE[使用パターン<br/>時間帯・名前傾向]
    end

    LATENCY --> ERROR
    ERROR --> AVAIL
    USERS --> CONV
    CONV --> USAGE

    classDef performance fill:#e8f5e8
    classDef business fill:#e3f2fd

    class LATENCY,ERROR,AVAIL performance
    class USERS,CONV,USAGE business
```

## GCPサービス関連図

### 使用中のGCPサービス一覧

```mermaid
graph TB
    subgraph "Core Services - コアサービス"
        CF[Cloud Functions<br/>⚡ サーバーレス実行環境<br/>- HTTP Trigger<br/>- 自動スケーリング<br/>- Python 3.13 Runtime]
        CS[Cloud Storage<br/>🗄️ 静的ホスティング<br/>- Frontend配信<br/>- 高可用性<br/>- グローバル配信]
    end

    subgraph "Development & Deployment - 開発・デプロイ"
        IAM[Cloud IAM<br/>🔐 アクセス管理<br/>- 役割ベース制御<br/>- セキュリティポリシー<br/>- サービスアカウント]
        RM[Resource Manager<br/>📁 プロジェクト管理<br/>- ai-tools-471505<br/>- リソース組織化<br/>- 請求管理]
    end

    subgraph "Monitoring & Operations - 監視・運用"
        CM[Cloud Monitoring<br/>📊 パフォーマンス監視<br/>- メトリクス収集<br/>- アラート設定<br/>- ダッシュボード]
        CL[Cloud Logging<br/>📋 ログ管理<br/>- 構造化ログ<br/>- セキュリティログ<br/>- 検索・分析]
        CE[Cloud Error Reporting<br/>🚨 エラー追跡<br/>- 例外監視<br/>- アラート通知<br/>- デバッグ支援]
    end

    subgraph "Networking & Security - ネットワーク・セキュリティ"
        VPC[Virtual Private Cloud<br/>🌐 ネットワーク基盤<br/>- プライベートネットワーク<br/>- ファイアウォール<br/>- セキュリティグループ]
        CDN[Cloud CDN<br/>⚡ コンテンツ配信<br/>- グローバルキャッシュ<br/>- 高速配信<br/>- DDoS保護]
    end

    subgraph "Regional Configuration - リージョン設定"
        REGION[asia-northeast1<br/>🗾 東京リージョン<br/>- 低レイテンシ<br/>- データ主権<br/>- 災害対策]
    end

    %% Core Dependencies
    CF --> CS
    CF --> IAM
    CS --> IAM
    
    %% Monitoring Integration
    CF --> CM
    CF --> CL
    CF --> CE
    CS --> CM
    CS --> CL
    
    %% Network Integration
    CF --> VPC
    CS --> CDN
    CDN --> VPC
    
    %% Resource Management
    RM --> CF
    RM --> CS
    RM --> IAM
    RM --> CM
    RM --> CL
    RM --> CE
    RM --> VPC
    RM --> CDN
    
    %% Regional Deployment
    CF --> REGION
    CS --> REGION
    CM --> REGION
    CL --> REGION
    CE --> REGION

    %% Styling
    classDef core fill:#4285f4,color:#fff
    classDef dev fill:#34a853,color:#fff
    classDef monitor fill:#ea4335,color:#fff
    classDef network fill:#fbbc04,color:#000
    classDef region fill:#9aa0a6,color:#fff

    class CF,CS core
    class IAM,RM dev
    class CM,CL,CE monitor
    class VPC,CDN network
    class REGION region
```

### サービス間の詳細関連性

```mermaid
graph LR
    subgraph "Request Flow - リクエストフロー"
        USER[👤 ユーザー]
        BROWSER[🌐 ブラウザ]
    end

    subgraph "Google Cloud Platform"
        subgraph "Frontend Layer"
            STORAGE[Cloud Storage<br/>静的ホスティング]
            CDN[Cloud CDN<br/>グローバル配信]
        end
        
        subgraph "API Layer"
            FUNCTIONS[Cloud Functions<br/>API実行]
            IAM[Cloud IAM<br/>認証・認可]
        end
        
        subgraph "Security Layer"
            SEC[セキュリティ対策<br/>Phase A実装済み<br/>- オリジン制限<br/>- レート制限<br/>- User-Agent検証]
        end
        
        subgraph "Monitoring Layer"
            LOGGING[Cloud Logging<br/>セキュリティログ]
            MONITORING[Cloud Monitoring<br/>メトリクス]
            ERROR[Error Reporting<br/>例外追跡]
        end
    end

    %% User Request Flow
    USER --> BROWSER
    BROWSER --> CDN
    CDN --> STORAGE
    STORAGE --> FUNCTIONS
    
    %% Security Integration
    FUNCTIONS --> SEC
    SEC --> LOGGING
    
    %% Authentication & Authorization
    FUNCTIONS --> IAM
    STORAGE --> IAM
    
    %% Monitoring Integration
    FUNCTIONS --> MONITORING
    FUNCTIONS --> ERROR
    STORAGE --> MONITORING
    SEC --> LOGGING

    %% Styling
    classDef user fill:#e3f2fd
    classDef frontend fill:#f3e5f5
    classDef api fill:#e8f5e8
    classDef security fill:#fce4ec
    classDef monitoring fill:#fff3e0

    class USER,BROWSER user
    class STORAGE,CDN frontend
    class FUNCTIONS,IAM api
    class SEC security
    class LOGGING,MONITORING,ERROR monitoring
```

### GCPサービス設定詳細

```mermaid
graph TB
    subgraph "Cloud Functions Configuration"
        CF_CONFIG[seimei-handan Function<br/>━━━━━━━━━━━━━━━━<br/>• Runtime: Python 3.13<br/>• Memory: 512MB<br/>• Timeout: 60s<br/>• Region: asia-northeast1<br/>• Trigger: HTTP<br/>• Entry Point: seimei_handan<br/>• Auth: allow-unauthenticated]
    end

    subgraph "Cloud Storage Configuration"
        CS_CONFIG[Frontend Hosting Bucket<br/>━━━━━━━━━━━━━━━━━━━━<br/>• Bucket: seimei-handan-frontend-storage<br/>• Location: Multi-region<br/>• Storage Class: Standard<br/>• Public Access: Enabled<br/>• Website Configuration: Enabled<br/>• CORS: Configured for API access]
    end

    subgraph "Security Configuration"
        SEC_CONFIG[セキュリティ設定<br/>━━━━━━━━━━━━━━<br/>• Origin制限: storage.googleapis.com<br/>• Rate Limiting: 10 req/min<br/>• User-Agent検証: Enabled<br/>• Security Logging: Enabled<br/>• CORS: Configured<br/>• HTTPS Enforcement: Enabled]
    end

    subgraph "Monitoring Configuration"
        MON_CONFIG[監視・ログ設定<br/>━━━━━━━━━━━━━━<br/>• Cloud Logging: Structured logs<br/>• Cloud Monitoring: Custom metrics<br/>• Error Reporting: Exception tracking<br/>• Alerting: Performance & errors<br/>• Dashboard: Real-time monitoring]
    end

    CF_CONFIG --> SEC_CONFIG
    CS_CONFIG --> SEC_CONFIG
    SEC_CONFIG --> MON_CONFIG

    classDef config fill:#e8f5e8
    classDef security fill:#fce4ec
    classDef monitoring fill:#fff3e0

    class CF_CONFIG,CS_CONFIG config
    class SEC_CONFIG security
    class MON_CONFIG monitoring
```

### コスト構成とサービス利用料

```mermaid
pie title 月間コスト分布 (1000ユーザー想定)
    "Cloud Functions (実行時間)" : 40
    "Cloud Storage (ストレージ・転送)" : 30
    "Cloud CDN (配信)" : 20
    "Cloud Monitoring & Logging" : 7
    "その他 (IAM, Resource Manager)" : 3
```

---

**更新日**: 2025年9月10日  
**バージョン**: 1.1 (セキュリティ対策Phase A実装)  
**ステータス**: 本番運用中・セキュリティ強化済み