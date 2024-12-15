#1: Import libraries need for the test
from application.models import Entry,Prediction
import datetime as datetime
import pytest
from flask import json
#Unit Test
#2: Parametrize section contains the data for the test
# Unexpected Failure Testing For Prediction
@pytest.mark.parametrize("predictionlist",[
[ 150, 1.3, 'A1', 15456, 2017, 53.8, 12567.24], #Test integer, float and string arguments
[ 20, 2.0, 'A6', 36240, 2016, 64.2, 16548.89] 
])
#3: Write the test function pass in the arguments
def test_PredictionClass(predictionlist,capsys):
    with capsys.disabled():
        print(predictionlist)
        now = datetime.datetime.now(datetime.UTC)
        new_entry = Prediction( tax= predictionlist[0],
                engine_size = predictionlist[1],
                model= predictionlist[2],
                mileage = predictionlist[3],
                year = predictionlist[4],
                mpg = predictionlist[5],
                prediction = predictionlist[6],
                predicted_on= now)
        assert new_entry.tax == predictionlist[0]
        assert new_entry.engine_size == predictionlist[1]
        assert new_entry.model == predictionlist[2]
        assert new_entry.mileage == predictionlist[3]
        assert new_entry.year == predictionlist[4]
        assert new_entry.mpg == predictionlist[5]
        assert new_entry.prediction == predictionlist[6]
        assert new_entry.predicted_on == now


# Unexpected Failure Testing For User Entry
@pytest.mark.parametrize("entrylist",[
['test@gmail.com','password123'], #Test String arguments
['aiman.21@ichat.sp.edu.sg','abcd']
])
#3: Write the test function pass in the arguments
def test_EntryClass(entrylist,capsys):
    with capsys.disabled():
        print(entrylist)

        new_entry = Entry( email= entrylist[0],
                password = entrylist[1])
        assert new_entry.email == entrylist[0]
        assert new_entry.password == entrylist[1]
      
#4: Expected Failure Testing
# What if input contains 0 or negative values
# What if output is negative
@pytest.mark.xfail(reason="arguments <= 0")
@pytest.mark.parametrize("predictionlist",[
 [ 0, 1.3, 'A1', 15456, 2017, 53.8, 12567.24], 
 [ 20, -1.4, 'A6', 36240, 2016, 64.2, 16548.89],
 [ 150, 1.3, 'A1', -14230, 2017, 53.8, 12567.24], 
 [ 20, 2.0, 'A6', 36240, 0, 64.2, 16548.89],
 [ 150, 1.3, 'A1', 15456, 2017, -43.6, 12567.24], 
 [ 20, 2.0, 'A6', 36240, 2016, 64.2, -16548.89] 
 ])
def test_PredictionValidation_Negative_0(predictionlist, capsys):
     test_PredictionClass(predictionlist, capsys)

# Range testing
# What if input is in/out of range
@pytest.mark.xfail(reason="Out of range")
@pytest.mark.parametrize("predictionlist",[
 [ 0, 0.0, 'A1', 1, 1997, 18.9, 12567.24], 
 [ 580, 6.3, 'A6', 323000, 2020, 188.3, 16548.89],
 [ -1, -0.1, 'A1', 0, 1996, 18.8, 12567.24],
 [ 581, 6.4, 'A6', 323001, 2021, 188.4, 16548.89] 
 ])
def test_PredictionValidation_RangeTest(predictionlist, capsys):
     tax = predictionlist[0]
     engine_size = predictionlist[1]
     mileage = predictionlist[3]
     year = predictionlist[4]
     mpg = predictionlist[5]
     assert  0 <= tax <= 580, f"Tax not within the range 0 to 580"
     assert  0.0 <= engine_size <= 6.3, f"Engine size not within the range 0 to 6.3"
     assert  1 <= mileage <= 323000,f"Mileage not within the range 1 to 323000"
     assert  1997 <= year <= 2020,f"year not within the range 1997 to 2020"
     assert  18.9 <= mpg <= 188.3,f"mpg not within the range 18.9 to 188.3"

     test_PredictionClass(predictionlist, capsys)

# Validity Testing
# Check if car model is valid 
@pytest.mark.xfail(reason="Invalid car model")
@pytest.mark.parametrize("predictionlist",[
 [ 150, 1.3, 'AC1', 15456, 2017, 53.8, 12567.24], 
 [ 20, 2.0, 'B4', 36240, 2016, 64.2, 16548.89] 
 ])
def test_PredictionValidation_CarModel(predictionlist, capsys):
     test_PredictionClass(predictionlist, capsys)

# @pytest.mark.xfail(reason="Invalid Year Range")
# @pytest.mark.parametrize("predictionlist",[
#  [ 150, 1.3, 'A1', 15456, 1996, 53.8, 12567.24],
#  [ 20, 2.0, 'A6', 36240, 2021, 64.2, 16548.89],
#  [ 150, 1.3, 'A1', 15456, 0, 53.8, 12567.24] 
#  ])
# def test_PredictionValidation_Year(predictionlist, capsys):
#      test_PredictionClass(predictionlist, capsys)


# Validity Test 
# What if input is not an email 
@pytest.mark.xfail(reason="Invalid email")
@pytest.mark.parametrize("entrylist",[
 [ 'aiman','password123'], 
 [ 10, 'abcd'] 
 ])
def test_EntryValidation_Email(entrylist, capsys):
     test_EntryClass(entrylist, capsys)

# Validity Test
# What if input is empty
@pytest.mark.xfail(reason="Invalid password")
@pytest.mark.parametrize("entrylist",[
 [ 'aiman@gmail.com',''] 
 
 ])
def test_EntryValidation_PW(entrylist, capsys):
     test_EntryClass(entrylist, capsys)


