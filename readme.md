<div align="center">
<a href="https://github.com/ajb3932/immich-partner-sharing"><img src="https://raw.githubusercontent.com/ajb3932/immich-partner-sharing/refs/heads/main/partnersharing.png" title="Logo" style="max-width:100%;" width="128" alt='App Logo' /></a>
</div>

# 🤝 Immich Partner Sharing

Automatically sync faces to albums in Immich, recreating Google Photos partner sharing functionality.

Built on the amazing Python package [immich-face-to-album](https://pypi.org/project/immich-face-to-album/) by romainrbr.

Initially created as my wife and I have separate Immich accounts but would like to share photos of our daughter automatically.

## 📷 Screenshot

<img src="https://raw.githubusercontent.com/ajb3932/immich-partner-sharing/main/screenshot.jpg" title="App Screenshot" style="max-width:100%;" alt='App Screenshot'/>

## ✨ Features

- ✅ **Unlimited Face Mappings**: Configure as many face-to-album syncs as needed
- ✅ **Multi-Account Support**: Works across different Immich user accounts  
- ✅ **Incremental Sync**: Only adds new photos, doesn't duplicate existing ones
- ✅ **Dry Run Mode**: Test configuration without making changes
- ✅ **Health Checks**: Built-in monitoring and error handling
- ✅ **Unraid Ready**: Includes Community Applications template

## ⚠️ Disclaimer

**This project is not affiliated with [immich][immich-github-url]!**

## 🐳 Docker 

**Docker Compose:**

Copy and paste this text into your `docker-compose.yml` file, make your own edits, and run it with `docker-compose up -d`

```yaml
services:
  immich-partner-sharing:
    image: ajb3932/immich-partner-sharing:latest
    container_name: immich-partner-sharing
    restart: unless-stopped
    network_mode: host
    environment:
      - IMMICH_SERVER=http://localhost:2283
      - SYNC_INTERVAL_MINUTES=60
      - RUN_ONCE=false
      - DRY_RUN=false
      - SYNC_MAPPING_1=your-api-key-1:face-id-1:album-id-1:Photos of John
      - SYNC_MAPPING_2=your-api-key-2:face-id-2:album-id-2:Photos of Jane
      - SYNC_MAPPING_3=your-api-key-1:face-id-3:album-id-3:Photos of Kids
      # Add more mappings as needed...
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('${IMMICH_SERVER}/api/server-info')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

**Docker CLI:**

⚠️ Must have an Immich server running and accessible.

```bash
docker run -d \
  --name immich-partner-sharing \
  --network host \
  -e IMMICH_SERVER="http://localhost:2283" \
  -e SYNC_MAPPING_1="your-api-key:face-id:album-id:Description" \
  --restart unless-stopped \
  ajb3932/immich-partner-sharing
```

## 🌍 Environment Variables

The following Environment Variables are available:

| Variable Name | Description | Options | Default Value |
|---------------|-------------|---------|---------------|
| `IMMICH_SERVER` | URL of your Immich server | `http://[IP]:[PORT]` | `http://localhost:2283` |
| `SYNC_INTERVAL_MINUTES` | How often to check for new photos | `[MINUTES]` | `60` |
| `RUN_ONCE` | Run once and exit (for testing) | `true`, `false` | `false` |
| `DRY_RUN` | Test mode - show what would happen | `true`, `false` | `false` |
| `SYNC_MAPPING_X` | Face-to-album sync mapping | `api_key:face_id:album_id:description` | None |

## 🚀 First Run

1. **Create shared albums** for each account (e.g., "Partner Sharing - John", "Partner Sharing - Jane")
2. **Generate API keys** for each Immich user account
3. **Find Face and Album IDs** (see Finding IDs section below)
4. **Configure environment variables** with your mappings
5. **Test with dry run mode** first: `DRY_RUN=true`

## 🔍 Finding IDs

**API Keys:** Immich → Account Settings → API Keys → Create

**Face IDs:** Immich → Explore → People → Click person → Copy ID from URL  
Example URL: `http://your-server/people/f3437c84-83f9-4e84-9640-0dcd12efd08e`  
Face ID: `f3437c84-83f9-4e84-9640-0dcd12efd08e`

**Album IDs:** Immich → Albums → Click album → Copy ID from URL  
Example URL: `http://your-server/albums/ff85e8c5-32e6-49e0-a0ad-e4dd7ef66bce`  
Album ID: `ff85e8c5-32e6-49e0-a0ad-e4dd7ef66bce`

## 💡 Use Cases

| Use Case | Description |
|----------|-------------|
| **Partner Sharing** | Automatically share photos of family members between accounts |
| **Child Albums** | Keep all photos of your children organized across parent accounts |
| **Pet Albums** | Organize photos of pets (if face detection picks them up) |
| **Event Albums** | Automatically populate albums with photos of specific people |
| **Multi-User Families** | Sync faces across different user accounts seamlessly |

## 📝 Example Configuration

For a family with Alex and Abbie's accounts sharing photos of their daughter Mabel:

```bash
# Alex's account syncing photos of Mabel and Abbie to Abbie's partner album
SYNC_MAPPING_1=alex-api-key:mabel-face-id:abbie-album-id:Mabel to Abbies album
SYNC_MAPPING_2=alex-api-key:abbie-face-id:abbie-album-id:Abbie to Abbies album

# Abbie's account syncing photos of Mabel and Alex to Alex's partner album  
SYNC_MAPPING_3=abbie-api-key:mabel-face-id:alex-album-id:Mabel to Alex album
SYNC_MAPPING_4=abbie-api-key:alex-face-id:alex-album-id:Alex to Alex album
```

## 🙋 I want to run this myself

🐳 **Docker**
```bash
git clone https://github.com/ajb3932/immich-partner-sharing.git
cd immich-partner-sharing
cp .env-example .env
# Edit .env with your configuration
docker build -t immich-partner-sharing .
docker run -d --env-file .env immich-partner-sharing
```

🐳 **Docker Compose** (edit `.env` file first)
```bash
git clone https://github.com/ajb3932/immich-partner-sharing.git
cd immich-partner-sharing
cp .env-example .env
# Edit .env with your configuration
docker-compose up -d
```

💾 **Python** (for development)
```bash
git clone https://github.com/ajb3932/immich-partner-sharing.git
cd immich-partner-sharing/app
pip install -r requirements.txt
# Set environment variables
python main.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - feel free to use and modify!

## 🙏 Acknowledgments

- Built on [immich-face-to-album](https://pypi.org/project/immich-face-to-album/) by romainrbr
- Inspired by Google Photos partner sharing functionality
- Created for the amazing [Immich](https://immich.app/) self-hosted photo management platform

<div align="center">
<a href='https://ko-fi.com/F1F11GNNZU' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi4.png?v=6' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>
</div>
