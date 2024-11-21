from screen_time_tracker import ScreenTimeTracker

def main():
    tracker = ScreenTimeTracker()
    try:
        tracker.start_tracking()
        tracker.tracker_thread.join()  # Allow thread to complete tracking if needed
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt received. Stopping tracker.")
        tracker.stop()  # Stop tracking immediately

if __name__ == "__main__":
    main()
