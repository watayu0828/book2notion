## 概要

Book2Notionは、Kindleでハイライトした文章を一括でNotionにインポートするデスクトップツールです。

## ダウンロード
[Release](https://github.com/watayu0828/book2notion/releases) から、環境にあったzipファイルをダウンロードし、PCの任意の場所に解凍してください。

## 初期設定

### 1. Book2Notion用のデータベースを複製

[専用データベース](https://www.notion.so/3d443390a32544e9825255cd6aa5010e?pvs=21)を自身のワークスペースに複製してください。

### 2. インテグレーションの作成とインテグレーショントークンを取得

NotionとBook2Notionを連携させるためのインテグレーショントークンを作成します。

[こちら](https://notion-lab.jp/2024-01-21-notion-integration-connect/#Notion%20%E3%82%A4%E3%83%B3%E3%83%86%E3%82%B0%E3%83%AC%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%82%92%E4%BD%9C%E6%88%90%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95)の記事を参考にインテグレーショントークンを作成してください。

ここで作成したインテグレーショントークン（secret_から始まる英数字）は、後の手順で使用します。

### 3. データベースとインテグレーションを接続

[こちら](https://notion-lab.jp/2024-01-21-notion-integration-connect/#%E4%BD%9C%E6%88%90%E3%81%97%E3%81%9F%E3%82%A4%E3%83%B3%E3%83%86%E3%82%B0%E3%83%AC%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%82%92%20Notion%20%E3%81%A8%E6%8E%A5%E7%B6%9A%EF%BC%88%E3%82%B3%E3%83%8D%E3%82%AF%E3%83%88%EF%BC%89%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95)の記事を参考にBook2Notionのデータベースと上記で作成したインテグレーションを接続してください。

### 4. 環境ファイルにインテグレーショントークンとデータベースIDを転記

`_internal`フォルダにある`.env` ファイルにインテグレーショントークンとデータベースIDを転記します。

```
TOKEN='secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
DATABASE_ID='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```

TOKENには、インテグレーション作成時に取得したインテグレーショントークン（secret_から始まる英数字）を貼り付けしてください。

DATABASE_IDには、複製したデータベースのURLからデータベースIDをコピーし、貼り付けてください。下記例の`{}` 内の文字列です。

`https://hoge.notion.site/{データベースID}?v=xxxxxxxxxxxxxxxx&pvs=4`

## 使い方

### 1. Kindleアプリからハイライトをエクスポート

Kindleアプリからハイライトのデータを出力します。

#### ① 「注釈」ページにあるエクスポートボタンをタップします

<img src="https://github.com/watayu0828/book2notion/assets/10852460/58fe3b34-fc51-46ee-b7a6-a5d3117d7ba1" width="30%" />

#### ② 「Eメール」をタップします

<img src="https://github.com/watayu0828/book2notion/assets/10852460/1556ba6a-f952-4022-b5aa-d0dcd8c58072" width="30%" />

#### ③ 「エクスポート」ボタンをタップして、自身のメールアドレス宛てにメールを送信します

<img src="https://github.com/watayu0828/book2notion/assets/10852460/b3640134-c6ec-411d-9692-1f194a71d7d7" width="30%" />

### 2. メールに添付されたデータをPCにダウンロード

<img src="https://github.com/watayu0828/book2notion/assets/10852460/575c910d-6474-441c-b5a8-d523f66e5e3c" width="80%" />

### 3. Book2Notionを実行し、エクスポートしたファイルを選択

`book2notion.py` を実行し、エクスポートしたファイルを選択します。

<img src="https://github.com/watayu0828/book2notion/assets/10852460/8666ca6a-655c-4428-ad8c-d2b5cee3c1e4" width="80%" />

インポートが完了すると、Notionにデータが追加されます。

<img src="https://github.com/watayu0828/book2notion/assets/10852460/6bc8a270-c48b-4509-a1d2-e488baa8fdc4" width="80%" />

## Licence

[MIT](LICENSE)

## サポート

Book2Notionはフリーソフトですが、応援・寄付歓迎です。

活動の励みになりますので、応援よろしくお願いします！🙌

<a href="https://www.buymeacoffee.com/watayu0828" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
