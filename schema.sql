CREATE TABLE IF NOT EXISTS service_schedule_rule (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  host_name VARCHAR(255) NOT NULL,
  service_name VARCHAR(255) NOT NULL,
  action_type VARCHAR(16) NOT NULL COMMENT 'START or STOP',
  cron_expr VARCHAR(64) NOT NULL,
  timezone VARCHAR(64) DEFAULT 'Asia/Shanghai',
  is_enabled TINYINT NOT NULL DEFAULT 1,
  service_owner VARCHAR(128) NOT NULL,
  remark VARCHAR(255) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY idx_host_service (host_name, service_name)
);

CREATE TABLE IF NOT EXISTS service_owner_contact (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  owner_name VARCHAR(128) NOT NULL UNIQUE,
  mobile VARCHAR(64) NOT NULL,
  email VARCHAR(255) NULL,
  dingding VARCHAR(255) NULL,
  remark VARCHAR(255) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alert_aggregation (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  bucket_start DATETIME NOT NULL,
  hostname VARCHAR(255) NOT NULL,
  service_name VARCHAR(255) NOT NULL,
  status VARCHAR(32) NOT NULL,
  robot_token VARCHAR(255) NOT NULL,
  session VARCHAR(16) NOT NULL,
  service_owner VARCHAR(128) NULL,
  mobile VARCHAR(64) NULL,
  count INT NOT NULL DEFAULT 1,
  latest_event_json JSON NULL,
  flushed TINYINT NOT NULL DEFAULT 0,
  flushed_at DATETIME NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uk_bucket_host_service_status_token (bucket_start, hostname, service_name, status, robot_token),
  KEY idx_flushed_bucket (flushed, bucket_start)
);
