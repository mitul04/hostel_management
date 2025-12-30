import tkinter as tk
import psycopg2

# Database connection parameters
db_params = {
    'dbname': 'hostel_mgmt',
    'user': 'postgres',
    'password': 'pass4096',
    'host': 'localhost',  # or your database server address
    'port': '5432'        # default PostgreSQL port
}
connection = psycopg2.connect(**db_params)
cursor = connection.cursor()

try:
    # Execute a simple SQL command
    cursor.execute("SELECT version();")

    # Fetch the result
    db_version = cursor.fetchone()
    print("PostgreSQL Database Version:", db_version)

    # Execute a simple SQL command
    cursor.execute("SELECT * FROM District;")

    # Fetch the result
    records = cursor.fetchall()
    for rec in records:
        print(rec)

except Exception as e:
    print("Error connecting to PostgreSQL:", e)

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if connection:
        connection.close()

#
#class MainApplication(tk.Tk):
#   def __init__(self):
    #    super().__init__()
    #    self.title("Organizing Panels with Classes")
    #    self.geometry("1200x900")
    #    self.bottom_panel = Panel1(self)
    #    self.bottom_panel.pack(padx=10, pady=10)

#class Panel1(tk.Frame):
#    def __init__(self, parent):
#        super().__init__(parent,width=1000, height=750)
#        self.pack_propagate(False)
#        self.config(bg="lightgreen")
#        # add your designs in this function


# create panels for each of the pages as classes and write the design inside __init__() function
# Main execution
#if __name__ == "__main__":
#    app = MainApplication()
#    app.mainloop()