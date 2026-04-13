# ImageOrganizer

画像や動画ファイルを日付別に整理するための Python ツールです。

本プログラムは、まず画像の EXIF 時刻を読み取ります。
EXIF 時刻が取得できない場合は、ファイルの更新日時を使用します。
整理後のファイルは、保存先ディレクトリ内で `年\月\日` のフォルダ構成に配置されます。


## 主な機能

- ソースフォルダ配下のサブフォルダを再帰的に走査
- 画像と動画を日付で自動整理
- デフォルトで `move` モードを使用
- 元ファイルを残す `copy` モードに対応
- 中国語、英語、日本語 UI に対応
- 実行ごとに個別のログファイルを生成
- 同名ファイルがある場合は自動で連番を付与


## 対応ファイル形式

- `.jpg`
- `.jpeg`
- `.png`
- `.mp4`
- `.mov`


## 実行環境

- Windows 10 または Windows 11
- Python 3.10 以上
- 依存ライブラリ: `Pillow`

依存関係のインストール:

```powershell
pip install Pillow
```

環境構築の詳細は以下を参照してください。

- [ENVIRONMENT.md](./ENVIRONMENT.md)
- [环境配置说明.md](./环境配置说明.md)
- [環境設定ガイド.md](./環境設定ガイド.md)


## 基本的な使い方

プロジェクトのルートディレクトリでターミナルを開き、次を実行します。

```powershell
python main.py --src ソースフォルダ --dst 保存先フォルダ
```

例:

```powershell
python main.py --src D:\InputPhotos --dst D:\SortedPhotos
```


## 起動パラメータ

### `--src`

ソースフォルダ。必須です。

### `--dst`

保存先フォルダ。必須です。

### `--mode`

整理モード:

- `move`: ファイルを移動。デフォルト
- `copy`: ファイルをコピーし、元ファイルを保持

例:

```powershell
python main.py --src D:\InputPhotos --dst D:\SortedPhotos --mode copy
```

### `--lang`

表示言語:

- `zh`: 中国語
- `en`: 英語
- `ja`: 日本語

例:

```powershell
python main.py --src D:\InputPhotos --dst D:\SortedPhotos --lang en
python main.py --src D:\InputPhotos --dst D:\SortedPhotos --lang ja
```


## よく使う例

### デフォルトでファイルを移動

```powershell
python main.py --src D:\InputPhotos --dst D:\SortedPhotos
```

### 元ファイルを残してコピー

```powershell
python main.py --src D:\InputPhotos --dst D:\SortedPhotos --mode copy
```

### 英語 UI を使用

```powershell
python main.py --src D:\InputPhotos --dst D:\SortedPhotos --lang en
```

### 日本語 UI を使用

```powershell
python main.py --src D:\InputPhotos --dst D:\SortedPhotos --lang ja
```


## ログについて

プログラムはスクリプトのディレクトリ配下に `log` フォルダを自動作成または再利用します。

ログファイル名は次の形式です。

```text
organize_log_YYYYMMDD_HHMMSS.txt
```

例:

```text
organize_log_20260413_135222.txt
```

実行完了後、生成されたログファイルのフルパスが表示されます。


## 整理ルール

- ソースフォルダ配下のすべてのサブフォルダを再帰的に走査
- まず画像の EXIF 時刻を使用
- EXIF がない場合はファイル更新日時を使用
- `保存先\年\月\日\` に出力
- 同名ファイルが存在する場合は連番を追加

同名ファイルの例:

```text
photo.jpg
photo_1.jpg
photo_2.jpg
```


## プロジェクト構成

- `main.py`
  実行エントリーポイント
- `core/`
  日付判定と EXIF 読み取りロジック
- `services/`
  ファイル整理ロジック
- `locales/`
  中国語、英語、日本語の表示テキスト
- `log/`
  実行ごとのログ出力フォルダ


## 注意事項

- ソースと保存先のパスが正しいことを確認してください
- デフォルトの `move` モードでは元ファイルがソースから移動されます
- 元ファイルを残したい場合は `--mode copy` を使用してください
- まずは少量のファイルでテストすることを推奨します
- 大量処理の前に重要ファイルをバックアップしてください


## よくある失敗原因

- ファイル使用中で移動またはコピーできない
- ファイル権限が不足している
- 画像の EXIF 情報が不正
- 保存先ディレクトリに書き込み権限がない


## 免責事項

本ツールは、画像および動画ファイルを自動整理するためのものです。
実際の使用においては、パスの誤り、権限の問題、ファイルのロック、ディスク異常、時刻情報の誤り、実行中断、その他予期しない要因により、整理結果が期待どおりにならない場合があります。

特に以下にご注意ください。

- デフォルトの `move` モードでは元ファイルが移動されます
- 同名ファイルは自動的にリネームされます
- EXIF 時刻やファイル時刻が不正確な場合、保存先の日付フォルダが実際の撮影日と一致しないことがあります
- ログは補助用途であり、結果の完全性を保証するものではありません

リスクを下げるため、以下を推奨します。

1. 最初は少量のファイルでテストする
2. 検証時は `--mode copy` を優先する
3. 本番処理の前に重要データをバックアップする
4. 実行後にログと保存先フォルダを確認する

完全な免責説明については以下を参照してください。

- [免责声明.md](./免责声明.md)
