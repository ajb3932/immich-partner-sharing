# Immich Partner Sharing

Automatically sync faces to albums in Immich, recreating Google Photos partner sharing functionality.

Built on the amazing work from 

## Features

- ✅ **Unlimited Face Mappings**: Configure as many face-to-album syncs as needed
- ✅ **Multi-Account Support**: Works across different Immich user accounts
- ✅ **Incremental Sync**: Only adds new photos, doesn't duplicate existing ones
- ✅ **Dry Run Mode**: Test configuration without making changes
- ✅ **Health Checks**: Built-in monitoring and error handling
- ✅ **Unraid Ready**: Includes Community Applications template

## Quick Start

Create shared albums for each account, something like *Partner Sharing (Person)*
Clone the repo
cp .env-example -> .env
Update the values in .env
docker compose up -d

### Example Configuration

```bash
IMMICH_SERVER=http://localhost:2283
SYNC_INTERVAL_MINUTES=60
SYNC_MAPPING_1=your-api-key-1:face-id-1:album-id-1:Photos of John
SYNC_MAPPING_2=your-api-key-2:face-id-2:album-id-2:Photos of Jane
SYNC_MAPPING_3=your-api-key-1:face-id-3:album-id-3:Photos of Kids
```

## Finding IDs

API Keys: Immich → Account Settings → API Keys → Create
Face IDs: Immich → Explore → People → Click person → Copy ID from URL
Album IDs: Immich → Albums → Click album → Copy ID from URL

## Use Cases

Partner Sharing: Automatically share photos of family members
Child Albums: Keep all photos of your children organized
Pet Albums: Organize photos of pets (if face detection picks them up)
Event Albums: Automatically populate albums with photos of specific people
Multi-User Families: Sync faces across different user accounts

## Configuration
All configuration is done via environment variables. See docker-compose.yml for full examples.

## Contributing

Fork the repository
Create a feature branch
Make your changes
Test thoroughly
Submit a pull request

## License
MIT License - feel free to use and modify!