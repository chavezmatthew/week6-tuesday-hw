from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from connection import connection, Error


app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    member_name = fields.String(required = True)
    email = fields.String()
    phone = fields.String()

    class Meta:
        fields = ("member_name", "email", "phone")

member_schema = MemberSchema()
members_schema = MemberSchema(many = True)

class WorkoutSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    workout_date = fields.String(required = True)
    member_id = fields.Int()

    class Meta:
        fields = ("workout_date", "member_id")

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many = True)


@app.route('/')
def home():
    return r'''
    <pre>
_ _ _ ____ _    ____ ____ _  _ ____    ___ ____    ___ _  _ ____    _ _ _ ____ ____ _  _ ____ _  _ ___    ____ ___  ___    /
| | | |___ |    |    |  | |\/| |___     |  |  |     |  |__| |___    | | | |  | |__/ |_/  |  | |  |  |     |__| |__] |__]  /
|_|_| |___ |___ |___ |__| |  | |___     |  |__|     |  |  | |___    |_|_| |__| |  \ | \_ |__| |__|  |     |  | |    |    .
    </pre>
    '''

@app.route('/members', methods = ['GET'])
def get_members():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary = True)
            query = "SELECT * FROM members;"
            cursor.execute(query)
            members = cursor.fetchall()

        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return members_schema.jsonify(members)

@app.route("/members/<int:id>", methods = ['GET'])
def get_member(id):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM members WHERE id = %s"
            cursor.execute(query, (id,))
            member = cursor.fetchone()
            if not member:
                return jsonify({"error": "Member not found"}), 404
            return member_schema.jsonify(member)
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500

@app.route("/members", methods = ["POST"])
def add_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    conn = connection ()
    if conn is not None:
        try:
            cursor = conn.cursor()

            new_member = (member_data["member_name"], member_data["email"], member_data["phone"])

            query = "INSERT INTO members (member_name, email, phone) VALUES (%s, %s, %s)"

            cursor.execute(query, new_member)
            conn.commit()

            return jsonify({"Message": "New member added successfully!"}), 200
        
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"Error":"Database connection failed"}), 500
    
@app.route("/members/<int:id>", methods = ["PUT"])
def update_member(id):
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            check_query = "SELECT * FROM members WHERE id = %s"
            cursor.execute(check_query, (id,))
            member = cursor.fetchone()
            if not member:
                return jsonify ({"Error": "Member was not found."}), 404
            
            updated_member = (member_data["member_name"], member_data["email"], member_data["phone"], id)

            query = "UPDATE members SET member_name = %s, email = %s, phone = %s WHERE id = %s"

            cursor.execute(query, updated_member)
            conn.commit()

            return jsonify({"Message": f"Successfully updated member {id}"}), 200
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"Error": "Database connection failed."}), 500
    

@app.route("/members/<int:id>", methods = ['DELETE'])
def delete_member(id):
    
    conn = connection()
    
    if conn is not None:
        try:
            cursor = conn.cursor()

            check_query = "SELECT * FROM members WHERE id = %s"
            cursor.execute(check_query, (id,))
            member = cursor.fetchone()
            if not member:
                return jsonify({"Error": "Member not found"})
            
            query = "DELETE FROM members WHERE id = %s"
            cursor.execute(query, (id,))
            conn.commit()

            return jsonify({"Message": f"Member {id} was successfully deleted!"})
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"Error": "Database connection failed"}), 500


@app.route('/workouts', methods = ['GET'])
def get_workouts():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary = True)
            query = "SELECT * FROM workouts;"
            cursor.execute(query)
            workouts = cursor.fetchall()

        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return workouts_schema.jsonify(workouts)

@app.route("/workouts/<int:id>", methods = ['GET'])
def get_workout(id):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM workouts WHERE id = %s"
            cursor.execute(query, (id,))
            workout = cursor.fetchone()
            if not workout:
                return jsonify({"error": "Workout not found"}), 404
            return workout_schema.jsonify(workout)
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500

@app.route("/member/workouts/<int:id>", methods = ['GET'])
def get_member_workouts(id):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM workouts WHERE member_id = %s"
            cursor.execute(query, (id,))
            workouts = cursor.fetchall()
            if not workouts:
                return jsonify({"error": "Workouts not found"}), 404
            return workouts_schema.jsonify(workouts)
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500

@app.route("/workouts", methods = ["POST"])
def add_workout():
    try:
        workout_data = workout_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    conn = connection ()
    if conn is not None:
        try:
            cursor = conn.cursor()

            new_workout = (workout_data["workout_date"], workout_data["member_id"])

            query = "INSERT INTO workouts (workout_date, member_id) VALUES (%s, %s)"

            cursor.execute(query, new_workout)
            conn.commit()

            return jsonify({"Message": "New workout added successfully!"}), 200
        
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"Error":"Database connection failed"}), 500
    
@app.route("/workouts/<int:id>", methods = ["PUT"])
def update_workout(id):
    try:
        workout_data = workout_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            check_query = "SELECT * FROM workouts WHERE id = %s"
            cursor.execute(check_query, (id,))
            workout = cursor.fetchone()
            if not workout:
                return jsonify ({"Error": "Workout was not found."}), 404
            
            updated_workout = (workout_data["workout_date"], workout_data["member_id"], id)

            query = "UPDATE workouts SET workout_date = %s, member_id = %s WHERE id = %s"

            cursor.execute(query, updated_workout)
            conn.commit()

            return jsonify({"Message": f"Successfully updated workout {id}"}), 200
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"Error": "Database connection failed."}), 500
    

@app.route("/workouts/<int:id>", methods = ['DELETE'])
def delete_workout(id):
    
    conn = connection()
    
    if conn is not None:
        try:
            cursor = conn.cursor()

            check_query = "SELECT * FROM workouts WHERE id = %s"
            cursor.execute(check_query, (id,))
            workout = cursor.fetchone()
            if not workout:
                return jsonify({"Error": "Workout not found"})
            
            query = "DELETE FROM workouts WHERE id = %s"
            cursor.execute(query, (id,))
            conn.commit()

            return jsonify({"Message": f"Workout {id} was successfully deleted!"})
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"Error": "Database connection failed"}), 500



if __name__ == "__main__":
    app.run(debug=True)

