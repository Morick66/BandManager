from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# 文件路径
file_path = 'inventory.json'

# 读取JSON文件
def load_inventory():
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# 保存数据到JSON文件
def save_inventory(inventory):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(inventory, f, indent=4, ensure_ascii=False)

# 获取库存项目
def get_inventory(item_type, style):
    inventory = load_inventory()
    for item in inventory:
        if item['item_type'] == item_type and item['style'] == style:
            return item
    return None

# 更新库存
def update_inventory(item, size, quantity, action):
    if action == '出售':
        item[size] = item.get(size, 0) - quantity
    elif action == '入库':
        item[size] = item.get(size, 0) + quantity

@app.route('/')
def index():
    inventories = load_inventory()
    return render_template('index.html', inventories=inventories)

@app.route('/add_movement', methods=['POST'])
def add_movement():
    action = request.form.get('action')
    size = request.form.get('size')
    quantity = int(request.form.get('quantity'))
    item_type = request.form.get('item_type')
    style = request.form.get('style')

    inventory = load_inventory()
    item = get_inventory(item_type, style)
    if item:
        update_inventory(item, size, quantity, action)
    else:
        new_item = {
            "item_type": item_type,
            "style": style,
            size: quantity if action == '入库' else -quantity
        }
        inventory.append(new_item)
    
    save_inventory(inventory)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
