步骤概览（Windows）

1. 下载 DataX
- 官方仓库: https://github.com/alibaba/DataX
- 推荐下载 release 或 zip，解压到工作目录，例如 `E:\datax`。

2. 准备 MySQL 驱动
- DataX 自带的是 MySQL 5 驱动，远程库为新版驱动（示例 workspace 中有 `mysql-connector-java-8.0.27`）。
- 将 `mysql-connector-java-8.0.27.jar` 复制到 `E:\datax\plugin\writer\mysqlwriter\` 和 `E:\datax\plugin\reader\mysqlreader\` 目录下（覆盖或并存即可）。

3. 修改 Python 脚本（可选，仅当使用 python3 报错时）
- 如果运行 `datax.py` 出现 print 或 except 语法错误，需按 DataX 的 userGuide 修复 `bin` 下的脚本（小修正）。

4. 编写 job.json
- 参考 `mysql2mysql_2-5_template.json`，将 `writer` 的 `<LOCAL_*>` 占位符替换为本地 MySQL 连接信息。
- 若要同步其它表，复制 content 模块并修改 `querySql` 与 `table` 字段。

5. 运行 DataX（建议先打开 CMD/PowerShell 并设置编码）
```powershell
chcp 65001
python E:\datax\bin\datax.py E:\datax\job\mysql2mysql_2-5.json
```
- 如使用的是 DataX 的 `datax.py` 可直接运行；Windows 下有时需要 `python3`。

6. 常见注意事项
- 若某表包含 MySQL 保留字（例如 `index`），可在目标表字段用反引号包裹或重命名目标字段；也可以在 writer 的 `column` 中指定列名并映射。
- 大表请适当增大 `channel`（并发数），但注意目标库写入压力。
- 保存运行日志：DataX 会在控制台输出和 `log` 目录写入日志，用于截图证明同步成功。

示例 job 模板：`datax/mysql2mysql_2-5_template.json`
