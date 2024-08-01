from app import create_app
from datetime import datetime


app = create_app()

@app.template_filter('datetime')
def datetime_filter(timestamp):
    return datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')


app.jinja_env.filters['datetime'] = datetime_filter


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
