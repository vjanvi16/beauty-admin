from flask import Flask,request,flash,jsonify
from flask_mysqldb import MySQL 
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"*":{"origins":"*"}})
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bella'

mysql = MySQL(app)


@app.route("/")
def hello():
    return "Hello!"

@app.route("/api/products")
def get_products():
    cur = mysql.connection.cursor()
    # cur.execute("SELECT * FROM beauty")
    cur.execute("SELECT id, name, description, image_data FROM images")
    data = cur.fetchall()
    # cur.close()

    # return render_template('index.html',beauty=data)
    products = []
    for row in data:
        image_bytes = row[3]
        if image_bytes:
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            image_url = f"data:image/jpeg;base64,{image_base64}"
        else:
            image_url = None
        products.append({
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "image_data": image_url
        })

    return jsonify(products)


from flask import request
import base64

@app.route("/insert", methods=["POST"])
def insert():
    image_file = request.files.get("image")
    name = request.form.get("name")
    description = request.form.get("description")

    if not image_file:
        return jsonify({"error": "No image uploaded"}), 400

    image_binary = image_file.read()

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO images (image_name, name, description, image_data) VALUES (%s, %s, %s, %s)",
        (image_file.filename, name, description, image_binary)
    )
    mysql.connection.commit()

    return jsonify({"message": "Product added successfully"}), 200




# @app.route('/delete/<string:id_data>', methods = ['GET'])
# def delete(id_data):
#     flash("Record has been deleted successfully")
#     cur = mysql.connection.cursor()
#     cur.execute("DELETE FROM images WHERE id=%s",(id_data))
#     mysql.connection.commit()
#     return jsonify({"message": "deleted"})

@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM images WHERE id=%s", (id_data,))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "deleted"})



# @app.route("/update", methods=["POST"])
# def update():
#     id = request.form.get("id")
#     name = request.form.get("name")
#     description = request.form.get("description")

#     image_file = request.files.get("image")

#     cur = mysql.connection.cursor()

#     if image_file and image_file.filename != "":
#         image_data = image_file.read()
#         cur.execute("""
#             UPDATE beauty 
#             SET name=%s, description=%s, image=%s 
#             WHERE id=%s
#         """, (name, description, image_data, id))
#     else:
#         cur.execute("""
#             UPDATE images 
#             SET name=%s, description=%s 
#             WHERE id=%s
#         """, (name, description, id))

#     mysql.connection.commit()

#     return jsonify({"message": "Updated successfully"}), 200
@app.route('/update/<int:id>', methods=['POST'])
def update_product(id):
    name = request.form.get('name')
    description = request.form.get('description')
    file = request.files.get('image')

    cursor = mysql.connection.cursor()

    # If a new image was uploaded
    if file and file.filename != "":
        image_name = file.filename
        image_data = file.read()

        sql = """UPDATE images 
                 SET name=%s, description=%s, image_name=%s, image_data=%s
                 WHERE id=%s"""
        cursor.execute(sql, (name, description, image_name, image_data, id))

    else:
        # If no image selected, keep the old image
        sql = """UPDATE images 
                 SET name=%s, description=%s 
                 WHERE id=%s"""
        cursor.execute(sql, (name, description, id))

    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Updated successfully"})




if __name__ == "__main__":
    app.run(port=5000)













import mysql.connector

def insert_image_into_db(host, user, password, database, image_path, image_name):
    try:
        # Establish a database connection
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bella"
        )
        cursor = conn.cursor()

        # Read the image file in binary mode
        with open(image_path, 'rb') as file:
            binary_image_data = file.read()

        # Define the INSERT query
        sql = "INSERT INTO images (image_name, image_data) VALUES (%s, %s)"
            
        # Execute the query with the image data
        cursor.execute(sql, (image_name, binary_image_data))

        # Commit the changes to the database
        conn.commit()
        print(f"Image '{image_name}' successfully stored in the database.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and connection
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection closed.")

# Example usage:
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'bella'
}
    
image_file_path = 'C:/Users/Dell/Desktop/New folder/v.jpeg' # Replace with your image path
image_display_name = 'my_example_image.jpg' # Name to store in DB

insert_image_into_db(
    db_config['host'],
    db_config['user'],
    db_config['password'],
    db_config['database'],
    image_file_path,
    image_display_name
)











import mysql.connector
import os

def retrieve_image_from_db(host, user, password, database, image_name_to_retrieve, save_path):
    try:
        # Establish a database connection
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bella"
        )
        cursor = conn.cursor()

        # Define the SELECT query to fetch the specific image by name
        sql = "SELECT image_data FROM images WHERE image_name = %s"
            
        # Execute the query
        cursor.execute(sql, (image_name_to_retrieve,))

        # Fetch the result (assuming only one result for a unique name)
        result = cursor.fetchone()

        if result:
            binary_image_data = result[0]
            
            # Write the binary data back to a file in binary mode
            with open(save_path, 'wb') as file:
                file.write(binary_image_data)
            
            print(f"Image data successfully retrieved and saved to: {save_path}")
        else:
            print(f"Image '{image_name_to_retrieve}' not found in the database.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and connection
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection closed.")

# --- Example Usage ---

# (Make sure the insert_image_into_db function from your original code has run first)

db_config = {
    'host': 'localhost',
    'user': 'root', # Use your actual username
    'password': '', # Use your actual password
    'database': 'bella' # Use your actual database name
}

# The name you used when inserting the image
image_display_name = 'my_example_image.jpg' 

# The path where you want to save the retrieved image file
output_save_path = os.path.join(os.getcwd(), 'retrieved_image.jpg') 

# Run the retrieval function
retrieve_image_from_db(
    db_config['host'],
    db_config['user'],
    db_config['password'],
    db_config['database'],
    image_display_name,
    output_save_path
)
