import tkinter as tk
from tkinter import messagebox
import yagmail
import time
import threading
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
TRIG = 23  # Ultrasound projector
ECHO = 22  # Ultrasound Receiver
servoPIN_1 = 17  # Servo Motor 1
servoPIN_2 = 18  # Servo Motor 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN_1, GPIO.OUT)
GPIO.setup(servoPIN_2, GPIO.OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

servo1 = GPIO.PWM(servoPIN_1, 50)
servo2 = GPIO.PWM(servoPIN_2, 50)
servo1.start(2.5)
servo2.start(2.5)

def ultrasound_servo_control():
    global motion_detected
    motion_detected = 0
    while True:
        GPIO.output(TRIG, False)
        time.sleep(0.000002)
        GPIO.output(TRIG, True)
        time.sleep(0.00010)
        GPIO.output(TRIG, False)

        StartTime = time.time()
        StopTime = time.time()

        while GPIO.input(ECHO) == 0:
            StartTime = time.time()

        while GPIO.input(ECHO) == 1:
            StopTime = time.time()

        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2
        distance = int(distance)

        if(distance <= 20):
            if motion_start is None:
                motion_start = time.time()
            elif time.time() - motion_start >=0.50:
                motion_detected += 1
                if motion_detected % 3 == 0:
                    servo1.ChangeDutyCycle(12.5) #180 degrees
                    servo2.ChangeDutyCycle(12.5) #180 degrees
                    time.sleep(0.5)
                    servo1.ChangeDutyCycle(2.5) #0 degrees reset
                    servo2.ChangeDutyCycle(2.5) #0 degrees reset
                motion_start = None
            else:
                print("no motion detected, noice")
        else:
            motion_start = None
        
        time.sleep(0.1)

class Email:
    def __init__(self, root):
        self.root = root
        self.root.title("Dawg I'm really trying bro")
        self.root.geometry("500x500")

        self.label_email = tk.Label(root, text="Enter your email:")
        self.label_email.pack(pady=10)

        self.entry_email = tk.Entry(root)
        self.entry_email.pack(pady=5)

        self.submit_button = tk.Button(root, text="Submit", command=self.submit_email)
        self.submit_button.pack(pady=10)

    def submit_email(self):
        email = self.entry_email.get().strip()
        if not email:
            messagebox.showerror("Error", "Gimme your email smh.")
            return

        self.root.destroy()
        root = tk.Tk()
        Timer(root, email)
        root.mainloop()

class Timer:
    def __init__(self, root, email):
        self.root = root
        self.root.title("Dawg I'm really trying bro")
        self.root.geometry("500x500")

        self.user_email = email

        self.label_hours = tk.Label(root, text="Enter time in hours:")
        self.label_hours.pack(pady=5)
        self.entry_hours = tk.Entry(root)
        self.entry_hours.pack(pady=5)

        self.label_minutes = tk.Label(root, text="Enter time in minutes:")
        self.label_minutes.pack(pady=5)
        self.entry_minutes = tk.Entry(root)
        self.entry_minutes.pack(pady=5)

        self.label_seconds = tk.Label(root, text="Enter time in seconds:")
        self.label_seconds.pack(pady=5)
        self.entry_seconds = tk.Entry(root)
        self.entry_seconds.pack(pady=5)

        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(pady=5)
        self.pause_button = tk.Button(root, text="Pause", command=self.pause_resume, state=tk.DISABLED)
        self.pause_button.pack(pady=5)
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.label_timer = tk.Label(root, text="Time: 00:00:00", font=("Helvetica", 14))
        self.label_timer.pack(pady=10)

        self.timer_running = False
        self.paused = False
        self.remaining_time = 0
        self.total_time = 0

    def start_timer(self):
        if not self.timer_running:
            try:
                hours = int(self.entry_hours.get()) if self.entry_hours.get() else 0
                minutes = int(self.entry_minutes.get()) if self.entry_minutes.get() else 0
                seconds = int(self.entry_seconds.get()) if self.entry_seconds.get() else 0

                if self.remaining_time == 0:
                    self.remaining_time = (hours * 3600) + (minutes * 60) + seconds
                    self.total_time = self.remaining_time

                if self.remaining_time <= 0:
                    raise ValueError("I need you to be so fr, enter a real time.")

                self.timer_running = True
                self.paused = False
                self.pause_button.config(text="Pause", state=tk.NORMAL)
                self.stop_button.config(state=tk.NORMAL)
                self.update_timer()

            except ValueError as e:
                messagebox.showerror("Error", str(e))
                self.root.after(2000, self.root.destroy)

    def update_timer(self):
        if self.timer_running and not self.paused:
            if self.remaining_time <= 0:
                self.timer_running = False
                self.label_timer.configure(text="Freedom!")
                self.send_email()
                self.pause_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.DISABLED)
                self.root.after(2000, self.root.destroy)
            else:
                hrs, rem = divmod(self.remaining_time, 3600)
                mins, secs = divmod(rem, 60)
                self.label_timer.configure(text=f"Time remaining: {hrs:02}:{mins:02}:{secs:02}")
                self.remaining_time -= 1
                self.root.after(1000, self.update_timer)

    def pause_resume(self):
        if self.timer_running:
            if self.paused:
                self.paused = False
                self.pause_button.config(text="Pause")
                self.update_timer()
            else:
                self.paused = True
                self.pause_button.config(text="Resume")

    def stop_timer(self):
        self.timer_running = False
        self.paused = False
        self.remaining_time = 0
        self.label_timer.configure(text="Time: 00:00:00")
        self.pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)

    def send_email(self):
        yag_mail = yagmail.SMTP(user='aly2695@gmail.com', password="pwkn bpaz xbsz lnpp", host='smtp.gmail.com')

        hrs, rem = divmod(self.total_time, 3600)
        mins, secs = divmod(rem, 60)
        elapsed_time = f"{hrs:02}:{mins:02}:{secs:02}"

        Subject = "Extreme Study Buddy - Study Session Complete"
        Body = f"""
        Congrats!

        You spent this much time studying: {elapsed_time}
        """

        yag_mail.send(to=self.user_email, subject=Subject, contents=Body)
        print(f"Email has been sent successfully to {self.user_email} with the study time.")


#Servo/Ultrasound start
servo_thread = threading.Thread(target=ultrasound_servo_control, daemon=True)
servo_thread.start()

#GUI Timer start
email_root = tk.Tk()
app = Email(email_root)
email_root.mainloop()
