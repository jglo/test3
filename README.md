# News to X Post Generator Bot

A Python bot that automatically fetches current mainstream news headlines and generates engaging X (Twitter) posts.

## Features

- 📰 Fetches real-time news from multiple major sources (CNN, BBC, Reuters, NYT, The Guardian)
- 🤖 Generates X-ready posts with proper formatting
- ⚡️ Multiple post templates for variety
- 📏 Respects X's 280 character limit
- 💾 Saves posts to JSON for easy access
- 🔗 Includes source links when space permits

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd test3
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Create a `.env` file for configuration:
```bash
cp .env.example .env
```

## Usage

Run the bot:
```bash
python news_bot.py
```

The bot will:
1. Fetch headlines from multiple news sources
2. Generate formatted X posts
3. Display them in the console
4. Save them to `posts.json`

## Configuration

You can configure the bot using environment variables in a `.env` file:

- `NUM_POSTS`: Number of posts to generate (default: 5)
- `DEMO_MODE`: Use demo headlines instead of fetching from RSS (default: false)

Example `.env`:
```
NUM_POSTS=10
DEMO_MODE=true
```

### Demo Mode

The bot includes a demo mode with sample headlines for testing:
- Automatically activates if RSS feeds are unavailable
- Can be manually enabled via `DEMO_MODE=true` environment variable
- Great for testing the post generation logic without network access

## Output

The bot generates two outputs:

1. **Console Display**: Shows all generated posts with character counts
2. **posts.json**: JSON file containing all posts with metadata

Example `posts.json`:
```json
{
  "generated_at": "2025-10-22T10:30:00",
  "count": 5,
  "posts": [
    "🔥 Breaking: Major tech announcement shakes industry\nhttps://example.com/article",
    "📰 Just in: Global leaders meet for climate summit\nhttps://example.com/article2"
  ]
}
```

## News Sources

The bot attempts to fetch from:
- Science Daily
- Reddit World News
- Reddit Technology
- Hacker News
- Engadget

**Note:** If RSS feeds are blocked or unavailable, the bot automatically falls back to demo mode with sample headlines.

## Post Templates

The bot uses various templates to create engaging posts:
- 🔥 Breaking: {headline}
- 📰 Just in: {headline}
- ⚡️ {headline}
- 🌍 News: {headline}
- And more...

## Requirements

- Python 3.7+
- Internet connection for fetching news

## License

MIT License

## Contributing

Feel free to open issues or submit pull requests!

## Notes

- This bot generates posts but does not automatically post to X
- You can use the generated posts manually or integrate with X's API
- RSS feeds are used for reliable, free news access
- The bot respects X's 280 character limit automatically
