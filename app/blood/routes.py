from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.blood.forms import BloodForm, DeleteForm
from app.models import BloodEntry

bp = Blueprint('blood', __name__, url_prefix='/blood')

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_entry():
    form = BloodForm()
    if form.validate_on_submit():
        entry = BloodEntry(
            blood=form.blood.data,
            note=form.note.data,
            user_id=current_user.id
        )
        db.session.add(entry)
        db.session.commit()
        flash('Wpis poziomu krwi został zapisany.', 'success')
        return redirect(url_for('blood.dashboard'))
    return render_template('blood/new.html', form=form)

@bp.route('/dashboard')
@login_required
def dashboard():
    entries = BloodEntry.query.filter_by(user_id=current_user.id).order_by(BloodEntry.timestamp.asc()).all()
    blood_data = [
        {"date": entry.timestamp.strftime('%Y-%m-%d'), "blood": entry.blood}
        for entry in entries
    ]
    delete_form = DeleteForm()
    return render_template('blood/dashboard.html', entries=entries, blood_data=blood_data, delete_form=delete_form)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_entry(id):
    entry = BloodEntry.query.get_or_404(id)
    if entry.user_id != current_user.id:
        flash('Nie masz uprawnień do edycji tego wpisu.', 'danger')
        return redirect(url_for('blood.dashboard'))
    
    form = BloodForm(obj=entry)
    
    if form.validate_on_submit():
        entry.blood = form.blood.data
        entry.note = form.note.data
        db.session.commit()
        flash('Wpis poziomu krwi został pomyślnie zaktualizowany.', 'info')
        return redirect(url_for('blood.dashboard'))
    
    return render_template('blood/edit.html', form=form, entry=entry)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_entry(id):
    entry = BloodEntry.query.get_or_404(id)
    if entry.user_id != current_user.id:
        flash('Nie masz uprawnień do usunięcia tego wpisu.', 'danger')
        return redirect(url_for('blood.dashboard'))
    
    db.session.delete(entry)
    db.session.commit()
    flash('Wpis poziomu krwi został usunięty.', 'danger')
    return redirect(url_for('blood.dashboard'))
