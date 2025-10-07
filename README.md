Study Tracker
日々の学習内容を記録・可視化できるアプリケーション
デモサイト（Render）：https://studytracker.onrender.com

概要
Study Trackerは、学習時間を記録し、科目ごとの合計や期間別の学習量をグラフで確認できるFlaskアプリです。
「どの科目にどれくらい時間を使っているか」を可視化することで、学習のバランスを改善し、モチベーションの維持に役立てることを目的としています。

主な機能
・学習記録の追加・編集・削除　
　　科目・時間・日付を入力して登録可能
・期間指定フィルタ	
　　開始日・終了日を指定して学習履歴を絞り込み
・グラフ表示	
　　日ごとの合計学習時間を棒グラフで可視化（Chart.js使用）
・科目別集計	
　　科目ごとの合計学習時間を自動集計
・データ保存	
　　SQLiteを使用してローカルに保存
・Webデプロイ	
　　Renderにより無料で常時アクセス可能

使用技術
　バックエンド	Python / Flask / SQLAlchemy
　フロントエンド	HTML / CSS / Bootstrap / Chart.js
　データベース	SQLite（開発） 
　デプロイ	Render（Free Plan）
　その他	GitHub / VSCode

ディレクトリ構成
　studytracker/
　├── app.py                  #Flaskメインアプリ
　├── instance/
　│   └── study.db            #SQLiteデータベース
　├── templates/
　│   ├── base.html
　│   ├── index.html
　│   ├── add.html
　│   ├── edit.html
　│   ├── about.html
　├── static/
　│   ├── style.css
　│   └── chart.js
　├── requirements.txt
　├── runtime.txt
　├── Procfile
　└── README.md

環境構築手順
1. クローン
　git clone https://github.com/ssoo72/studytracker.git
　cd studytracker
2. 仮想環境セットアップ
　python -m venv venv
　source venv/bin/activate   #Windowsは venv\Scripts\activate
3. パッケージインストール
　pip install -r requirements.txt
4.ローカルで起動
　python app.py


