---
name: "策略代码生成器"
description: "根据用户给出的策略思路，自动生成 SimTradeLab 可运行策略代码，并可在生成后根据用户选择直接运行回测。当用户提供策略逻辑并要求创建策略代码骨架、回测脚本或策略实现时使用。"
---

# 策略代码生成器

该技能用于将用户的自然语言策略描述转换为 SimTradeLab 可直接运行的最小策略代码。生成后根据用户选择，决定是否直接运行回测。

## 触发条件

- 用户给出策略逻辑，要求创建或生成策略代码
- 用户要求写策略骨架、回测脚本或策略实现
- 用户描述买入或卖出规则，希望落地为可运行代码
- 用户提到策略代码、创建策略
- 生成策略后用户要求运行或检查结果
- 用户提出修改已有策略代码或策略逻辑时

## 工作流程

1. 明确策略约束：市场、频率、标的范围、持仓规则、出场规则
2. 从项目文档确认可用接口：优先参考 `docs/PTrade_API_Complete_Reference.md`、`docs/TOOLS.md`
3. 映射到最小必要接口与数据字段，不引入未确认接口
4. 在 `strategies/<中文策略名>/` 下生成策略入口文件，默认文件名为 `backtest.py`
5. 在同一目录下生成 `run.py`，内容参考 `src/simtradelab/backtest/run.py`
6. `run.py` 中只修改必要配置项，其余代码、注释、结构保持与 `src/simtradelab/backtest/run.py` 完全一致
7. 在同一目录下生成或更新策略规则说明文档，文件名为 `策略规则.md`
8. 若修改已有策略，必须同步更新对应 `策略规则.md` 中的交易规则说明
9. 仅保存文件，不主动询问是否运行

## 目录规范

所有策略相关脚本必须放在该策略自己的目录下，严禁散落在项目其他位置。

策略文件夹名称必须使用中文命名，禁止使用英文或拼音。

## 策略规则文档

每个策略目录下必须包含 `策略规则.md`，用于详细记录当前策略的交易规则。

### 文档要求

- 文件路径：`strategies/<中文策略名>/策略规则.md`
- 文档必须使用 Markdown 格式，结构清晰，便于阅读和后续维护
- 文档标题结构必须严格遵循以下固定标题层级，AI 只能在这些固定标题下增加内容，或新增二级/三级标题，不得删除或修改固定标题：
  - 固定二级标题（必须保留）：
    - `## 运行配置`
    - `## 交易规则`
  - 固定三级标题（必须保留）：
    - `### 买入规则`
    - `### 卖出规则`
    - `### 仓位规则`
    - `### 止盈规则`
    - `### 止损规则`
    - `### 其他规则`
- 若策略有相似文件，优先修改现有策略文件，而不是新建策略文件
- 修改已有策略时，必须同步更新 `策略规则.md` 中的交易规则说明，确保文档与代码保持一致

## 代码规范

- 默认中文注释
- 生命周期函数：`initialize`、`before_trading_start`、`handle_data`、`after_trading_end`
- 状态变量统一使用 `g.` 前缀
- 数据获取优先使用 `get_history`，字段明确列出
- 日志使用 `log.info`
- 保持最小实现，不做超出要求的扩展
- 注释必须详细，方便后续检查策略文件的正确性
- 在关键逻辑、信号计算、交易执行处添加说明性注释，解释每一步的目的和判断依据
- 对于复杂的计算逻辑，需要注释说明计算原理和预期结果
- 在关键位置必须打印日志，便于检查策略逻辑的正确性
- 日志应覆盖：数据获取、信号计算过程、买入/卖出条件判断、仓位变化、异常或边界情况
- 使用 `log.info` 打印关键中间值和最终决策，确保回测输出可追溯、可验证

## 模板结构

```python
# -*- coding: utf-8 -*-
"""
<策略名称>
"""


def initialize(context):
    g.security = '<标的代码>'
    set_universe(g.security)
    g.state = {}


def handle_data(context, data):
    security = g.security
    # 1. 获取数据
    # 2. 计算信号
    # 3. 执行交易
    pass


def after_trading_end(context, data):
    # 日志或状态记录
    pass
```

## 生成规则

