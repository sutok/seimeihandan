# Load Balancer + SSL証明書設定 (seimei.shinyudo.com)

# 静的グローバルIPアドレス
resource "google_compute_global_address" "frontend_ip" {
  name = "${var.app_name}-global-ip"
  
  depends_on = [
    google_project_service.required_apis
  ]
}

# SSL証明書 (Google-managed)
resource "google_compute_managed_ssl_certificate" "frontend_ssl" {
  name = "${var.app_name}-ssl-cert"

  managed {
    domains = [var.domain_name]
  }

  lifecycle {
    create_before_destroy = true
  }
  
  depends_on = [
    google_project_service.required_apis
  ]
}

# Cloud Storage用バックエンド設定
resource "google_compute_backend_bucket" "frontend_backend" {
  name        = "${var.app_name}-backend-bucket"
  description = "Frontend storage backend for ${var.domain_name}"
  bucket_name = google_storage_bucket.frontend_bucket.name
  enable_cdn  = true

  cdn_policy {
    cache_mode        = "CACHE_ALL_STATIC"
    default_ttl       = 3600
    max_ttl           = 86400
    negative_caching  = true
    serve_while_stale = 86400
    
  }

  depends_on = [google_storage_bucket.frontend_bucket]
}

# URLマップ設定
resource "google_compute_url_map" "frontend_url_map" {
  name            = "${var.app_name}-url-map"
  description     = "URL map for ${var.domain_name}"
  default_service = google_compute_backend_bucket.frontend_backend.id

  # SPA用のフォールバック設定（React Router対応）
  host_rule {
    hosts        = [var.domain_name]
    path_matcher = "path-matcher-1"
  }

  path_matcher {
    name            = "path-matcher-1"
    default_service = google_compute_backend_bucket.frontend_backend.id

    # 静的アセット用
    path_rule {
      paths   = ["/static/*", "/assets/*", "/*.js", "/*.css", "/*.ico", "/*.png", "/*.jpg", "/*.svg"]
      service = google_compute_backend_bucket.frontend_backend.id
    }

    # APIコール以外は全てindex.htmlにリダイレクト（SPA対応）
    path_rule {
      paths   = ["/*"]
      service = google_compute_backend_bucket.frontend_backend.id
      
      route_action {
        url_rewrite {
          path_prefix_rewrite = "/index.html"
        }
      }
    }
  }
}

# HTTPSプロキシ
resource "google_compute_target_https_proxy" "frontend_https_proxy" {
  name             = "${var.app_name}-https-proxy"
  url_map          = google_compute_url_map.frontend_url_map.id
  ssl_certificates = [google_compute_managed_ssl_certificate.frontend_ssl.id]

  depends_on = [google_compute_managed_ssl_certificate.frontend_ssl]
}

# HTTPプロキシ（HTTPからHTTPSへのリダイレクト用）
resource "google_compute_url_map" "frontend_http_redirect" {
  name = "${var.app_name}-http-redirect"

  default_url_redirect {
    https_redirect         = true
    redirect_response_code = "MOVED_PERMANENTLY_DEFAULT"
    strip_query            = false
  }
}

resource "google_compute_target_http_proxy" "frontend_http_proxy" {
  name    = "${var.app_name}-http-proxy"
  url_map = google_compute_url_map.frontend_http_redirect.id
}

# Global Forwarding Rules
resource "google_compute_global_forwarding_rule" "frontend_https" {
  name                  = "${var.app_name}-https-forwarding-rule"
  ip_protocol           = "TCP"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  port_range            = "443"
  target                = google_compute_target_https_proxy.frontend_https_proxy.id
  ip_address            = google_compute_global_address.frontend_ip.id
}

resource "google_compute_global_forwarding_rule" "frontend_http" {
  name                  = "${var.app_name}-http-forwarding-rule"
  ip_protocol           = "TCP"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  port_range            = "80"
  target                = google_compute_target_http_proxy.frontend_http_proxy.id
  ip_address            = google_compute_global_address.frontend_ip.id
}