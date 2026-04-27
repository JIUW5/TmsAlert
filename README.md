# TMS Alert Service

按你建议改为 `app/` 分层目录，并使用 `config.yaml` 管理配置。

## 项目结构

```text
app/
├── api/
│   ├── router.py
│   └── routes/
│       ├── health.py
│       └── v1/
│           └── alerts.py
├── middlewares/
├── schemas/
│   └── event.py
├── services/
│   ├── aggregation_service.py
│   ├── calendar_service.py
│   ├── event_service.py
│   ├── owner_service.py
│   ├── rule_service.py
│   ├── time_service.py
│   └── webhook_service.py
├── config.py
├── db.py
├── metrics.py
└── main.py
config.yaml
schema.sql
setup.py
```

## 能力

1. 接收 n9e 告警和恢复（`POST /v1/events/n9e`）。
2. 使用 `labels.name + labels.hostname` 查 MariaDB 规则表。
3. 根据 `labels.ex` 调交易日历服务 `/tradingDays`。
4. 按 `START/STOP + cron_expr` 判断是否在调度窗口。
5. 按 `service_owner` 查手机号。
6. 使用 `robot_token` 调 webhook 发群消息。
7. 1 分钟聚合（同主机+同服务+同状态+同 token）。
8. 支持 K8s 多副本（DB 唯一键 + `FOR UPDATE SKIP LOCKED`）。
9. 暴露 `/metrics`。

## 配置

统一在 `config.yaml`：
- `app`
- `session`
- `aggregation`
- `mariadb`
- `calendar`
- `webhook`

## 启动

```bash
pip install -r requirements.txt
python setup.py develop
tms-alert-service
```

## API

- `GET /healthz`
- `GET /metrics`
- `POST /v1/events/n9e`
- `POST /v1/admin/flush`

## 打包

```bash
python setup.py sdist bdist_wheel
```
