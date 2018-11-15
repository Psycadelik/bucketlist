# app/__init__.py
import os
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

# local import 
from instance.config import app_config
from .models import db
from flask import request,jsonify,abort
#initialize sql-alchemy

migrate = Migrate()


def create_app(config_name='testing'):
	from .models import Bucketlist

	app = FlaskAPI(__name__, instance_relative_config=True)
	app.config.from_object(app_config[config_name])
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)
	from app import models 

	migrate.init_app(app, db)

	############ Work begins here #####
	### GET & POST ###
	@app.route('/bucketlists/',methods=['POST','GET'])
	def bucketlists():
		if request.method == "POST":
			name = str(request.data.get('name',''))
			if name:
				bucketlist = Bucketlist(name=name)
				bucketlist.save()
				response = jsonify({
					'id': bucketlist.id,
					'name': bucketlist.name,
					'date_created': bucketlist.date_created,
					'date_modified': bucketlist.date_modified
					})
				response.status_code = 201
				return response
		else:
			#GET
			bucketlists = Bucketlist.get_all()
			results = []

			for bucketlist in bucketlists:
				obj = {
					'id':bucketlist.id,
					'name': bucketlist.name,
					'date_created':bucketlist.date_created,
					'date_modified':bucketlist.date_modified
				}
				results.append(obj)
			response = jsonify(results)
			response.status_code = 200
			return response

	#### PUT & DELETE ###
	@app.route('/bucketlists/<int:id>', methods=['GET','PUT','DELETE'])
	def bucketlist_manipulation(id, **kwargs):
		#retrieve a bucketlist using it's ID
		bucketlist = Bucketlist.query.filter_by(id=id).first()
		if not bucketlist:
			# Raise an HTTPException with a 404 not found status code
			abort(404)

		if request.method == 'DELETE':
			bucketlist.delete()
			return {
			"message": "bucketlist {} deleted successfully".format(bucketlist.id)
			},200
		elif request.method == 'PUT':
			name = str(request.data.get('name',''))
			bucketlist.name = name
			bucketlist.save()
			response = jsonify({
				'id': bucketlist.id,
				'name': bucketlist.name,
				'date_created': bucketlist.date_created,
				'date_modified': bucketlist.date_modified
				})
			response.status_code = 200
			return response
		else:
			#GET
			response = jsonify({
				'id': bucketlist.id,
				'name': bucketlist.name,
				'date_created': bucketlist.date_created,
				'date_modified': bucketlist.date_modified
				})
			response.status_code = 200
			return response
	return app
