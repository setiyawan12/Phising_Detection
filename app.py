from typing import Union
import joblib,os
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#pkl
phish_model = open('phishingv3.pkl','rb')
phish_model_ls = joblib.load(phish_model)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/predict/{feature}')
async def predict(features):
	X_predict = []
	X_predict.append(str(features))
	y_Predict = phish_model_ls.predict(X_predict)
	if y_Predict == 'bad':
		result = "This is a Phishing Site"
	else:
		result = "This is not a Phishing Site"
	
	# return (features, result)
	return {"data":features,"result":result}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == '__main__':
	uvicorn.run(app,host="127.0.0.1",port=8181)