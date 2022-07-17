from flask import Flask, Response, render_template, request
from get_jobs import get_jobs

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('./index.html')


jobs = []


@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    search = request.args.get('search')
    jobs = get_jobs(search)
    jobs_cnt = len(jobs)
    return render_template('./jobs.html', search=search, jobs=jobs, jobs_cnt=jobs_cnt)


@app.route('/jobs_to_csv/<search>', methods=['GET'])
def export_jobs(search):
    jobs = get_jobs(search)
    csv_header = 'title,company,link\n'
    csv_contents = []
    for job in jobs:
        content = f"{job['title']},{job['company']},{job['link']}"
        csv_contents.append(content)
    csv_text = csv_header + '\n'.join(csv_contents)
    return Response(csv_text, mimetype="text/csv", headers={"Content-disposition": "attachment; filename=jobs.csv"})


app.run(host="0.0.0.0")
