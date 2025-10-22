#!/usr/bin/env python3
"""
News to X Post Generator Bot
Fetches current news headlines and generates engaging X (Twitter) posts.
"""

import random
from datetime import datetime
from typing import List, Dict
import json
import os
import urllib.request
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv is optional
    pass


class NewsBot:
    """Bot that generates X posts from news headlines."""

    # Free RSS news feeds from major sources
    # Using more bot-friendly sources
    NEWS_FEEDS = [
        "https://rss.sciencedaily.com/top.xml",  # Science Daily
        "https://www.reddit.com/r/worldnews/.rss",  # Reddit World News
        "https://www.reddit.com/r/technology/.rss",  # Reddit Technology
        "https://hnrss.org/frontpage",  # Hacker News
        "https://www.engadget.com/rss.xml",  # Engadget
    ]

    # Post templates for variety
    POST_TEMPLATES = [
        "🔥 Breaking: {headline}",
        "📰 Just in: {headline}",
        "⚡️ {headline}",
        "🌍 News: {headline}",
        "{headline} 👀",
        "📢 {headline}",
        "💡 {headline}",
        "🚨 {headline}",
    ]

    # Demo headlines for testing when network is unavailable
    DEMO_HEADLINES = [
        {
            'title': 'Scientists Discover New Method to Convert CO2 into Renewable Fuel',
            'link': 'https://example.com/climate-breakthrough',
            'source': 'Science Daily',
            'published': 'Today'
        },
        {
            'title': 'Major Tech Company Announces Revolutionary AI Chip with 10x Performance',
            'link': 'https://example.com/ai-chip',
            'source': 'Tech News',
            'published': 'Today'
        },
        {
            'title': 'Global Leaders Reach Historic Agreement on Climate Change at Summit',
            'link': 'https://example.com/climate-summit',
            'source': 'World News',
            'published': 'Today'
        },
        {
            'title': 'Breakthrough in Quantum Computing Brings Practical Applications Closer',
            'link': 'https://example.com/quantum',
            'source': 'Technology',
            'published': 'Today'
        },
        {
            'title': 'New Study Shows Promising Results for Cancer Treatment Using CRISPR',
            'link': 'https://example.com/crispr-cancer',
            'source': 'Medical News',
            'published': 'Today'
        },
        {
            'title': 'SpaceX Successfully Launches Mission to Establish Lunar Base',
            'link': 'https://example.com/moon-base',
            'source': 'Space News',
            'published': 'Today'
        },
        {
            'title': 'Researchers Develop Battery Technology with 5x Longer Life',
            'link': 'https://example.com/battery-tech',
            'source': 'Innovation Daily',
            'published': 'Today'
        },
        {
            'title': 'Major Cybersecurity Vulnerability Discovered in Popular Software',
            'link': 'https://example.com/security-alert',
            'source': 'Security News',
            'published': 'Today'
        },
    ]

    def __init__(self, max_posts: int = 5, demo_mode: bool = False):
        """
        Initialize the news bot.

        Args:
            max_posts: Maximum number of posts to generate
            demo_mode: Use demo headlines instead of fetching real news
        """
        self.max_posts = max_posts
        self.max_length = 280  # X character limit
        self.demo_mode = demo_mode

    def fetch_headlines(self) -> List[Dict[str, str]]:
        """
        Fetch headlines from various news sources using RSS feeds.

        Returns:
            List of dictionaries containing headline info
        """
        # Use demo mode if enabled
        if self.demo_mode:
            print("Using demo headlines (demo mode enabled)")
            return self.DEMO_HEADLINES.copy()

        headlines = []

        print("Fetching news headlines...")
        for feed_url in self.NEWS_FEEDS:
            try:
                # Fetch RSS feed
                req = urllib.request.Request(
                    feed_url,
                    headers={'User-Agent': 'Mozilla/5.0 (NewsBot/1.0)'}
                )

                with urllib.request.urlopen(req, timeout=10) as response:
                    xml_content = response.read()

                # Parse XML
                root = ET.fromstring(xml_content)

                # Get source name
                source_elem = root.find('.//channel/title')
                source = source_elem.text if source_elem is not None else 'News Source'

                # Extract items (headlines)
                for item in root.findall('.//item')[:5]:  # Top 5 from each source
                    title_elem = item.find('title')
                    link_elem = item.find('link')
                    pub_elem = item.find('pubDate')

                    if title_elem is not None and link_elem is not None:
                        headlines.append({
                            'title': title_elem.text,
                            'link': link_elem.text,
                            'source': source,
                            'published': pub_elem.text if pub_elem is not None else 'Unknown'
                        })

                print(f"✓ Fetched from {source}")
            except Exception as e:
                print(f"✗ Error fetching from {feed_url}: {e}")

        # Fallback to demo mode if no headlines were fetched
        if not headlines:
            print("\n⚠ No headlines fetched from RSS feeds")
            print("Falling back to demo mode...")
            return self.DEMO_HEADLINES.copy()

        return headlines

    def generate_post(self, headline: Dict[str, str]) -> str:
        """
        Generate an X post from a headline.

        Args:
            headline: Dictionary containing headline information

        Returns:
            Formatted X post text
        """
        # Choose a random template
        template = random.choice(self.POST_TEMPLATES)

        # Get the headline title
        title = headline['title']
        link = headline['link']

        # Start with template
        post = template.format(headline=title)

        # Add link if there's space
        if len(post) + len(link) + 2 <= self.max_length:
            post = f"{post}\n{link}"
        else:
            # Truncate title to make room for link
            available_space = self.max_length - len(template.format(headline="")) - len(link) - 5
            if available_space > 50:
                truncated_title = title[:available_space] + "..."
                post = template.format(headline=truncated_title)
                post = f"{post}\n{link}"

        return post

    def generate_posts(self) -> List[str]:
        """
        Generate multiple X posts from current news.

        Returns:
            List of formatted X posts
        """
        headlines = self.fetch_headlines()

        if not headlines:
            print("No headlines found!")
            return []

        # Shuffle to get variety
        random.shuffle(headlines)

        # Generate posts
        posts = []
        for headline in headlines[:self.max_posts]:
            post = self.generate_post(headline)
            posts.append(post)

        return posts

    def save_posts(self, posts: List[str], filename: str = "posts.json"):
        """
        Save generated posts to a JSON file.

        Args:
            posts: List of post texts
            filename: Output filename
        """
        output = {
            'generated_at': datetime.now().isoformat(),
            'count': len(posts),
            'posts': posts
        }

        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"\n✓ Saved {len(posts)} posts to {filename}")

    def display_posts(self, posts: List[str]):
        """
        Display generated posts to console.

        Args:
            posts: List of post texts
        """
        print(f"\n{'='*60}")
        print(f"Generated {len(posts)} X Posts")
        print(f"{'='*60}\n")

        for i, post in enumerate(posts, 1):
            print(f"Post #{i}:")
            print(f"{'-'*60}")
            print(post)
            print(f"{'-'*60}")
            print(f"Characters: {len(post)}/280\n")


def main():
    """Main function to run the bot."""
    print("🤖 News to X Post Generator Bot")
    print("=" * 60)

    # Get configuration from environment
    num_posts = int(os.getenv('NUM_POSTS', '5'))
    demo_mode = os.getenv('DEMO_MODE', 'false').lower() == 'true'

    # Create bot instance
    bot = NewsBot(max_posts=num_posts, demo_mode=demo_mode)

    # Generate posts
    posts = bot.generate_posts()

    if posts:
        # Display posts
        bot.display_posts(posts)

        # Save to file
        bot.save_posts(posts)

        print(f"✓ Successfully generated {len(posts)} posts!")
    else:
        print("✗ Failed to generate posts")


if __name__ == "__main__":
    main()