- 策略代码必须放在项目根目录下的 `strategies/<中文策略名>/` 目录中，文件夹名称必须使用中文
- 策略入口文件默认命名为 `backtest.py`，如需实盘也可提供 `live.py`
- 回测入口文件命名为 `run.py`，严格参考 `src/simtradelab/backtest/run.py` 的配置结构与运行方式
- `run.py` 只改动必要配置项，如 `strategy_name`、`strategy_file`、`start_date`、`end_date` 等策略相关配置；其余代码、注释、导入、UTF-8 配置、路径过滤逻辑等保持与 `src/simtradelab/backtest/run.py` 完全一致
- 默认单一标的；若用户明确多标的，再扩展
- 默认日线 `1d`；若用户明确分钟线，再改为 `1m`
- 默认现金全仓或按用户指定仓位买入
- 若用户未指定日期范围，默认使用 `2025-05-15` 至 `2026-01-30`
- 涨停或跌停判断优先使用 `high_limit`、`low_limit`、`unlimited`
- 必须明确出场条件，避免无限持仓
- 不在代码中引入未在项目文档中确认的接口
- **严禁**将策略脚本放在 `strategies/<中文策略名>/` 以外的任何目录
- 所有与该策略相关的文件（包括但不限于 `backtest.py`、`run.py`、`live.py`、配置文件、数据文件等）都必须存放在 `strategies/<中文策略名>/` 目录内

## 运行规则

- 生成文件后，不主动询问是否运行回测
- 若用户明确要求运行，使用项目约定方式执行 `run.py`
- 若用户未明确要求，仅保存文件，不执行任何运行命令
- 运行失败时，将错误信息反馈给用户，不隐藏异常
- 策略文件生成或修改完成后，必须向用户说明策略文件的核心买入卖出条件，包括信号触发条件、仓位管理规则和出场条件
- 说明内容应简洁明了，突出策略的关键交易逻辑，便于用户快速验证策略是否符合预期

## 示例

用户输入：
"5日均线斜率大于0买入，小于0卖出，需要下一根K线确认"

在 `strategies/五日均线斜率/` 下生成 `backtest.py`：

```python
# -*- coding: utf-8 -*-
"""
5日均线斜率策略
"""


def initialize(context):
    g.security = '000333.SZ'
    set_universe(g.security)
    g.last_slope = 0


def handle_data(context, data):
    security = g.security

    # 1. 获取数据
    df = get_history(6, '1d', 'close', security, fq=None, include=True)
    if len(df) < 6:
        log.info('[跳过] 数据不足，当前长度=%d' % len(df))
        return
    closes = df['close'].values
    log.info('[数据] 收盘价=%s' % closes)

    # 2. 计算信号
    ma5_series = [closes[i:i+5].mean() for i in range(6)]
    x = [0, 1, 2, 3, 4, 5]
    slope = float(__import__('numpy').polyfit(x, ma5_series, 1)[0])
    current_price = closes[-1]
    last_ma5 = ma5_series[-1]
    log.info('[信号] 斜率=%.6f, 当前价格=%.2f, 上一根MA5=%.2f' % (slope, current_price, last_ma5))

    # 3. 执行交易
    position = get_position(security)
    has_position = position.amount > 0
    log.info('[持仓] 当前持仓数量=%d, 是否持仓=%s' % (position.amount if position else 0, has_position))

    if slope > 0 and current_price > last_ma5 and not has_position:
        order_value(security, context.portfolio.cash)
        log.info('[买入] 斜率=%.6f, 价格=%.2f, MA5=%.2f, 可用资金=%.2f' % (
            slope, current_price, last_ma5, context.portfolio.cash))
    elif slope < 0 and current_price < last_ma5 and has_position:
        order_target(security, 0)
        log.info('[卖出] 斜率=%.6f, 价格=%.2f, MA5=%.2f' % (slope, current_price, last_ma5))
    else:
        log.info('[观望] 斜率=%.6f, 价格=%.2f, MA5=%.2f, 持仓=%s' % (
            slope, current_price, last_ma5, has_position))
    g.last_slope = slope


def after_trading_end(context, data):
    security = g.security
    position = get_position(security)
    log.info('日期 | 斜率: %.6f | 持仓: %d | 总资产: %.2f' % (
        g.last_slope, position.amount if position else 0, context.portfolio.portfolio_value))
```

在同一目录下生成 `run.py`，参考 `src/simtradelab/backtest/run.py`：

