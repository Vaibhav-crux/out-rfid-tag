# app/ui/mainWindow/fetchDataFromFile.py

from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from app.config.refreshSession import create_session
from app.model.allotedTags import AllotedTags
from app.model.vehicleRegistration import VehicleRegistration
from app.model.vehicleInOut import VehicleInOut

def fetch_and_update_rfid(file_path, rfid_input_left, rfid_input_right, status_label, indicator_label, vehicle_info, window):
    """Fetches the RFID tag from the specified file and updates the provided text boxes."""
    rfid_tag = read_rfid_from_file(file_path)
    if rfid_tag:
        rfid_input_left.setText(rfid_tag)
        rfid_input_right.setText(rfid_tag)
        # After setting the RFID Tag, check its status in the AllotedTags table
        if not check_rfid_status_in_db(rfid_tag, status_label, indicator_label):
            # If RFID Tag is valid and not blacklisted, check in the VehicleRegistration table
            if check_vehicle_registration_in_db(rfid_tag, status_label, indicator_label, vehicle_info):
                # If vehicle is registered and validity is okay, check VehicleInOut table
                check_vehicle_in_out_status(rfid_tag, status_label, indicator_label, vehicle_info, window)

def read_rfid_from_file(file_path):
    """Reads the RFID tag from the specified file."""
    try:
        with open(file_path, "r") as file:
            return file.readline().strip()  # Read the first line and strip any extra whitespace
    except FileNotFoundError:
        print(f"RFID file not found: {file_path}")
        return ""

def check_rfid_status_in_db(rfid_tag, status_label, indicator_label):
    """Checks the RFID Tag in the AllotedTags table and updates the status label and indicator."""
    session = create_session()
    try:
        # Query the AllotedTags table for the given RFID Tag
        record = session.query(AllotedTags).filter_by(rfidTag=rfid_tag).one()
        
        if record.blacklisted:
            status_label.setText("Vehicle Blocked")
            indicator_label.setStyleSheet("background-color: red; border-radius: 10px;")
            return True  # RFID found and blocked
        else:
            status_label.setText("Vehicle Found")
            indicator_label.setStyleSheet("background-color: green; border-radius: 10px;")
            return False  # RFID found and not blocked
    except NoResultFound:
        status_label.setText("Vehicle not found")
        indicator_label.setStyleSheet("background-color: red; border-radius: 10px;")
        return True  # RFID not found
    finally:
        session.close()

def check_vehicle_registration_in_db(rfid_tag, status_label, indicator_label, vehicle_info):
    """Checks the RFID Tag in the VehicleRegistration table and populates the vehicle information."""
    session = create_session()
    try:
        # Query the VehicleRegistration table for the given RFID Tag
        record = session.query(VehicleRegistration).filter_by(rfidTag=rfid_tag).one()

        # Check if the ValidityTill date has expired
        current_date = datetime.utcnow().date()
        validity_till_date = datetime.strptime(record.validityTill, "%d/%m/%Y").date()  # Adjusted date format

        if validity_till_date < current_date:
            status_label.setText("Vehicle Validity Expire")
            indicator_label.setStyleSheet("background-color: red; border-radius: 10px;")
            return False  # RFID found but validity expired

        # Populate the vehicle information into the respective text boxes on the left and right forms
        vehicle_info['typeOfVehicleLeft'].setText(record.typeOfVehicle.name)
        vehicle_info['vehicleNumberLeft'].setText(record.vehicleNumber)
        vehicle_info['validityTillLeft'].setText(record.validityTill)

        # vehicle_info['typeOfVehicleRight'].setText(record.typeOfVehicle.name)
        # vehicle_info['vehicleNumberRight'].setText(record.vehicleNumber)
        # vehicle_info['doNumber'].setText(record.doNumber)
        vehicle_info['transporter'].setText(record.transporter)
        vehicle_info['driverOwner'].setText(record.driverOwner)
        vehicle_info['weighbridgeNo'].setText(record.weighbridgeNo)
        vehicle_info['visitPurpose'].setText(record.visitPurpose)
        vehicle_info['placeToVisit'].setText(record.placeToVisit)
        vehicle_info['personToVisit'].setText(record.personToVisit)
        vehicle_info['validityTillRight'].setText(record.validityTill)
        vehicle_info['section'].setText(record.section)

        # Update the status and indicator
        status_label.setText("Vehicle Registered")
        indicator_label.setStyleSheet("background-color: green; border-radius: 10px;")
        return True  # RFID found and validity is okay
    except NoResultFound:
        status_label.setText("Vehicle Not Registered")
        indicator_label.setStyleSheet("background-color: yellow; border-radius: 10px;")
        return False  # RFID not found in VehicleRegistration
    finally:
        session.close()

