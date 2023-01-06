from flask import Flask, jsonify, request

from entities import Permissions
from exceptions import ParkingException
from parking import Parking

parking_service = Parking()
app = Flask("Parking Service")


@app.route("/add_parking_nodes", methods=["POST"])
def add_parking_nodes():
    data = request.json
    result = parking_service.add_new_place(data)
    if isinstance(result, ParkingException):
        return jsonify({"success": False, "msg": str(result)}), 500
    return jsonify({"success": True, "msg": result}), 422


@app.route("/car_come")
def car_come():
    data = request.json
    number: str = data.get("car_number")
    permission: str | None = data.get("permission")
    if permission and not Permissions.has_value(permission):
        return jsonify({"success": False, "msg": "Invalid permission"}), 422

    result = parking_service.car_come(
        car_number=number, permission=Permissions(permission) if permission else None
    )
    if isinstance(result, ParkingException):
        return jsonify({"success": False, "msg": f"parking has no free place"}), 200
    return jsonify({"success": True, "msg": f"parking number is {result}"}), 200


@app.route("/car_leave")
def car_leave():
    data = request.json
    number: str = data.get("car_number")
    result = parking_service.car_leave(car_number=number)
    if isinstance(result, ParkingException):
        return jsonify({"success": False, "msg": str(result)}), 404
    return (
        jsonify({"success": True, "msg": f"parking place number {result} is free"}),
        200,
    )


@app.route("/get_empty_count")
def get_empty_count():
    return (
        jsonify(
            {"success": True, "msg": {"free_spots": parking_service.get_empty_count}}
        ),
        200,
    )


if __name__ == "__main__":
    app.run()
