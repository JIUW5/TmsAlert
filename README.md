# TMS Alert Service

接收 n9e 告警事件并进行规则过滤、交易日校验、调度窗口判断、告警聚合与 webhook 发送。

## 功能覆盖

1. 接收 n9e 告警和恢复（`POST /events/n9e`）。
2. 使用 `labels.name + labels.hostname` 查询 MariaDB `service_schedule_rule`，判断是否由本服务管理。
3. 根据 `labels.ex` 调用交易日历 `/tradingDays` 校验交易日（按日盘/夜盘）。
4. 按规则表的 `START/STOP + cron_expr` 判断当前是否在调度时间内。
5. 根据 `service_owner` 查询 `service_owner_contact` 获取手机号。
6. 使用告警事件中的 `robot_token` 调 webhook 发送告警/恢复。
7. 1 分钟聚合（同主机+同服务+同状态+同 token），支持 K8s 多副本（通过数据库去重与 `FOR UPDATE SKIP LOCKED` 抢占刷新任务）。
8. 暴露 `/metrics` Prometheus 指标。

## 项目结构

```text
tms_alert_service/
├── app.py                       # FastAPI 应用、路由、生命周期
├── main.py                      # 进程启动入口
├── config.py                    # 环境配置
├── db.py                        # MariaDB 连接
├── metrics.py                   # Prometheus 指标定义
├── models.py                    # 请求模型
└── services/
    ├── event_processor.py       # 主处理流程编排
    ├── rule_service.py          # 规则查询 + cron 调度判断
    ├── calendar_service.py      # 交易日历校验
    ├── owner_service.py         # 负责人手机号查询
    ├── aggregation_service.py   # 1 分钟聚合 + 刷新发送
    ├── webhook_service.py       # webhook 发送
    └── time_utils.py            # 时区/日夜盘工具
```

## 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python setup.py develop
```

## 启动

```bash
tms-alert-service
```

或

```bash
uvicorn tms_alert_service.app:app --host 0.0.0.0 --port 8080
```

## 环境变量

- `DB_HOST/DB_PORT/DB_USER/DB_PASSWORD/DB_NAME`
- `CALENDAR_BASE_URL`（默认 `http://calendar.saturn-res.ipa.zs`）
- `WEBHOOK_URL_TEMPLATE`（默认 `http://172.17.228.97:5008/robot/send?access_token={token}`）
- `SESSION_TIMEZONE`（默认 `Asia/Shanghai`）
- `DAY_SESSION_START_HOUR`（默认 `8`）
- `DAY_SESSION_END_HOUR`（默认 `20`）
- `AGGREGATION_WINDOW_SECONDS`（默认 `60`）
- `AGGREGATION_FLUSH_INTERVAL_SECONDS`（默认 `5`）

## n9e 事件示例

```json
{
  "labels": {
    "name": "sftptd_exporter",
    "hostname": "kgi-cht-4",
    "ex": "NOT_SCHEDULED"
  },
  "status": "resolved",
  "robot_identifier": "IT_TradeService_India",
  "robot_token": "faa438..."
}
```

## Metrics

- `tms_event_total{status}`
- `tms_event_filtered_total{reason}`
- `tms_event_processed_total`
- `tms_webhook_send_total{result}`
- `tms_event_latency_seconds`
- `tms_pending_aggregation_records`

## K8s 多副本说明

- 每个副本都可接收事件并写入 `alert_aggregation`。
- 聚合发送使用数据库行锁 `FOR UPDATE SKIP LOCKED`，避免重复发送。
- 唯一键 `(bucket_start, hostname, service_name, status, robot_token)` 确保聚合幂等。

## 初始化数据库

```bash
mysql -h <host> -u <user> -p <db_name> < schema.sql
```

## 打包

```bash
python setup.py sdist bdist_wheel
```
