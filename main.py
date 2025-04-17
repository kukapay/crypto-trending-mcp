from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright
import html2text
import asyncio

# Initialize the MCP server
mcp = FastMCP("CryptoTrending", dependencies=["playwright", "html2text"])

async def scrape_trending_coins() -> str:
    """Scrape the CoinGecko trending page and convert it to Markdown."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(
          headless=True
        )
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            permissions=['geolocation', 'notifications']
        )        
        page = await context.new_page()
        await page.goto("https://www.coingecko.com/en/highlights/trending-crypto")
        
        # Wait for the page to load key content
        await page.wait_for_selector("table", timeout=60000)
        
        # Get the full HTML content of the page
        html_content = await page.content()
        
        # Convert HTML to Markdown using html2text
        h = html2text.HTML2Text()
        h.ignore_links = True  # Skip links
        h.ignore_images = True  # Skip images
        h.body_width = 0  # Disable line wrapping
        markdown = h.handle(html_content)
        
        await browser.close()
        return markdown

# Tool: Get trending coins in Markdown format
@mcp.tool()
async def get_trending_md_doc() -> str:
    """
    Retrieve a Markdown document containing the CoinGecko trending cryptocurrencies page.
    
    Returns:
        A string containing a Markdown-formatted document representing the full CoinGecko trending page.
        The document includes:
        - Page headers and introductory text.
        - A table of trending cryptocurrencies with columns such as Rank, Name, Symbol, Price,
          1h Change, 24h Change, 7d Change, 24h Volume, and Market Cap.
        - Additional page content like footers, navigation, or metadata.
        The trending coins table is embedded within the document and can be extracted for analysis.
    """
    return await scrape_trending_coins()

# Prompt: Guide the client on extracting and parsing the Markdown table
@mcp.prompt()
def parse_trending_md_doc(doc: str) -> str:
    """
    Guide the MCP client to parse the trending coins table from a CoinGecko Markdown document using an LLM.

    Args:
        doc (str): The Markdown document containing the trending coins table.
    
    Returns:
        A string with instructions for the LLM to extract and parse the table.
    """
    return """
The following Markdown document contains the CoinGecko trending cryptocurrencies page, including a table of trending coins among other content:

{md_doc}

1. Extract the table with columns: Rank, Name, Symbol, Price, 1h Change, 24h Change, 7d Change, 24h Volume, Market Cap.
2. Parse the table into JSON, where each coin is an object with fields: rank, name, symbol, price, change_1h, change_24h, change_7d, volume_24h, market_cap.
""".format(md_doc=doc)

if __name__ == "__main__":
    mcp.run()
