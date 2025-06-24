from dotenv import load_dotenv
from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI,set_tracing_disabled,function_tool
import os
import asyncio
import requests
#----------------------------------------------

load_dotenv()
#----------------------------------------------

set_tracing_disabled(disabled=True)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
#-----------------------------------------------

client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)
#---------------------------------------------

@function_tool
def cryptocurrency_price(symbol:str):
    """
    fetches the current price of cryptocurrency, The symbol (e.g., BTCUSDT, ETHBTC) may be in lowercase or uppercase
    """
    symbol = symbol.upper()
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    responce = requests.get(url)
#--------------------------------------------

    if responce.status_code == 200:
        data = responce.json()
        return {"symbol": symbol, "price": data["price"]}
    else:
        return {"error": f"Failed to fetch data for symbol {symbol}"}
    
#---------------------------------------------------

agent = Agent(
    name="my_agent",
    model=OpenAIChatCompletionsModel(model="mistralai/mistral-small-24b-instruct-2501", openai_client=client),
    instructions="You are a helpful assistant, you can help users by answering questions and fetching real time cryptocurrency data using available tools",
    tools=[cryptocurrency_price]
)
#-----------------------------------------------

async def main():
    query = input("\n Enter your crypto query: ")
    res = await Runner.run(agent,query)
    print("\n Output from crypto currency Assistant.")
    print("\n 🔥:",res.final_output, "\n")
#-----------------------------------------------


if __name__ == "__main__":
    asyncio.run(main())
