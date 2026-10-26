# unionpay-merchant-onboarding-archive · 商户进件材料归档

`unionpay-merchant-onboarding-archive` 归档收单商户进件阶段提交的材料清单与审核留痕，
供分支机构复核与巡检抽样使用。当前归档批次 `2026-Q3`。

## 目录

| 文件 | 说明 |
|---|---|
| `archive/merchant-docs.csv` | 进件材料清单（已按归档口径脱敏） |
| `src/archive_loader.py` | 清单加载与完整性校验 |

## 标识

归档系统在配置中心注册为 `unionpay-merchant-onboarding-archive`，
见 `src/archive_loader.py` 的 `ARCHIVE_NAME` 常量与本文档标题。

## 字段说明

| 字段 | 说明 |
|---|---|
| `mch_no` | 商户号，15 位 |
| `mch_name` | 商户名称（已脱敏为字号 + `**`） |
| `branch` | 受理分支机构 |
| `mcc` | 商户类别码 |
| `doc_type` | 材料类型：营业执照 / 开户许可 / 法人证件 / 结算账户 / 门店照 |
| `expire_date` | 材料有效期 |
| `reviewer` | 复核人工号 |
| `contact` | 联系人手机，已掩码 |

## 完整性校验

1. 五类材料齐全才算进件完成，缺任一类标记 `incomplete`。
2. 营业执照与法人证件到期日在 30 日内标 `expiring`，需提前换证。
3. 同一商户号重复进件以 `submit_time` 最新一条为准。

## 已知问题

1. 分支机构改名后历史记录仍用旧机构名，跨期对比需走机构映射表。
2. `mcc` 存在少量历史非法值（如 `5999` 被手工改成 `5998`），校验只告警不阻断。

## 维护

收单运营支持组（内部 IM 群 `#acq-ops`）。