#5: Test add API
# Unit testing for adding entry
@pytest.mark.parametrize("predictionlist",[
 [ 150, 1.3, 'A1', 15456, 2017, 53.8, 12567.24], #Test integer arguments
 [ 20, 2.0, 'A6', 36240, 2016, 64.2, 16548.89]
 ])
def test_addAPI(client,predictionlist,capsys):
     with capsys.disabled():
     #prepare the data into a dictionary
         data1 = { 'tax': predictionlist[0],
         'engine_size' :  predictionlist[1],
         'model':  predictionlist[2],
         'mileage' :  predictionlist[3],
         'year' :  predictionlist[4],
         'mpg' : predictionlist[5],
         'prediction' :  predictionlist[6]}
         #use client object to post
         #data is converted to json
         #posting content is specified
         response = client.post('/api/add',
         data=json.dumps(data1),
         content_type="application/json",)
         #check the outcome of the action
         assert response.status_code == 200
         assert response.headers["Content-Type"] == "application/json"
         response_body = json.loads(response.get_data(as_text=True))
         assert response_body["id"]


#Test get API
# Unit Testing for Retrieving Entry
@pytest.mark.parametrize("predictionlist",[
[ 3, 'aiman.21@ichat.sp.edu.sg', 132, 1.3, 'A2', 14234,2018,55.4,22188.14]
])
def test_getAPI(client, predictionlist, capsys):
    with capsys.disabled():
        response = client.get(f'/api/get/{predictionlist[0]}')
        ret = json.loads(response.get_data(as_text=True))
        #check the outcome of the action
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        response_body = json.loads(response.get_data(   as_text=True))
        assert response_body["id"] == predictionlist[0]
      #  assert response_body["email"] == (predictionlist[1])
        assert response_body["tax"] == (predictionlist[2])
        assert response_body["engine_size"] == (predictionlist[3])
        assert response_body["model"] == (predictionlist[4])
        assert response_body["mileage"] == (predictionlist[5])
        assert response_body["year"] == (predictionlist[6])
        assert response_body["mpg"] == (predictionlist[7])
        assert response_body["prediction"] == (predictionlist[8])
        with pytest.raises(KeyError):
             _ = response_body["email"]




#Test delete API
# Unit testing for deleting entry
@pytest.mark.parametrize ("predictionlist", [ [  134, 1.4, 'A1', 12345,2018,53.0,22542.66]
])
def test_deleteAPI (client, predictionlist, capsys): 
    with capsys.disabled():
        #prepare the data into a dictionary
        data1 = { 'tax': predictionlist[0],
        'engine_size' :  predictionlist[1],
        'model':  predictionlist[2],
        'mileage' :  predictionlist[3],
        'year' :  predictionlist[4],
        'mpg' : predictionlist[5],
        'prediction' :  predictionlist[6]}
        #use client object to post data & converted to json 
        response = client.post('/api/add', data=json.dumps (data1),content_type="application/json",)
        response_body= json. loads (response.get_data (as_text=True)) 
        assert response_body["id"]
        id = response_body["id"]
        response2 = client.get(f'/api/delete/{id}')
        ret = json.loads (response2.get_data (as_text=True))
        #check the outcome of the action
        assert response2.status_code == 200
        assert response2.headers["Content-Type"] == "application/json"
        response2_body = json. loads (response2.get_data(as_text=True))
        assert response2_body ["result"] == "ok"

# Unit testing for adding entry
#5: Test add API
@pytest.mark.parametrize("entrylist",[
 ['test@gmail.com','password123'], #Test integer arguments
 ['aiman.21@ichat.sp.edu.sg','abcd']
 ])
def test_addAPIuser(client,entrylist,capsys):
     with capsys.disabled():
         #prepare the data into a dictionary
         data1 = { 'email': entrylist[0],
         'password' : entrylist[1]}
         #use client object to post
         #data is converted to json
         #posting content is specified
         response = client.post('/api/addu',
         data=json.dumps(data1),
         content_type="application/json",)
         #check the outcome of the action
         assert response.status_code == 200
         assert response.headers["Content-Type"] == "application/json"
         response_body = json.loads(response.get_data(as_text=True))
         assert response_body["id"]

# Unit testing for retrieving entry
@pytest.mark.parametrize("entrylist",[
[ 4, 'test@gmail.com','password123']
])
def test_getuserAPI(client, entrylist, capsys):
    with capsys.disabled():
        response = client.get(f'/api/getuser/{entrylist[0]}')
        ret = json.loads(response.get_data(as_text=True))
        #check the outcome of the action
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        response_body = json.loads(response.get_data(   as_text=True))
        assert response_body["id"] == entrylist[0]
        assert response_body["email"] == (entrylist[1])
        assert response_body["password"] == (entrylist[2])
        
# Unit testing for deleting entry
@pytest.mark.parametrize ("entrylist", [ ['test5@gmai.com','123']
])
def test_deleteuserAPI (client, entrylist, capsys): 
    with capsys.disabled():
        #prepare the data into a dictionary
        data1 = { 'email': entrylist[0],
        'password' :  entrylist[1]}
        #use client object to post data & converted to json 
        response = client.post('/api/addu', data=json.dumps (data1),content_type="application/json",)
        response_body= json. loads (response.get_data (as_text=True)) 
        assert response_body["id"]
        id = response_body["id"]
        response2 = client.get(f'/api/deleteuser/{id}')
        ret = json.loads (response2.get_data (as_text=True))
        #check the outcome of the action
        assert response2.status_code == 200
        assert response2.headers["Content-Type"] == "application/json"
        response2_body = json. loads (response2.get_data(as_text=True))
        assert response2_body ["result"] == "ok"