from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)

# Load inventory
def load_inventory():
    with open("data/inventory.json", "r") as f:
        return json.load(f)

# Save inventory
def save_inventory(data):
    with open("data/inventory.json", "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def index():
    items = load_inventory()
    return render_template("index.html", items=items)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    items = load_inventory()
    
    if request.method == "POST":
        item_id = int(request.form["id"])
        new_qty = int(request.form["quantity"])
        
        for item in items:
            if item["id"] == item_id:
                item["quantity"] = new_qty
        
        save_inventory(items)
        return redirect(url_for("admin"))

    # Expiry filter
    today = datetime.today()
    expiring_soon = [
        item for item in items 
        if (datetime.strptime(item["expiry"], "%Y-%m-%d") - today).days <= 5
    ]
    
    return render_template("admin.html", items=items, expiring_soon=expiring_soon)

if __name__ == "__main__":
    app.run(debug=True)