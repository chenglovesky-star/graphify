# Fork 自定义变更

> 本 fork 在 [safishamsi/graphify](https://github.com/safishamsi/graphify) 基础上添加 PyInstaller 单文件二进制构建，用于 [second-brain-installer](https://github.com/your-name/second-brain-installer) 集成。

## 变更内容

| 文件 | 状态 | 说明 |
|------|------|------|
| `graphify.spec` | **新增** | PyInstaller 配置，打包成单文件二进制 |
| `.github/workflows/release.yml` | **新增** | GitHub Actions，5 平台 CI 自动构建 + Release |
| `graphify/__main__.py` 等源码 | **未修改** | 跟随 upstream 同步 |

## 触发 Release

```bash
# 在 v8 分支上打 tag
git tag v0.8.47-test
git push origin v0.8.47-test
```

CI 会自动：
1. 在 5 个平台（macOS arm64/x64, Linux x64/arm64, Windows x64）构建
2. 计算每个二进制的 SHA256
3. 创建 GitHub Release,资产包括：
   - `graphify-darwin-arm64`
   - `graphify-darwin-x64`
   - `graphify-linux-arm64`
   - `graphify-linux-x64`
   - `graphify-windows-x64.exe`
   - `SHA256SUMS`

## second-brain-installer 集成

安装器通过 `brain.lock.json` 下载对应平台二进制：

```jsonc
{
  "components": {
    "graphify": {
      "name": "graphify",
      "version": "0.8.47",
      "installMethod": "github-release",
      "repo": "chenglovesky-star/graphify",
      "tag": "v${version}",
      "source": {
        "darwin-arm64": "${ghProxy}${repo}/releases/download/v${version}/graphify-darwin-arm64",
        ...
      },
      "sha256": { /* 从 SHA256SUMS 复制 */ }
    }
  }
}
```

## 同步 Upstream

```bash
git fetch upstream
git checkout v8
git merge upstream/v8
# 解决冲突(本 fork 只改了 spec 和 workflow,通常无冲突)
git push origin v8
# 打新 tag 触发 Release
git tag v0.8.48
git push --tags
```