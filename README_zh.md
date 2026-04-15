# Media Archive Organizer

面向高级用户的媒体整理工具，适用于需要重复检测、严格匹配和更高可控性的归档场景。

程序会优先读取图片 EXIF 时间；如果没有 EXIF 时间，则使用文件修改时间。
整理后的文件会按“年\月\日”的目录结构输出到目标目录中。

它支持：

- 基于日期的目录整理
- `move` / `copy` 两种模式
- 面向相似图片的 pHash 重复检测
- 面向完全一致文件的 SHA-256 严格检测
- 多语言命令行提示
- 每次运行独立日志，方便追溯

语言导航：

- English: [README.md](./README.md)
- 中文: [README_zh.md](./README_zh.md)
- 日本語: [README_ja.md](./README_ja.md)


## 项目定位

这是增强版媒体整理工程，适用于需要重复检测、严格匹配和更高可控性的场景。

相较于基础版按日期整理工具，它额外提供：

- 重复检测
- 严格的完全一致文件匹配
- 带阈值控制的相似图片检测
- 持久化 `hash_db`
- 更强的目标目录安全限制
- 最小自动化冒烟测试

如果你只需要低复杂度的按日期整理功能，基础版工具会更合适。


## 功能简介

- 递归扫描源目录中的子目录
- 按日期自动整理图片和视频
- 默认使用 `move` 模式移动文件
- 支持 `copy` 模式保留原文件
- 支持重复检测：可关闭、相似图片检测（pHash）或严格文件检测（SHA-256）
- 支持中文、英文、日文界面
- 每次运行自动生成独立日志文件
- 同名文件自动追加序号，避免直接覆盖


## 支持的文件类型

- `.jpg`
- `.jpeg`
- `.png`
- `.mp4`
- `.mov`


## 运行环境

- Windows 10 或 Windows 11
- Python 3.10 或更高版本
- 依赖库：`Pillow`

安装依赖：

```powershell
.\venv\Scripts\python.exe -m pip install Pillow
```

说明：

- 建议先在项目根目录执行 `python -m venv venv`
- 项目的虚拟环境默认位于 `.\venv`
- 更推荐使用 `.\venv\Scripts\python.exe` 和 `.\venv\Scripts\pip.exe`，这样可以明确知道依赖安装到了当前项目的虚拟环境中
- 如果直接执行 `python` 或 `pip`，有可能调用到系统 Python 或其他虚拟环境

如需更完整的环境说明，请参考：

- [ENVIRONMENT.md](./ENVIRONMENT.md)
- [环境配置说明.md](./环境配置说明.md)
- [環境設定ガイド.md](./環境設定ガイド.md)


## 基本用法

请先进入项目根目录，再执行命令：

```powershell
cd D:\ImageOrganizer
```

推荐执行方式：

```powershell
.\venv\Scripts\python.exe .\main.py --src 源目录 --dst 目标目录
```

示例：

```powershell
.\venv\Scripts\python.exe .\main.py --src D:\InputPhotos --dst D:\SortedPhotos
```


## 启动参数

### `--src`

源目录，必填。

### `--dst`

目标目录，必填。

### `--mode`

整理模式，可选：

- `move`：移动文件，默认值
- `copy`：拷贝文件，保留原文件

示例：

```powershell
.\venv\Scripts\python.exe .\main.py --src D:\InputPhotos --dst D:\SortedPhotos --mode copy
```

### `--lang`

界面语言，可选：

- `zh`：中文
- `en`：英文
- `ja`：日文

示例：

```powershell
.\venv\Scripts\python.exe .\main.py --src D:\InputPhotos --dst D:\SortedPhotos --lang en
.\venv\Scripts\python.exe .\main.py --src D:\InputPhotos --dst D:\SortedPhotos --lang ja
```

### `--duplicate-detection`

重复检测模式，可选：

- `off`：关闭重复检测
- `phash`：使用 pHash 检测相似图片
- `strict`：使用 SHA-256 检测完全一致文件

说明：

- `phash` 更适合检测视觉上相近的图片
- `strict` 更适合严格用户，只有文件内容完全一致才会判定为重复
- `hash_db` 仅作为当前目标目录下的参考，不会把文件导向其他历史目标目录

