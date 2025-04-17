# Crypto Trending MCP Server

An MCP server that tracks and monitors the latest trending tokens on CoinGecko, providing real-time insights into the most popular cryptocurrencies.

[![Discord](https://img.shields.io/discord/1353556181251133481?cacheSeconds=3600)](https://discord.gg/aRnuu2eJ)
![GitHub License](https://img.shields.io/github/license/kukapay/crypto-trending-mcp)
![Python Version](https://img.shields.io/badge/python-3.10+-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## Features

- **Tool: `get_trending_md_doc`**  
  Returns a Markdown document of the full CoinGecko trending page, including a table of trending cryptocurrencies with columns: Rank, Name, Symbol, Price, 1h Change, 24h Change, 7d Change, 24h Volume, Market Cap.

- **Prompt: `parse_trending_md_doc`**  
  Guides MCP clients to extract the trending coins table from the Markdown document and parse it with an LLM, supporting analyses like identifying coins with positive price changes or ranking by market cap.

- **Seamless Integration**  
  Designed for use with Claude Desktop, allowing natural language queries to analyze trending crypto data via MCP tools and prompts.

- **Lightweight & Extensible**  
  Built with minimal dependencies and a simple architecture, making it easy to extend or deploy.

## Installation

### Prerequisites

- **Python 3.10+**
- **Node.js** (for Playwright browser dependencies)
- **Claude Desktop** (optional, for testing with MCP client)

### Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/kukapay/crypto-trending-mcp.git
   cd crypto-trending-mcp
   ```

2. **Install Dependencies with uv**:

   ```bash
   uv sync
   playwright install
   ```

## Usage

### Integrating with Claude Desktop

1. **Configure Claude Desktop**:

   - Edit the configuration file:
     - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
     - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - Add the server configuration:

     ```json
     {
       "mcpServers": {
         "crypto-trending": {
           "command": "uv",
           "args": [
             "--directory",
             "/absolute/path/to/crypto-trending-mcp",
             "run",
             "main.py"
           ]
         }
       }
     }
     ```

     Replace `/absolute/path/to/crypto-trending-mcp` with the absolute path to your `main.py`.

2. **Restart Claude Desktop**:

   - Close and reopen Claude Desktop.
   - Look for the hammer icon (🔨) in the input box, indicating MCP tools are available.

3. **Interact with the Server**:

   - Ask natural language questions like:
     - "What are the trending cryptocurrencies with positive 24h price changes?"
     - "Show the top 3 trending coins by market cap."
   - Claude will use the `get_trending_md_doc` tool and `parse_trending_md_doc` prompt to fetch and analyze the data.

### Example Output

The `get_trending_md_doc` tool returns a Markdown document like:

```markdown
# Trending Crypto

...

| Rank | Name        | Symbol | Price      | 1h Change | 24h Change | 7d Change | 24h Volume      | Market Cap         |
|------|-------------|--------|------------|-----------|------------|-----------|-----------------|-------------------|
| 1    | Bitcoin     | BTC    | $67,890.12 | +0.45%    | +2.34%     | +10.12%   | $45,123,456,789 | $1,345,678,901,234 |
| 2    | Ethereum    | ETH    | $2,456.78  | -0.12%    | -1.12%     | +5.67%    | $20,987,654,321 | $295,123,456,789   |
| 3    | Solana      | SOL    | $167.45    | +0.89%    | +5.67%     | +15.34%   | $3,456,789,123  | $78,901,234,567    |

...

*Data from CoinGecko*
```

The `parse_trending_md_doc` prompt guides the LLM to extract the table and produce structured output, such as:

```json
[
  {
    "rank": 1,
    "name": "Bitcoin",
    "symbol": "BTC",
    "price": "$67,890.12",
    "change_1h": "+0.45%",
    "change_24h": "+2.34%",
    "change_7d": "+10.12%",
    "volume_24h": "$45,123,456,789",
    "market_cap": "$1,345,678,901,234"
  },
  ...
]
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
