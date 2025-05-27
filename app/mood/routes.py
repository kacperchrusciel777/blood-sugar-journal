from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.mood.forms import MoodForm, DeleteForm
from app.models import MoodEntry

bp = Blueprint('mood', __name__, url_prefix='/mood')

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_entry():
    form = MoodForm()
    if form.validate_on_submit():
        entry = MoodEntry(
            mood=form.mood.data,
            note=form.note.data,
            user_id=current_user.id
        )
        db.session.add(entry)
        db.session.commit()
        flash('Mood saved!')
        return redirect(url_for('mood.dashboard'))
    return render_template('mood/new.html', form=form)


@bp.route('/dashboard')
@login_required
def dashboard():
    entries = MoodEntry.query.filter_by(user_id=current_user.id).order_by(MoodEntry.timestamp.asc()).all()
    mood_data = [
        {"date": entry.timestamp.strftime('%Y-%m-%d'), "mood": entry.mood}
        for entry in entries
    ]
    delete_form = DeleteForm()
    return render_template('mood/dashboard.html', entries=entries, mood_data=mood_data, delete_form=delete_form)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_entry(id):
    entry = MoodEntry.query.get_or_404(id)
    if entry.user_id != current_user.id:
        flash('You do not have permission to edit this entry.', 'danger')
        return redirect(url_for('mood.dashboard'))
    
    form = MoodForm(obj=entry)  # wstępne wypełnienie formularza danymi z bazy
    
    if form.validate_on_submit():
        entry.mood = form.mood.data
        entry.note = form.note.data
        db.session.commit()
        flash('Mood entry updated successfully.', 'success')
        return redirect(url_for('mood.dashboard'))
    
    return render_template('mood/edit.html', form=form, entry=entry)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_entry(id):
    entry = MoodEntry.query.get_or_404(id)
    if entry.user_id != current_user.id:
        flash('You do not have permission to delete this entry.', 'danger')
        return redirect(url_for('mood.dashboard'))
    
    db.session.delete(entry)
    db.session.commit()
    flash('Mood entry deleted.', 'success')
    return redirect(url_for('mood.dashboard'))
