from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.glucose.forms import GlucoseForm, DeleteForm, FilterDateForm
from app.models import GlucoseEntry
from datetime import datetime

bp = Blueprint('glucose', __name__, url_prefix='/glucose')

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_entry():
    form = GlucoseForm()
    if form.validate_on_submit():
        entry = GlucoseEntry(
            glucose=form.glucose.data,
            note=form.note.data,
            tag=form.tag.data,
            user_id=current_user.id
        )
        db.session.add(entry)
        db.session.commit()
        flash('Glucose level entry has been saved.', 'success')
        return redirect(url_for('glucose.dashboard'))
    return render_template('glucose/new.html', form=form)

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    filter_form = FilterDateForm(request.args)
    query = GlucoseEntry.query.filter_by(user_id=current_user.id)

    if filter_form.start_date.data:
        start_dt = datetime.combine(filter_form.start_date.data, datetime.min.time())
        query = query.filter(GlucoseEntry.timestamp >= start_dt)
    if filter_form.end_date.data:
        end_dt = datetime.combine(filter_form.end_date.data, datetime.max.time())
        query = query.filter(GlucoseEntry.timestamp <= end_dt)

    entries = query.order_by(GlucoseEntry.timestamp.asc()).all()

    glucose_data = [
        {"date": entry.timestamp.strftime('%Y-%m-%d'), "glucose": entry.glucose}
        for entry in entries
    ]

    avg_glucose = min_glucose = max_glucose = None
    if entries:
        values = [e.glucose for e in entries]
        avg_glucose = sum(values) / len(values)
        min_glucose = min(values)
        max_glucose = max(values)

    delete_form = DeleteForm()
    return render_template(
        'glucose/dashboard.html',
        entries=entries,
        glucose_data=glucose_data,
        delete_form=delete_form,
        filter_form=filter_form,
        avg_glucose=avg_glucose,
        min_glucose=min_glucose,
        max_glucose=max_glucose
    )

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_entry(id):
    entry = GlucoseEntry.query.get_or_404(id)
    if entry.user_id != current_user.id:
        flash('You do not have permission to edit this entry.', 'danger')
        return redirect(url_for('glucose.dashboard'))

    form = GlucoseForm(obj=entry)
    if form.validate_on_submit():
        entry.glucose = form.glucose.data
        entry.note = form.note.data
        entry.tag = form.tag.data
        db.session.commit()
        flash('Glucose level entry has been successfully updated.', 'info')
        return redirect(url_for('glucose.dashboard'))

    return render_template('glucose/edit.html', form=form, entry=entry)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_entry(id):
    entry = GlucoseEntry.query.get_or_404(id)
    if entry.user_id != current_user.id:
        flash('You do not have permission to delete this entry.', 'danger')
        return redirect(url_for('glucose.dashboard'))

    db.session.delete(entry)
    db.session.commit()
    flash('Glucose level entry has been deleted.', 'success')
    return redirect(url_for('glucose.dashboard'))
