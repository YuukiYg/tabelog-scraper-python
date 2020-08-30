# tabelog-scraper-python

食べログのURLから、お店の情報を抽出するプログラム。

## 使い方
1. インストール  
	`pip install requests`  
	`pip install beautifulsoup4`

2. 入力ファイル作成
	入力ファイルは、食べログのURLを1行ずつ列挙したテキストファイルである。下記は例。
	```
	https://tabelog.com/tokyo/A1301/A130103/13202360/
	https://tabelog.com/tokyo/A1301/A130102/13006215/
	https://tabelog.com/tokyo/A1301/A130102/13137968/
	```
3. 実行  
	`python tabelog_scraper.py input.txt`
