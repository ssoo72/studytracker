from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
import collections
from sqlalchemy import func

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///study.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# モデルはここで1回だけ定義
class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    time = db.Column(db.Integer, nullable=False)
    studied_at = db.Column(db.Date, default=date.today, nullable=False)

# 初回テーブル作成
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    records = Record.query.order_by(Record.studied_at.desc()).all()
    total = sum(r.time for r in records)


    # --- デフォルトは直近7日間 ---
    start_date = date.today() - timedelta(days=6)
    end_date = date.today()

    # フォームから受け取ったら上書き
    if request.method == "POST":
        start_str = request.form.get("start_date")
        end_str = request.form.get("end_date")
        if start_str:
            try:
                start_date = datetime.strptime(start_str, "%Y-%m-%d").date() 
            except ValueError:
                pass  # 入力が不正なら無視
        if end_str:
            try:
                end_date = datetime.strptime(end_str, "%Y-%m-%d").date() 
            except ValueError:
                pass

    # データを期間で絞り込み
    records = Record.query.filter(
        Record.studied_at >= start_date,
        Record.studied_at <= end_date
    ).order_by(Record.studied_at.desc()).all()

    total = sum(r.time for r in records)

    # 科目別合計
    subject_totals = db.session.query(
        Record.subject, func.sum(Record.time)
    ).filter(
        Record.studied_at >= start_date,
        Record.studied_at <= end_date
    ).group_by(Record.subject).all()


    # 日別グラフ用
    days = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    by_day = {d: 0 for d in days}
    for r in records:
        if r.studied_at:  # None の場合はスキップ
            by_day[r.studied_at] += r.time
    labels = [d.strftime("%m/%d") for d in days]
    values = [by_day.get(d, 0) for d in days]

    return render_template("index.html",
        records=records, total=total, subject_totals=subject_totals,
        labels=labels, values=values,
        start_date=start_date, end_date=end_date
    )

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        subject = request.form["subject"]
        time = int(request.form["time"])
        date_str = request.form.get("studied_at")
        studied_at = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()

        record = Record(subject=subject, time=time, studied_at=studied_at)
        db.session.add(record)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    record = Record.query.get_or_404(id)
    if request.method == "POST":
        record.subject = request.form["subject"]
        record.time = int(request.form["time"])
        date_str = request.form.get("studied_at")
        record.studied_at = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else record.studied_at
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", record=record)

@app.route("/delete/<int:id>")
def delete(id):
    record = Record.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    # 二重実行防止のために use_reloader=False を付ける
    app.run(debug=True, use_reloader=False)
