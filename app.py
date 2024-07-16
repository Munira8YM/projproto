from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# Mock data for demonstration purposes
top_districts = [
    "District A", "District B", "District C", "District D", "District E",
    "District F", "District G", "District H", "District I", "District J"
]

district_prices = {
    "District A": 1000,
    "District B": 1100,
    "District C": 1200,
    "District D": 1300,
    "District E": 1400,
    "District F": 1500,
    "District G": 1600,
    "District H": 1700,
    "District I": 1800,
    "District J": 1900,
}

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Home Page</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                background-color: #f0f0f0;
            }
            h1 {
                color: #333;
            }
            button {
                margin: 10px;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to the Real Estate Info Site</h1>
        <p>Select your purpose:</p>
        <form action="/best_districts" method="get">
            <button type="submit">Know the Best Districts</button>
        </form>
        <form action="/price_per_meter" method="get">
            <button type="submit">Know the Prices per Meter</button>
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/best_districts", response_class=HTMLResponse)
def best_districts():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Best Districts</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                background-color: #f0f0f0;
            }
            h1 {
                color: #333;
            }
            form {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            input {
                margin: 5px;
                padding: 10px;
                font-size: 16px;
            }
            button {
                margin: 10px;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <h1>Top 10 Best Districts</h1>
        <ol>
            """ + "".join([f"<li>{district}</li>" for district in top_districts]) + """
        </ol>
        <a href="/">Back to Home</a>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/price_per_meter", response_class=HTMLResponse)
def price_per_meter():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Price per Meter</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                background-color: #f0f0f0;
            }
            h1 {
                color: #333;
            }
            form {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            input {
                margin: 5px;
                padding: 10px;
                font-size: 16px;
            }
            button {
                margin: 10px;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <h1>Enter District Name</h1>
        <form action="/district_price" method="post">
            <input type="text" name="district_name" placeholder="Enter district name">
            <button type="submit">Submit</button>
        </form>
        <a href="/">Back to Home</a>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/district_price", response_class=HTMLResponse)
def district_price(district_name: str = Form(...)):
    price = district_prices.get(district_name, "District not found")
    response_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>District Price</title>
    </head>
    <body>
        <h1>Price per Meter for {district_name}</h1>
        <p>{price if isinstance(price, str) else f"${price} per meter"}</p>
        <a href="/">Back to Home</a>
    </body>
    </html>
    """
    return HTMLResponse(content=response_content)