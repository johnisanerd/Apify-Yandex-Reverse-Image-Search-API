# 🔎 Yandex Reverse Image Search API: search by image, get structured JSON

> The most efficient, reliable, and developer-friendly way to use the Yandex Reverse Image Search API.

**Actor page:** [apify.com/johnvc/yandex-reverse-image-search](https://apify.com/johnvc/yandex-reverse-image-search?fpr=9n7kx3)
**Input schema:** [apify.com/johnvc/yandex-reverse-image-search/input-schema](https://apify.com/johnvc/yandex-reverse-image-search/input-schema?fpr=9n7kx3)

Search by image instead of by keywords. Give this reverse image search API the public URL of any image and it searches Yandex's reverse image engine (the same one behind yandex.com/images) to find every page where the image appears online, visually similar images, other sizes and resolutions of the same image, products that match the image, and descriptive tags. Every result is one JSON row tagged with a `result_type` field, so you can filter and route the data straight into your own code. Pay per result, with a hard cap you control.

## Video Walkthrough

[![Watch the walkthrough](https://img.youtube.com/vi/jREWahDGhJM/maxresdefault.jpg)](https://www.youtube.com/watch?v=jREWahDGhJM)

## Quick Start

### Prerequisites
- Python 3.11 or higher
- An Apify account and API key ([get a free key here](https://apify.com?fpr=9n7kx3))

1. **Clone the repository**
   ```bash
   git clone https://github.com/johnisanerd/Apify-Yandex-Reverse-Image-Search-API.git
   cd Apify-Yandex-Reverse-Image-Search-API
   ```

2. **Install dependencies with UV**
   ```bash
   # Install UV if you do not have it:
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install project dependencies:
   uv sync
   ```

3. **Configure your API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your Apify API key
   # Get your free API key at: https://apify.com?fpr=9n7kx3
   ```

4. **Run the example**
   ```bash
   uv run python yandex-reverse-image-search-api-example.py
   ```

### Alternative: set the API key directly
```bash
export APIFY_API_TOKEN="your_api_key_here"
uv run python yandex-reverse-image-search-api-example.py
```

## Why Use This Reverse Image Search API?

**Search by image, not by keyword.** A normal image search takes words and returns pictures. This reverse image search API does the opposite: you hand it a picture and it returns where that picture appears online, what looks similar to it, and what is in it. That is the difference between guessing a caption and asking the web directly.

**Yandex coverage as a clean API.** Yandex is widely regarded as one of the strongest reverse image engines on the web, especially for faces, places, and content that Western engines miss. This actor gives you that reach as a typed JSON endpoint, no HTML, no tokens, no blocking to manage on your side.

**One row per result, tagged and filterable.** Every result comes back as a single dataset row with a `result_type` field, so you can split matching pages from similar images from shopping matches in one pass and send each type where it belongs.

**Cost you control.** Billing is one charge per result row. You decide which result types to turn on and set a `max_results` cap, so a first run can be a few cents and a monitoring run can be tightly bounded.

**Built for automation and source hunting.** Save an image as a task, put it on a schedule, and re-check Yandex for new copies over time. It is a practical base for brand protection, counterfeit detection, image provenance work, and source hunting, tracing a compressed or cropped image back to its original.

## Features

### Core Capabilities
- Search by any public image URL and get every page where the image appears, with title, link, snippet, and source.
- Retrieve visually similar images from across the web, with thumbnails and full-size links.
- Optional result types: other resolutions of the same image, descriptive image tags, matching shop products with prices, and a knowledge-graph entity card.
- Crop-box targeting: search only part of an image (one face in a group photo, one product on a shelf).
- Six regional Yandex domains (yandex.com, yandex.ru, yandex.by, yandex.kz, yandex.uz, yandex.com.tr).

### Data Quality
- Structured JSON with a `result_type` tag on every row for easy filtering.
- A `max_results` cap that bounds both the rows returned and the amount billed.
- Consistent fields (title, link, source, original, thumbnail, search timestamp) across matching pages and similar images.

## Usage Examples

### Basic Example
```json
{
  "image_url": "https://example.com/product.jpg",
  "max_results": 20
}
```

### Advanced Example
```json
{
  "image_url": "https://example.com/group-photo.jpg",
  "crop": "0.1;0.2;0.5;0.8",
  "include_matching_pages": true,
  "include_similar_images": true,
  "include_shopping_results": true,
  "yandex_domain": "yandex.ru",
  "max_results": 100
}
```

## Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `image_url` | `str` | YES | - | Public http(s) URL of the image to search by. Yandex fetches it, so it must be reachable from the internet (direct image link, no login or redirect). |
| `crop` | `str` | no | (none) | Search only part of the image: four `;`-separated fractions 0-1 in the order left;top;right;bottom, e.g. `0.1;0.2;0.9;0.8`. |
| `include_matching_pages` | `bool` | no | `true` | Pages where the image appears online (result_type `matching_page`). |
| `include_similar_images` | `bool` | no | `true` | Visually similar images (result_type `similar_image`). |
| `include_image_sizes` | `bool` | no | `false` | Other resolutions of the same image (result_type `image_size`). |
| `include_image_tags` | `bool` | no | `false` | Descriptive tags for the image content (result_type `image_tag`). |
| `include_shopping_results` | `bool` | no | `false` | Matching products with prices (result_type `shopping_result`). |
| `include_knowledge_graph` | `bool` | no | `false` | Entity card for recognizable subjects (result_type `knowledge_graph`). |
| `yandex_domain` | `str` | no | `yandex.com` | Regional domain: `yandex.com`, `yandex.ru`, `yandex.by`, `yandex.kz`, `yandex.uz`, `yandex.com.tr`. |
| `max_results` | `int` | no | `0` | Hard cap on rows returned and billed. `0` = everything found. Set `20` for a cheap first run. |

## Output Format

Each result is one dataset row tagged with a `result_type`. A `matching_page` row looks like this:

```json
{
  "result_type": "matching_page",
  "position": 27,
  "title": "Central Illustration Agency Illustration portfolio: Matt Taylor",
  "link": "https://tr.pinterest.com/pin/matt-taylor-digital-illustration-illustrator-graphic-poster-art-car-scenery-bold--826762444071832079/",
  "thumbnail": "https://avatars.mds.yandex.net/i?id=592d913ed53e1f78fdd0804bd7064417b709bafb-5437458-images-thumbs&n=13&w=296&h=180",
  "original": "https://i.pinimg.com/736x/9e/b1/f7/9eb1f76ee45eb01706be89b8748a911b.jpg",
  "source": "tr.pinterest.com",
  "snippet": "After graduating from Buckinghamshire University he rolled straight into a successful ten year illustration career.",
  "image_url": "https://substack-post-media.s3.amazonaws.com/public/images/edbfb2cd-ebcb-4527-bec7-5315c182278f_445x445.png",
  "yandex_domain": "yandex.com",
  "crop": "",
  "search_timestamp": "2026-07-05T12:00:00"
}
```

Every row also carries the query image URL, the Yandex domain used, the crop box (if any), and a search timestamp.

---

<!-- The five install sections below come verbatim from the canonical MCP install copy.
     Each embeds a hosted screenshot from ApifyPublicData/assets/guides (no local screenshots/ folder). -->

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the Yandex Reverse Image Search API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings → Connectors** (or **Settings → Developer → Edit Config** to edit `claude_desktop_config.json` directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with only this Actor:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/yandex-reverse-image-search"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt in your browser, or add your Apify API token in the connector settings to skip OAuth.
4. In a Cowork chat, confirm the tool is available and ask it to run the Yandex Reverse Image Search API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the Actor's MCP server with one command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/yandex-reverse-image-search"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/yandex-reverse-image-search" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude Code to call the Yandex Reverse Image Search API.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable just this Actor's tool.

1. Go to **Settings → Connectors → Browse connectors** and search for **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tool `johnvc/yandex-reverse-image-search`.
3. In any chat, open **+ → Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL `https://mcp.apify.com/?tools=actors,docs,johnvc/yandex-reverse-image-search`, using OAuth when prompted.
5. Ask Claude to run the Yandex Reverse Image Search API.

Open Claude on the web: https://claude.ai/referral/uIlpa7nPLg

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/yandex-reverse-image-search"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/yandex-reverse-image-search",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

3. Open **Cursor → Settings → MCP** and confirm the **apify** server is connected (green dot).
4. In Composer or Chat, ask Cursor to call the Yandex Reverse Image Search API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a **Create app** button, open **Advanced settings** and enable **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/yandex-reverse-image-search`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp

---

[**Made with care**](https://apify.com/johnvc?fpr=9n7kx3)

*Use the Yandex Reverse Image Search API to power your image monitoring, brand protection, and source hunting workflows with reliable, structured results.*

Last Updated: 2026.09.03
