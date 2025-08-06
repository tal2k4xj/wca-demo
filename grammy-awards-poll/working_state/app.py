from flask import Flask, render_template, redirect, request
import os
import psycopg2
from dotenv import load_dotenv
from typing import Any
from collections import defaultdict

app = Flask(__name__)


def get_poll_data() -> list[dict[str, Any]]:
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT c.name AS category_name,
                ch.id AS choice_id,
                ch.name AS choice_name
            FROM categories c
            JOIN choices ch ON c.id = ch.category_id
            ORDER BY c.id DESC, ch.id DESC;
            """
        )
        poll_data = cursor.fetchall()

    categories = defaultdict(list)
    for category_name, choice_id, choice_name in poll_data:
        categories[category_name].append({"id": choice_id, "name": choice_name})

    return [{"name": name, "choices": choices} for name, choices in categories.items()]


def get_result_data() -> list[dict[str, Any]]:
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT c.id AS category_id, c.name AS category_name, ch.id AS choice_id, ch.name AS choice_name, COUNT(v.id) AS num_votes FROM categories c JOIN choices ch ON c.id = ch.category_id LEFT JOIN votes v ON ch.id = v.choice_id GROUP BY c.id, c.name, ch.id, ch.name ORDER BY c.id DESC, ch.id DESC;"
        )
        result_data = cursor.fetchall()

    category_total_votes = defaultdict(int)
    for category_id, category_name, choice_id, choice_name, num_votes in result_data:
        category_total_votes[category_id] += num_votes

    result = defaultdict(list)
    for category_id, category_name, choice_id, choice_name, num_votes in result_data:
        percent = (
            num_votes / category_total_votes[category_id]
            if category_total_votes[category_id] != 0
            else 0
        )
        result[category_name].append(
            {"name": choice_name, "percent": int(percent * 100)}
        )

    return [{"name": name, "choices": choices} for name, choices in result.items()]


@app.route("/vote", methods=["POST"])
def vote():
    choice_id = int(request.form["choice"])
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO votes (choice_id) VALUES (%s)", (choice_id,))
    conn.commit()
    return redirect("/user")


@app.route("/user")
def user():
    categories = get_poll_data()
    return render_template("user.html", categories=categories)


@app.route("/host")
def host():
    categories = get_result_data()
    return render_template("host.html", categories=categories)


if __name__ == "__main__":
    global conn
    load_dotenv()

    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
    app.run(host="0.0.0.0", port=4321)
