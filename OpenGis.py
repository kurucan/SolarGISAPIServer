from flask import Flask, app,request
from pandas.core.arrays import string_
from flask_restful import Resource,Api
from pvGIs import getPredictions
app=Flask(__name__)
api=Api(app)

class GetSolarRadiance(Resource):
    
    def get(self):
        lat=float(request.args.get('lat'))
        lng=float(request.args.get('lng'))
        results=getPredictions(lat,lng)

        return results
    
api.add_resource(GetSolarRadiance,'/')

if __name__ == '__main__':
    app.run(debug=True)