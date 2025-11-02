# YGOMod Card Database Repository Structure

This repository provides external card data for the YGOMod Minecraft modification. Cards are organized by sets and can be loaded dynamically by the mod.

## Repository Structure

```
├── index.json              # Main repository index
├── sets/                   # Individual card sets
│   ├── LOB.json           # Legend of Blue-Eyes White Dragon
│   ├── MRD.json           # Metal Raiders  
│   ├── SRL.json           # Spell Ruler
│   ├── PSV.json           # Pharaoh's Servant
│   ├── LOD.json           # Legacy of Darkness
│   ├── LON.json           # Labyrinth of Nightmare
│   ├── PGD.json           # Pharaonic Guardian
│   └── MFC.json           # Magician's Force
├── cards/                  # Individual card files (optional)
│   ├── monsters/
│   ├── spells/
│   └── traps/
└── README.md
```

## Quick Start

1. Create the main index.json file
2. Create individual set files in the sets/ directory
3. Populate cards using YGOPRODeck API data
4. Update the mod configuration to point to your repository

## File Formats

### index.json
```json
{
  "repository_info": {
    "name": "YGOMod Official Card Database",
    "version": "1.0.0",
    "description": "Official card database for YGOMod",
    "last_updated": "2024-01-15T10:30:00Z"
  },
  "sets": [
    {
      "id": "LOB",
      "name": "Legend of Blue-Eyes White Dragon",
      "file": "sets/LOB.json",
      "card_count": 126,
      "release_date": "2002-03-08"
    }
  ]
}
```

### sets/LOB.json (Example Set File)
```json
{
  "set_info": {
    "id": "LOB",
    "name": "Legend of Blue-Eyes White Dragon", 
    "code": "LOB",
    "release_date": "2002-03-08",
    "card_count": 126
  },
  "cards": [
    {
      "id": 89631139,
      "name": "Blue-Eyes White Dragon",
      "type": "Normal Monster",
      "humanReadableCardType": "Normal Monster",
      "frameType": "normal",
      "description": "This legendary dragon is a powerful engine of destruction...",
      "attack": 3000,
      "defense": 2500,
      "level": 8,
      "race": "Dragon",
      "attribute": "LIGHT",
      "archetype": "Blue-Eyes",
      "images": {
        "artwork_url": "https://images.ygoprodeck.com/images/cards/89631139.jpg",
        "small_url": "https://images.ygoprodeck.com/images/cards_small/89631139.jpg",
        "cropped_url": "https://images.ygoprodeck.com/images/cards_cropped/89631139.jpg"
      },
      "mod_specific": {
        "rarity_tier": "legendary",
        "pack_weight": 0.01,
        "craftable": false,
        "unlock_condition": "rare_pack",
        "tags": ["iconic", "dragon", "classic", "light", "monster", "blue_eyes"]
      }
    }
  ]
}
```

## Card Schema

All cards must follow the standardized schema. See `card_schema_examples.json` for full documentation.

### Required Fields
- `id`: YGOPRODeck card ID
- `name`: Card name
- `type`: Card type
- `description`: Card effect/description text
- `images`: Image URLs object

### Monster-Specific Fields
- `attack`: ATK value
- `defense`: DEF value
- `level`: Level/Rank
- `race`: Monster type
- `attribute`: Monster attribute

### Mod-Specific Fields
- `mod_specific.rarity_tier`: "common", "rare", "epic", "legendary"
- `mod_specific.pack_weight`: Appearance probability (0.0-1.0)
- `mod_specific.craftable`: Whether craftable by players
- `mod_specific.unlock_condition`: Required pack/achievement
- `mod_specific.tags`: Searchable keywords array

## Adding New Cards

1. Get card data from YGOPRODeck API:
   ```
   https://db.ygoprodeck.com/api/v7/cardinfo.php?name=CARD_NAME
   ```

2. Convert to YGOMod format using the provided schema

3. Add to appropriate set file

4. Update set card count in index.json

## Repository URL Configuration

Add your repository to the mod config:
```json
{
  "repositories": [
    {
      "name": "Your Repository",
      "url": "https://raw.githubusercontent.com/USERNAME/REPO/main/",
      "enabled": true
    }
  ]
}
```

## API Integration

The card generator script (`card_generator.py`) can help automate the conversion process:

```bash
python card_generator.py "Blue-Eyes White Dragon" blue_eyes.json
```

## Notes

- All image URLs should use YGOPRODeck's CDN for consistency
- Cards must have valid YGOPRODeck IDs for compatibility
- Pack weights should sum to reasonable probabilities within sets
- Tags should be lowercase and use underscores for spaces