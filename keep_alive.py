try:
    from flask import Flask
    from threading import Thread
    
    app = Flask('')
    
    @app.route('/')
    def home():
        return "Estou vivo!"
    
    def run():
        app.run(host='0.0.0.0', port=8080)
    
    def keep_alive():
        t = Thread(target=run)
        t.start()

except ImportError:
    # Flask not available, provide a no-op keep_alive function
    def keep_alive():
        pass  # Silent when Flask is not available