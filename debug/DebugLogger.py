from datetime import datetime

class DebugLogger:
    @staticmethod
    def Console(message, *args):
        time = datetime.now()
        print(f"| {time.hour}:{time.minute}:{time.second} | {message} {args}")