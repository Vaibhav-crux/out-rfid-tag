from app.config.db_config import SessionLocal
from app.model.vehicleInOut import VehicleInOut
from datetime import datetime

def insert_vehicle_in_out_from_alloted_tag(alloted_tag):
    session = SessionLocal()
    try:
        # Fetch the latest entry for the given RFID Tag or Vehicle Number
        existing_entry = session.query(VehicleInOut).filter(
            (VehicleInOut.rfidTag == alloted_tag['rfidTag']) | 
            (VehicleInOut.vehicleNumber == alloted_tag['vehicleNumber'])
        ).order_by(VehicleInOut.createdAt.desc()).first()

        # Check if an existing entry is found
        if existing_entry:
            # Check if the vehicle has a valid 'dateIn' and 'timeIn'
            if existing_entry.dateIn and existing_entry.timeIn:
                # If 'dateOut' and 'timeOut' are not set, update them
                if not existing_entry.dateOut or not existing_entry.timeOut:
                    existing_entry.dateOut = datetime.now().strftime('%Y-%m-%d')
                    existing_entry.timeOut = datetime.now().strftime('%H:%M:%S')
                    
                    # Update Gross, Tare, Net, and Challan No
                    existing_entry.gross = alloted_tag.get('gross')
                    existing_entry.tare = alloted_tag.get('tare')
                    existing_entry.net = alloted_tag.get('net')
                    existing_entry.challanNo = alloted_tag.get('challanNo')

                    session.commit()
                    print(f"Vehicle marked as 'out' for RFID: {alloted_tag['rfidTag']}")
                    return "Vehicle Marked Out"
                else:
                    # Vehicle is already marked as 'out'
                    print("Vehicle already marked as 'out'. Cannot insert a new entry.")
                    return "Vehicle Already Out"
            else:
                # If no valid 'dateIn' and 'timeIn' are found
                print("Vehicle not 'In'. Cannot mark as 'out'.")
                return "Vehicle Not In"

        # If no existing entry is found, insert new data
        vehicle_in_out = VehicleInOut(
            rfidTag=alloted_tag['rfidTag'],
            typeOfVehicle=alloted_tag['typeOfVehicle'],
            vehicleNumber=alloted_tag['vehicleNumber'],
            doNumber=alloted_tag.get('doNumber'),
            transporter=alloted_tag.get('transporter'),
            driverOwner=alloted_tag.get('driverOwner'),
            weighbridgeNo=alloted_tag.get('weighbridgeNo'),
            visitPurpose=alloted_tag.get('visitPurpose'),
            placeToVisit=alloted_tag.get('placeToVisit'),
            personToVisit=alloted_tag.get('personToVisit'),
            validityTill=alloted_tag.get('validityTill'),
            section=alloted_tag.get('section'),
            dateIn=datetime.now().strftime('%Y-%m-%d'),
            timeIn=datetime.now().strftime('%H:%M:%S'),
            user=alloted_tag.get('user', ''),
            shift=alloted_tag.get('shift', ''),
            gross=alloted_tag.get('gross'),  # Save Gross
            tare=alloted_tag.get('tare'),    # Save Tare
            net=alloted_tag.get('net'),      # Save Net
            challanNo=alloted_tag.get('challanNo'),  # Save Challan No
            barrierStatus='CLOSED'
        )

        session.add(vehicle_in_out)
        session.commit()
        print(f"VehicleInOut entry added for RFID: {alloted_tag['rfidTag']}")
        return "Success"

    except Exception as e:
        session.rollback()
        print(f"Failed to insert VehicleInOut entry: {e}")
        return "Error"
    finally:
        session.close()
