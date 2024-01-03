from flask import Blueprint, render_template

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def index():
    return render_template('index.html')


@index_bp.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@index_bp.route('/help', methods=['GET'])
def help():
    return render_template('help.html')


@index_bp.route('/tips', methods=['GET'])
def tips():
    return render_template('tips.html')


@index_bp.route('/law', methods=['GET'])
def law():
    return render_template('law.html')
