from src.web import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)  # Solo se ejecuta en desarrollo local (producción usa gunicorn)