from flask import render_template, request
from flask_login import current_user

from bluehire.models import Job
from . import main_bp


@main_bp.route("/")
def index():
    q = request.args.get("q", "")
    location = request.args.get("location", "")
    category = request.args.get("category", "")

    jobs_query = Job.query
    if q:
        like = f"%{q}%"
        jobs_query = jobs_query.filter(Job.title.ilike(like) | Job.skills_required.ilike(like))
    if location:
        jobs_query = jobs_query.filter(Job.location.ilike(f"%{location}%"))
    if category:
        jobs_query = jobs_query.filter(Job.category.ilike(f"%{category}%"))

    jobs = jobs_query.order_by(Job.created_at.desc()).limit(20).all()

    return render_template("index.html", jobs=jobs, q=q, location=location, category=category, user=current_user)


