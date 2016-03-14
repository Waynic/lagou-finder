from flask import Flask, render_template, jsonify
from JobDB import Job

app = Flask(__name__)


def sa_obj_to_dict(obj):
    return {k: v for (k, v) in obj.__dict__.items() if not k.startswith('_')}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/jobs')
def jobs_json():
    jobs = [sa_obj_to_dict(j) for j in Job.query.all()]
    return jsonify(error=0, total=len(jobs), items=jobs)

if __name__ == '__main__':
    app.run(debug=False)
