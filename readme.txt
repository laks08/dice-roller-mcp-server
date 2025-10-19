# Dice Roller MCP Server

A Model Context Protocol (MCP) server that provides comprehensive dice rolling functionality for tabletop RPGs, D&D, and general gaming needs.

## Purpose

This MCP server provides a secure interface for AI assistants to roll dice, flip coins, and handle various tabletop gaming mechanics including D&D 5e advantage/disadvantage systems.

## Features

### Current Implementation

- **`roll_dice_notation`** - Roll dice using standard notation like '3d6', '1d20+5', or '2d8-1'
- **`flip_coin`** - Flip one or more coins and get heads/tails results
- **`roll_dnd_stats`** - Generate D&D ability scores using 4d6 drop lowest method
- **`roll_percentile`** - Roll d100 with flavor text for different ranges
- **`roll_advantage`** - Roll with advantage (twice, take higher) for D&D 5e
- **`roll_disadvantage`** - Roll with disadvantage (twice, take lower) for D&D 5e
- **`roll_custom_die`** - Roll a custom die with any number of sides (2-1000)

## Prerequisites

- Docker Desktop with MCP Toolkit enabled
- Docker MCP CLI plugin (`docker mcp` command)

## Installation

See the step-by-step instructions provided with the files.

## Usage Examples

In Claude Desktop, you can ask:

- "Roll 3d6 for damage"
- "Flip a coin"
- "Roll D&D stats for my new character"
- "Roll a d20 with advantage"
- "Roll percentile dice"
- "Roll 2d8+3 for healing"
- "Flip 5 coins"
- "Roll with disadvantage on stealth"
- "Roll a d100"

## Architecture

```
Claude Desktop → MCP Gateway → Dice Roller MCP Server → Random Number Generation
                                        ↓
                              Formatted Results with Emojis
```

## Development

### Local Testing

```bash
# Run directly
python dice_roller_server.py

# Test MCP protocol
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python dice_roller_server.py
```

### Adding New Tools

1. Add the function to `dice_roller_server.py`
2. Decorate with `@mcp.tool()`
3. Update the catalog entry with the new tool name
4. Rebuild the Docker image

## Troubleshooting

### Tools Not Appearing

- Verify Docker image built successfully
- Check catalog and registry files
- Ensure Claude Desktop config includes custom catalog
- Restart Claude Desktop

### Random Number Issues

- All randomization uses Python's built-in `random` module
- Seeds are automatically initialized
- No external dependencies required

## Security Considerations

- No external API calls or network access required
- Running as non-root user
- No sensitive data handling
- Pure mathematical operations only

## Dice Notation Support

The server supports standard tabletop gaming dice notation:

- `d6`, `1d6` - Single six-sided die
- `3d6` - Three six-sided dice
- `1d20+5` - Twenty-sided die plus 5
- `2d8-1` - Two eight-sided dice minus 1
- Maximum 100 dice per roll
- Maximum 1000 sides per die

## License

MIT License