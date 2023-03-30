@app.route('/delete_inventory/<inventory_id>', methods=['DELETE'])
def delete_inventory(inventory_id):
    #the user input is gathered in JSON format
    try:
        for record in inventory_select():
            if record['inventory_id'] == int(inventory_id):
                delete_query = "DELETE FROM inventory WHERE id = %s" % (inventory_id)
                execute_query(conn,delete_query)
                return "Inventory was deleted Successfully"
    except Exception as e:
        return e

