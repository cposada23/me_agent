from tools.Pusher import Pusher

def main():
    # Initilize new Pusher instance
    pusher = Pusher()
    pusher.push_notification("test")


if __name__ == "__main__":
    main()