示例：

```powershell
.\venv\Scripts\python.exe .\main.py --src D:\InputPhotos --dst D:\SortedPhotos --duplicate-detection off
.\venv\Scripts\python.exe .\main.py --src D:\InputPhotos --dst D:\SortedPhotos --duplicate-detection strict
```

### `--phash-threshold`

设置 pHash 相似检测的最大汉明距离，默认值为 `4`。

说明：

- 数值越小，判定越严格
- 数值越大，越容易把相似图片视为重复
- 仅在 `--duplicate-detection phash` 时生效

示例：

```powershell
.\venv\Scripts\python.exe .\main.py --src D:\InputPhotos --dst D:\SortedPhotos --duplicate-detection phash --phash-threshold 4
```


## 常用示例

### 默认移动文件

```powershell
.\venv\Scripts\python.exe .\main.py --src D:\InputPhotos --dst D:\SortedPhotos
```

### 拷贝文件，不删除源文件

```powershell
.\venv\Scripts\python.exe .\main.py --src D:\InputPhotos --dst D:\SortedPhotos --mode copy
```

### 使用英文界面

```powershell
.\venv\Scripts\python.exe .\main.py --src D:\InputPhotos --dst D:\SortedPhotos --lang en
```

### 使用日文界面

```powershell
.\venv\Scripts\python.exe .\main.py --src D:\InputPhotos --dst D:\SortedPhotos --lang ja
```

### 使用严格重复检测

```powershell
.\venv\Scripts\python.exe .\main.py --src D:\InputPhotos --dst D:\SortedPhotos --duplicate-detection strict
```

### 使用相似图片检测

```powershell
.\venv\Scripts\python.exe .\main.py --src D:\InputPhotos --dst D:\SortedPhotos --duplicate-detection phash --phash-threshold 4
```


## 日志说明

程序每次运行都会自动在脚本所在目录下创建或使用 `log` 文件夹。

日志文件名格式如下：

```text
organize_log_YYYYMMDD_HHMMSS.txt
```

例如：

```text
organize_log_20260413_135222.txt
```

程序执行完成后，终端会显示本次日志文件的完整路径。


## 整理规则

- 程序会递归扫描源目录中的所有子目录
- 优先读取图片 EXIF 时间
- 若无 EXIF 时间，则使用文件修改时间
- 按 `目标目录\年\月\日\` 的形式输出
- 若启用重复检测，只会参考当前目标目录中的历史记录
- 若目标目录存在同名文件，会自动追加序号

同名文件示例：

```text
photo.jpg
photo_1.jpg
photo_2.jpg
```


## 文件结构说明

- `main.py`
  程序入口
- `core/`
  日期识别和 EXIF 读取逻辑
- `services/`
  文件整理逻辑
- `locales/`
  中英日提示文本
- `log/`
  每次运行生成的日志目录


## 注意事项

- 请确保源目录和目标目录填写正确
- 默认 `move` 模式会将文件从源目录移走
- 如果需要保留原文件，请使用 `--mode copy`
- 建议首次先使用少量文件测试
- 建议重要资料先备份再处理


## 常见失败原因

- 文件被占用，无法移动或拷贝
- 文件没有读取权限
- 图片 EXIF 信息异常
- 目标目录没有写入权限


## 免责声明

本工具用于对图片和视频文件进行自动整理。
在实际使用中，仍可能因路径错误、权限问题、文件占用、磁盘异常、时间信息错误、程序中断或其他不可预见因素导致整理结果不符合预期。

请特别注意以下事项：

- 默认 `move` 模式会移动原文件
- 同名文件会自动重命名
- EXIF 或文件时间不准确时，目标日期目录可能不符合真实拍摄日期
- 日志仅用于辅助排查，不构成结果完整性保证

为降低风险，建议：

1. 首次使用时先处理少量测试文件
2. 优先使用 `--mode copy` 验证效果
3. 正式处理前备份重要数据
4. 处理完成后检查日志与目标目录

更完整的免责说明请参考：

- [免责声明.md](./免责声明.md)