```python
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (c) 2025 Kay
#
# This file is part of SimTradeLab, dual-licensed under AGPL-3.0 and a
# commercial license. See LICENSE-COMMERCIAL.md or contact kayou@duck.com
#
"""
回测主入口 - 全量配置

包含 BacktestConfig 所有配置项，按需修改后运行即可。
"""


import sys

# 确保控制台 UTF-8 编码和实时输出（兼容 Windows）
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
sys.stderr.reconfigure(encoding='utf-8')

from simtradelab.backtest.runner import BacktestRunner
from simtradelab.backtest.config import BacktestConfig


if __name__ == '__main__':
    # ==================== 策略配置 ====================

    # 策略名称（对应 strategies/ 下的子目录名，必须使用中文）
    strategy_name = '五日均线斜率'

    # 策略文件名（默认 backtest.py，实盘模拟用 live.py）
    strategy_file = 'backtest.py'

    # ==================== 回测周期 ====================

    # 起止日期（格式：YYYY-MM-DD）
    start_date = '2025-05-15'
    end_date = '2026-01-30'

    # ==================== 资金与费用 ====================

    # 初始资金（元），必须大于 0
    initial_capital = 100000.0

    # ==================== 市场与券商 ====================

    # 市场代码：CN=A股，US=美股
    market = 'CN'

    # 券商 API 口径：auto / guosheng / dongguan / shanxi
    broker_profile = 'auto'

    # T+1 交易规则：None=使用市场默认（CN=True, US=False），可显式覆盖
    t_plus_1 = None

    # ==================== 数据配置 ====================

    # 行情数据根目录（None 使用项目默认路径）
    data_path = None

    # 策略目录（None 使用项目默认路径）
    strategies_path = None

    # 是否使用 DataServer（复用缓存，避免重复加载）
    use_data_server = True

    # ==================== 回测频率 ====================

    # 回测频率：'1d' 日线级别，'1m' 分钟级别
    frequency = '1d'

    # ==================== 基准配置 ====================

    # 基准代码（空串=使用市场默认基准，如 '000300' 沪深300）
    benchmark_code = '000016.SS'

    # ==================== 输出控制 ====================

    # 是否生成图表
    enable_charts = True

    # 是否写入日志文件
    enable_logging = True

    # 是否导出 CSV（持仓明细、每日统计等）
    enable_export = True

    # ==================== 性能配置 ====================

    # 是否启用多进程数据预加载
    enable_multiprocessing = True

    # 多进程 worker 数量（None=自动，取 CPU 核心数-1）
    num_workers = None

    # ==================== 语言 ====================

    # 界面语言：None=自动（CN→zh, 其他→系统检测），可显式指定 zh / en / de
    locale = None

    # ==================== 优化模式 ====================

    # 优化模式：跳过策略验证和依赖分析（由优化器框架管理）
    optimization_mode = False

    # ==================== 启动回测 ====================

    # 构建配置（data_path / strategies_path 为 None 时不传入，让默认值生效）
    _config_kwargs = dict(
        strategy_name=strategy_name,
        strategy_file=strategy_file,
        start_date=start_date,
        end_date=end_date,
        initial_capital=initial_capital,
        market=market,
        broker_profile=broker_profile,
        t_plus_1=t_plus_1,
        use_data_server=use_data_server,
        frequency=frequency,
        benchmark_code=benchmark_code,
        enable_charts=enable_charts,
        enable_logging=enable_logging,
        enable_export=enable_export,
        enable_multiprocessing=enable_multiprocessing,
        num_workers=num_workers,
        locale=locale,
        optimization_mode=optimization_mode,
    )

    # 过滤掉值为 None 的路径参数，让 Field(default_factory=...) 生效
    if data_path is not None:
        _config_kwargs['data_path'] = data_path
    if strategies_path is not None:
        _config_kwargs['strategies_path'] = strategies_path

    config = BacktestConfig(**_config_kwargs)

    # 运行方式：cd d:\Projects\Trade\SimTradeLab && poetry run python strategies/五日均线斜率/run.py
    runner = BacktestRunner()
    report = runner.run(config=config)
```

运行命令：`cd d:\Projects\Trade\SimTradeLab && poetry run python strategies/五日均线斜率/run.py`

同时在策略目录下生成 `策略规则.md`，示例如下：

```markdown
你作为回测系统策略开发专家，依据下述配置生成匹配系统编码规范的策略代码。
## 运行配置
- 开始日期：2025-05-15
- 结束日期：2026-01-30
- 交易标的：从A股所有股票里面寻找满足条件的
- K线周期：1d
## 交易规则
### 买入规则
- 每天检查前三天是涨停的票,当天买入
- 每只股票只买100股
### 卖出规则
- 结束日期全部卖出
### 仓位规则
- 最多能持有3只股票
- 每天最多只能买三只股票
### 止盈规则
- 收益≥10%卖出
- 收益从收益最高点回落3%卖出
### 止损规则
- 亏损5%卖出
### 其他规则
- 如果有相似的策略文件选择修改某个策略文件而不是新建策略文件
```

仅保存文件，等待用户明确要求运行后再执行。
