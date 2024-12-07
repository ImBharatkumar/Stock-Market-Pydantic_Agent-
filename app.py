from fastapi import FastAPI, HTTPException, Depends
from pydantic_ai import Agent
from pydantic import BaseModel
import yfinance as yf
import asyncio
import nest_asyncio  
from database import get_db
from models import Competitor,Base
from sqlalchemy.orm import Session


# Ensure database tables are created
from database import engine
Base.metadata.create_all(bind=engine)




# Apply nest_asyncio patch to allow nested event loops
nest_asyncio.apply()


# Class is inherited from BaseModel to validate varibables used in the programm
class StockPriceResult(BaseModel):
    symbol: str
    price: float
    currency: str = "USD"
    message: str
    info: str
    market_cap: float
    price_to_earning: float


# Function to get competition stock price
def sync_get_stock_price(symbol: str):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        price = ticker.fast_info.last_price
        return {
        "info": info['sector'],
        "market_cap":info['marketCap'],
        "price_to_earning":info['trailingPE'],
        "price": round(price, 2),
        "currency": "USD"
    }
    except Exception as e:
        raise ValueError(f"Error fetching stock price: {str(e)}")


# Save stock data to database using table competitor
def svae_data_to_db(db:Session ,stock_data:dict):
    try:
        # Create a new Competitor instance
        new_competitor = Competitor(
            name=stock_data['name'],
            sector=stock_data['sector'],
            price_to_earning=stock_data['price_to_earning'],  # Ensure float
            market_share=stock_data['market_cap'] # Convert to percentage
        )
        
        # Add to session and commit
        db.add(new_competitor)
        db.commit()
        db.refresh(new_competitor)
        return new_competitor
    except Exception as e:
        db.rollback()
        raise ValueError(f"Database insertion error: {str(e)}")




#defining the Agent
stock_agent = Agent(
    "groq:llama3-groq-70b-8192-tool-use-preview",
    result_type=StockPriceResult,
    system_prompt="You are a helpful financial assistant that can look up stock prices."
)



#Binding LLm with tool to fetch the stock information using yfinance
@stock_agent.tool_plain
def get_stock_price(symbol: str) -> dict:
    return sync_get_stock_price(symbol)



################################################################################################
# Fast api for serving application
app = FastAPI()

@app.post("/get_result/")
async def getanswer(symbol: str, db:Session = Depends(get_db)):
    try:
        # Use asyncio.run() to ensure an event loop
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, 
            lambda: stock_agent.run_sync(f"current stock price of {symbol}")
        )
        
        stock_data= {"name":symbol,
                "sector":result.data.info,
                "Current_Stock_Price": result.data.price,
                "market_cap":result.data.market_cap,
                "price_to_earning":result.data.price_to_earning
                }
        # Save to database
        saved_competitor = svae_data_to_db(db, stock_data)

        #return following to console/on server
        return {
            "name":symbol,
            "sector":result.data.info,
            "Current_Stock_Price": result.data.price,
            "market_cap":result.data.market_cap,
            "price_to_earning":result.data.price_to_earning,
            "saved_id": saved_competitor.id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@app.get("/competitor/{id}")
async def get_competitor(id: int, db: Session = Depends(get_db)):
    competitor = db.query(Competitor).filter(Competitor.id == id).first()
    if competitor is None:
        raise HTTPException(status_code=404, detail="Competitor not found")
    return competitor
