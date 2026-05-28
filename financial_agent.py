import os
import yfinance as yf
import pandas as pd
from google import genai
from google.genai import types

# Initialize the Gemini Client
client = genai.Client()

def get_indian_stock_data(ticker: str) -> dict:
    """
    Fetches real-time fundamental financial metrics, valuations, shareholding 
    patterns, and YoY/QoQ growth metrics for an Indian stock ticker from the NSE.
    """
    try:
        ticker = ticker.strip().upper()
        if not ticker.endswith(".NS"):
            ticker = f"{ticker}.NS"
            
        stock = yf.Ticker(ticker)
        info = stock.info
        
        if not info or 'longName' not in info:
            return {"error": f"Ticker {ticker} not found on the exchange."}
            
        metrics = {
            "Company Name": info.get("longName"),
            "Sector / Industry": info.get("industry"),
            "Current Price (INR)": info.get("currentPrice") or info.get("regularMarketPrice"),
            "Book Value per Share (INR)": info.get("bookValue"),
            "Price to Book (P/B)": info.get("priceToBook"),
            "Trailing P/E Ratio": info.get("trailingPE"),
            "Dividend Yield (%)": (info.get("dividendYield", 0) * 100) if info.get("dividendYield", 0) < 1 else info.get("dividendYield", 0),
            "Market Cap (INR)": info.get("marketCap"),
            "Promoter Shareholding (%)": (info.get("heldPercentInsiders", 0) * 100) if info.get("heldPercentInsiders") else "N/A",
            "Institutional Holding (%)": (info.get("heldPercentInstitutions", 0) * 100) if info.get("heldPercentInstitutions") else "N/A",
            "YoY Revenue Growth (%)": (info.get("revenueGrowth", 0) * 100) if info.get("revenueGrowth") else "N/A",
            "YoY Earnings Growth (%)": (info.get("earningsGrowth", 0) * 100) if info.get("earningsGrowth") else "N/A"
        }
        
        try:
            q_financials = stock.quarterly_financials
            q_financials.index = q_financials.index.str.lower()
            target_labels = ['total revenue', 'revenue', 'operating revenue']
            matching_row = [label for label in target_labels if label in q_financials.index]
            if matching_row and len(q_financials.columns) >= 2:
                revenue_series = q_financials.loc[matching_row]
                latest_q = revenue_series.iloc if isinstance(revenue_series, pd.DataFrame) else revenue_series.iloc
                prev_q = revenue_series.iloc if isinstance(revenue_series, pd.DataFrame) else revenue_series.iloc
                if pd.notna(latest_q) and pd.notna(prev_q) and prev_q != 0:
                    metrics["QoQ Revenue Growth (%)"] = ((latest_q - prev_q) / prev_q) * 100
        except:
            pass
            
        return metrics
    except Exception as e:
        return {"error": f"Failed to retrieve data matrix: {str(e)}"}

financial_tools = [get_indian_stock_data]

def start_conversational_agent():
    print("\n==================================================================")
    print("    🤖 LIVE CHAT: INDIAN STOCK FUNDAMENTAL AI AGENT INITIALIZED    ")
    print("==================================================================")
    print("Ask me anything about Indian stocks in plain language!")
    print("Example: 'Check out TCS fundamentals' or 'Compare INFY vs Reliance'")
    print("Type 'exit' or 'quit' to close the chatbot session.\n")
    
    system_instruction = (
        "You are an elite, highly professional Indian Stock Market Research Analyst. "
        "Your mandate is to use the provided `get_indian_stock_data` tool to fetch live factual data "
        "before answering any query about an Indian company. For any stock mentioned, extract its data "
        "using its ticker symbol (ensure you use the ticker plus '.NS' for accurate tool parsing). "
        "Provide thorough fundamental analysis, evaluate its book value, promoter holding configurations, "
        "and present your conclusions clearly."
    )
    
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=financial_tools,
            temperature=0.15
        )
    )
    
    while True:
        try:
            user_input = input("\nYou 👤: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit']:
                print("\nAI Agent: Closing session. Happy investing! 🚀")
                break
                
            print("AI Agent 🤖: Analyzing market vectors...")
            response = chat.send_message(user_input)
            print(f"\nAI Agent 🤖:\n{response.text}")
            print("-" * 66)
        except KeyboardInterrupt:
            print("\nAI Agent: Session closed manually.")
            break
        except Exception as err:
            print(f"\n❌ Error processing chat interaction: {str(err)}")

if __name__ == "__main__":
    start_conversational_agent()
