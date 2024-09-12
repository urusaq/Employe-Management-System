import mysql.connector
from mysql.connector import Error
from prettytable import PrettyTable

# Database connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',  # Replace with your MySQL password
    'database': 'amdocs'
}


def connect_db():
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Connected to the database.")
            return connection
        else:
            print("Some error occured")
            return None


def close_db(connection):
    if connection.is_connected():
        connection.close()
        print("Database connection closed.")


def admin_login(cursor):
    email = input("Enter admin email: ")
    password = input("Enter password: ")
    cursor.execute("SELECT * FROM EMPLOYEE WHERE email = %s AND password = %s", (email, password))
    admin = cursor.fetchone()
    return admin


def employee_login(cursor):
    email = input("Enter employee username: ")
    password = input("Enter password: ")
    cursor.execute("SELECT * FROM EMPLOYEE WHERE email = %s AND password = %s",
                   (email, password))
    employee = cursor.fetchone()
    return employee


def register_employee(cursor, connection):
        fname = input("Employee First name : ")
        lname = input("Employee Last name : ")
        email = input("Enter employee email: ")
        doj = input("Enter DOJ : ")
        role = input("Enter employee position: ")

        insert_query = "INSERT INTO EMPLOYEE(first_name, last_name, email, DOJ, emp_role) VALUES(%s,%s,%s,%s,%s)"
        values = (fname, lname, email, doj, role)
        cursor.execute(insert_query,values)
        connection.commit()
        print("Employee registered successfully.")

        print("set password for %s ", (fname))
        password = input("Enter password: ")
        cursor.execute("SELECT LAST_INSERT_ID()")
        empId = cursor.fetchone()[0]
        cursor.execute("UPDATE EMPLOYEE SET password = %s WHERE id = %s " , (password,empId))
        connection.commit()
        print("Password set successfully!!")


def view_employee_details(cursor, id):
    cursor.execute("SELECT * FROM EMPLOYEE WHERE id = %s\n", (id,))
    employee = cursor.fetchone()

    if employee:
        table = PrettyTable()
        table.field_names = [i[0] for i in cursor.description]
        table.add_row(employee)

        print(table)
    else:
        print("Employee not found!!")


def update_employee_details(cursor, connection, empId):
    print("What do you want to update ?\n 1. Name \n 2. email \n 3. Change Password")
    choice = int(input("enter your choice : "))

    if choice == 1:
            fname = input("EMPLOYEE FIRST NAME : ")
            lname = input("EMPLOYEE LAST NAME : ")

            query = "UPDATE EMPLOYEE SET first_name = %s , last_name = %s WHERE id = %s"
            cursor.execute(query, (fname, lname, empId))
            connection.commit()
            print("Details updated successfully.")

    elif choice == 2:
            email = input("enter email : ")
            query = "UPDATE EMPLOYEE SET email = %s WHERE id = %s"
            cursor.execute(query, (email, empId))
            connection.commit()
    else:
        cursor.execute("SELECT password from EMPLOYEE WHERE id = %s", (empId,))
        oldpass = cursor.fetchone()[0]
        opass = input("Enter old password : ")
        if oldpass == opass:
            passwrd = input("Enter new password : ")
            cursor.execute("UPDATE EMPLOYEE SET password = %s WHERE id = %s", (passwrd,empId))
            connection.commit()
            print("Password updated successfully!!")
        else:
            print("Wrong Password!!")



def add_employee(cursor, connection):
        fname = input("EMPLOYEE FIRST NAME : ")
        lname = input("EMPLOYEE LAST NAME : ")
        emailId = input("EMAIL ID : ")
        doj = input("DATE OF JOINING (DOJ) : ")
        Role = input("ROLE : ")


        insert_query = "INSERT INTO EMPLOYEE(first_name, last_name, email, DOJ, emp_role) VALUES(%s, %s,%s,%s,%s)"
        values = (fname, lname, emailId, doj, Role)
        cursor.execute(insert_query, values)
        connection.commit()
        print("Employee added successfully.")



def delete_employee(cursor, connection):
        empId = input("Enter the Employee id of the employee to delete: ")
        view_employee_details(cursor,empId)
        print("Are you sure you want to delete ?(Y or N)")
        choice = input("Enter your choice: ")
        if choice == 'Y':
            cursor.execute("DELETE FROM EMPLOYEE WHERE id = %s", (empId,))
            connection.commit()
            print("Employee deleted successfully.")
        else:
            print("Data not deleted")


def main():
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        while True:
            print("\n1. Admin Login")
            print("2. Employee Login")
            print("3. Register as Employee")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                admin = admin_login(cursor)
                if admin:
                    print("\nAdmin logged in successfully.")
                    while True:
                        print("\n1. View Employees")
                        print("2. Add Employee")
                        print("3. Update Employee Details")
                        print("4. Delete Employee")
                        print("5. Logout")
                        admin_choice = input("Enter your choice: ")

                        if admin_choice == '1':
                            print("1. View all employee \n2. View employee by id")
                            ch = input("Enter your choice : ")
                            if ch == '1':
                                cursor.execute("SELECT * FROM EMPLOYEE")
                                employees = cursor.fetchall()
                                table = PrettyTable()
                                table.field_names = [i[0] for i in cursor.description]
                                for row in employees:
                                    table.add_row(row)

                                print(table)
                                # for emp in employees:
                                #     print(f"First Name: {emp[2]}, Last Name: {emp[3]}, Email: {emp[4]}, DOJ: {emp[5]},Role: {emp[6]}")
                                    # view_employee_details(cursor, empId)
                            else:
                                empId = int(input("Enter employee ID : "))
                                view_employee_details(cursor, empId)
                        elif admin_choice == '2':
                            add_employee(cursor, connection)
                        elif admin_choice == '3':
                            update_employee_details(cursor, connection, input("Enter employee id: "))
                        elif admin_choice == '4':
                            delete_employee(cursor, connection)
                        elif admin_choice == '5':
                            print("Admin logged out.")
                            break
                        else:
                            print("Invalid choice.")
                else:
                    print("Invalid admin credentials.")

            elif choice == '2':
                employee = employee_login(cursor)
                if employee:
                    print("\nEmployee logged in successfully.")
                    while True:
                        print("\n1. View Your Details")
                        print("2. Update Your Details")
                        print("3. Logout")
                        emp_choice = input("Enter your choice: ")

                        if emp_choice == '1':
                            view_employee_details(cursor, employee[0])
                        elif emp_choice == '2':
                            update_employee_details(cursor, connection, employee[0])
                        elif emp_choice == '3':
                            print("Employee logged out.")
                            break
                        else:
                            print("Invalid choice.")
                else:
                    print("Invalid employee credentials.")

            elif choice == '3':
                register_employee(cursor, connection)

            elif choice == '4':
                close_db(connection)
                break

            else:
                print("Invalid choice.")
    else:
        print("Failed to connect to the database.")


if __name__ == "__main__":
    main()
