import time
import os
from pygame import mixer
import keyboard  # New import for keypress detection

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def timer(minutes, label, audio_file):
    seconds = minutes * 60
    start_time = time.time()
    while seconds > 0:
        if keyboard.is_pressed('q'):  # Check if 'q' is pressed to quit
            print("\nTimer stopped by user.")
            return False  # Signal to stop the session
        mins, secs = divmod(seconds, 60)
        time_display = f"{label}: {mins:02d}:{secs:02d} (Press 'q' to quit)"
        clear_screen()
        print(time_display)
        time.sleep(1)
        elapsed = time.time() - start_time
        seconds = int(minutes * 60 - elapsed)  # Adjust for real elapsed time
    clear_screen()
    print(f"{label} complete!")
    try:
        mixer.init()
        mixer.music.load(audio_file)
        mixer.music.play()
        time.sleep(2)
    except Exception as e:
        print(f"Could not play sound: {e}")
    return True  # Timer completed normally

def get_positive_int(prompt, default):
    while True:
        try:
            value = input(prompt + f" (default {default}): ") or default
            value = int(value)
            if value > 0:
                return value
            print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_settings():
    settings = {
        "work_time": 25,
        "short_break": 5,
        "long_break": 15,
        "total_cycles": 4,
        "audio_file": "alert.mp3"
    }
    while True:
        clear_screen()
        print("Current Settings:")
        print(f"1. Work period: {settings['work_time']} minutes")
        print(f"2. Short break: {settings['short_break']} minutes")
        print(f"3. Long break: {settings['long_break']} minutes")
        print(f"4. Total cycles: {settings['total_cycles']}")
        print(f"5. Audio file: {settings['audio_file']}")
        print("\nOptions:")
        print("1-5: Modify a setting")
        print("s: Start with these settings")
        print("q: Quit")

        choice = input("\nEnter your choice: ").lower()
        if choice == 's':
            return settings
        elif choice == 'q':
            print("Goodbye!")
            exit()
        elif choice == '1':
            settings['work_time'] = get_positive_int("Work period", settings['work_time'])
        elif choice == '2':
            settings['short_break'] = get_positive_int("Short break", settings['short_break'])
        elif choice == '3':
            settings['long_break'] = get_positive_int("Long break", settings['long_break'])
        elif choice == '4':
            settings['total_cycles'] = get_positive_int("Total cycles", settings['total_cycles'])
        elif choice == '5':
            settings['audio_file'] = input("Enter audio file name (e.g., alert.mp3): ") or settings['audio_file']
        else:
            print("Invalid choice. Try again.")
            time.sleep(1)

def pomodoro_cycle(work_time, short_break, long_break, total_cycles, audio_file):
    cycles = 0
    while cycles < total_cycles:
        cycles += 1
        print(f"\nCycle {cycles} of {total_cycles}")
        if not timer(work_time, "Work Time", audio_file):
            break  # Exit if timer was stopped
        if cycles % 4 == 0 and cycles < total_cycles:
            print("Time for a long break!")
            if not timer(long_break, "Long Break", audio_file):
                break
        elif cycles < total_cycles:
            print("Time for a short break!")
            if not timer(short_break, "Short Break", audio_file):
                break
    completed_cycles = cycles if cycles == total_cycles else cycles - 1
    print(f"\nPomodoro session ended. You completed {completed_cycles} of {total_cycles} cycles.")

if __name__ == "__main__":
    print("Welcome to the Pomodoro Timer!")
    settings = get_settings()
    print("\nStarting with:")
    print(f"Work = {settings['work_time']} min, Short Break = {settings['short_break']} min, Long Break = {settings['long_break']} min")
    print(f"Total cycles: {settings['total_cycles']}, Audio: {settings['audio_file']}")
    input("Press Enter to start...")
    pomodoro_cycle(settings['work_time'], settings['short_break'], settings['long_break'], settings['total_cycles'], settings['audio_file'])