def check_vehicle_in_out_status(rfid_tag, status_label, indicator_label, vehicle_info, window):
    """Checks the RFID Tag in the VehicleInOut table to determine vehicle exit status and fetch weighbridge data."""
    session = create_session()
    try:
        # Query the VehicleInOut table for the latest entry for the given RFID Tag
        record = session.query(VehicleInOut).filter_by(rfidTag=rfid_tag).order_by(VehicleInOut.createdAt.desc()).first()

        if not record or not record.dateIn or not record.timeIn:
            # If no entry found or if dateIn and timeIn are not present, vehicle did not enter
            status_label.setText("Vehicle didn't enter")
            indicator_label.setStyleSheet("background-color: red; border-radius: 10px;")
            window.exit_button.setEnabled(False)  # Disable the button
        elif record.dateOut and record.timeOut:
            # If the record already has DateOut and TimeOut, it means the vehicle has already exited
            status_label.setText("Vehicle Already Out")
            indicator_label.setStyleSheet("background-color: red; border-radius: 10px;")
            window.exit_button.setEnabled(False)  # Disable the button
        else:
            # Populate the gross, tare, net, and challanNo fields if they are available
            if record.gross:
                vehicle_info['gross'].setText(str(record.gross))
            if record.tare:
                vehicle_info['tare'].setText(str(record.tare))
            if record.net:
                vehicle_info['net'].setText(str(record.net))
            if record.challanNo:
                vehicle_info['challanNo'].setText(record.challanNo)

            # Check if all required fields are present
            if record.gross and record.tare and record.net and record.challanNo:
                # If all required fields are present, allow the vehicle to exit
                status_label.setText("Allow Vehicle to Exit")
                indicator_label.setStyleSheet("background-color: green; border-radius: 10px;")
                window.exit_button.setEnabled(True)  # Enable the button
            else:
                # If any of these fields are empty, indicate that weighbridge data is incomplete
                status_label.setText("Weighbridge data incomplete")
                indicator_label.setStyleSheet("background-color: yellow; border-radius: 10px;")
                window.exit_button.setEnabled(False)  # Disable the button

    except Exception as e:
        status_label.setText("Error Handling Vehicle Exit")
        indicator_label.setStyleSheet("background-color: red; border-radius: 10px;")
        window.exit_button.setEnabled(False)  # Disable the button in case of error
        print(f"Error: {e}")
    finally:
        session.close()


def handle_exit_button_click(rfid_tag, vehicle_info, status_label, indicator_label, window):
    """Handles the exit button click event: save DateOut and TimeOut, clear text boxes, and disable the button."""
    if rfid_tag:
        session = create_session()
        try:
            # Query the VehicleInOut table for the latest entry for the given RFID Tag
            record = session.query(VehicleInOut).filter_by(rfidTag=rfid_tag).order_by(VehicleInOut.createdAt.desc()).first()

            if record and record.dateIn and record.timeIn:
                # Save the current date and time as DateOut and TimeOut
                record.dateOut = datetime.utcnow().strftime("%Y-%m-%d")
                record.timeOut = datetime.utcnow().strftime("%H:%M:%S")
                session.commit()

                # Clear all the text boxes
                for key, textbox in vehicle_info.items():
                    textbox.clear()
                
                window.rfid_input_left.clear()
                window.rfid_input_right.clear()

                # Disable the exit button until next RFID tag is entered
                window.exit_button.setEnabled(False)

                # Reset the status label and indicator
                status_label.setText("Waiting for next vehicle")
                indicator_label.setStyleSheet("background-color: grey; border-radius: 10px;")

                print("Exit data saved successfully!")

                # Clear the contents of the readVehicle.txt file
                with open("app/file/readVehicle.txt", "w") as file:
                    file.write("")  # Clear the file by writing an empty string
            else:
                print("No valid entry found for the provided RFID Tag.")
        except Exception as e:
            print(f"Error during saving exit data: {e}")
        finally:
            session.close()
    else:
        print("RFID Tag is missing or invalid.")
