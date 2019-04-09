from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from hangman.auth import login_required
from hangman.db import get_db

bp = Blueprint('game', __name__)

@bp.route('/')
def index():
    # Implement use case 5.
    db = get_db()
    games = db.execute(
        'SELECT g.id, word, created, player_id, username'
        ' FROM game g JOIN user u ON g.player_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('game/index.html', games=games)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    # Implement use case 1.
    if request.method == 'POST':
        word = request.form['word']
        error = None

        if not word:
            error = 'A word is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO game (word, player_id)'
                ' VALUES (?, ?)',
                (word, g.user['id'])
            )
            db.commit()
            return redirect(url_for('game.index'))

    return render_template('game/create.html')


def get_post(id, check_player=True):
    # Implement use case 4.
    post = get_db().execute(
        'SELECT g.id, word, created, player_id, username'
        ' FROM game g JOIN user u ON g.id = u.id'
        ' WHERE g.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Game id {0} doesn't exist.".format(id))

    if check_player and post['player_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    # Implement use case 2.
    game = get_post(id)

    if request.method == 'POST':
        word = request.form['word']
        error = None

        if not word:
            error = 'A word is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE game SET word = ?'
                ' WHERE id = ?',
                (game, id)
            )
            db.commit()
            return redirect(url_for('game.index'))

    return render_template('game/update.html', game=game)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    # Implement use case 3.
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM word WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('game.index'))
