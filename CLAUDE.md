# Dice Roller MCP Server - Claude Integration Guide

## Overview

This MCP server provides comprehensive dice rolling functionality for tabletop RPGs and gaming. It's designed to work seamlessly with Claude Desktop through the MCP Gateway.

## Available Tools

### Core Dice Rolling

- `roll_dice_notation` - Standard dice notation (3d6, 1d20+5, etc.)
- `roll_custom_die` - Roll any die with 2-1000 sides
- `roll_percentile` - Roll d100 with flavor text

### Coin Flipping

- `flip_coin` - Flip 1-100 coins with summary statistics

### D&D 5e Specific

- `roll_dnd_stats` - Generate ability scores (4d6 drop lowest)
- `roll_advantage` - Roll twice, take higher result
- `roll_disadvantage` - Roll twice, take lower result

## Implementation Details

### Error Handling

- All tools return user-friendly error messages
- Input validation prevents invalid dice configurations
- Graceful handling of edge cases

### Output Formatting

- Uses emojis for visual clarity (🎲, 🪙, ⭐, etc.)
- Bold formatting for important results
- Clear breakdown of individual rolls and modifiers

### Performance Considerations

- No external API calls required
- Pure mathematical operations
- Minimal memory footprint
- Fast response times

## Usage Patterns

### Natural Language Examples

Users can ask Claude:

- "Roll initiative for my rogue" → Uses roll_dice_notation with "1d20"
- "Generate stats for a new character" → Uses roll_dnd_stats
- "Flip a coin to decide" → Uses flip_coin
- "Roll damage for my sword" → Uses roll_dice_notation with appropriate dice

### Direct Tool Usage

- Simple rolls: `roll_dice_notation("1d20+3")`
- Advantage: `roll_advantage("1d20+5")`
- Stats: `roll_dnd_stats()` (no parameters needed)

## Security Notes

- No network access required
- No file system access
- No external dependencies beyond Python standard library
- Runs in isolated Docker container
- Non-root user execution

## Troubleshooting

### Common Issues

1. **Tools not appearing**: Restart Claude Desktop after configuration
2. **Invalid notation**: Use standard format like "3d6" or "1d20+5"
3. **Large numbers**: Limited to 100 dice and 1000 sides for performance

### Debugging

- Check Docker logs for server errors
- Verify MCP Gateway configuration
- Test individual tools with simple inputs first

## Extension Ideas

Future enhancements could include:

- Dice pools (count successes)
- Exploding dice mechanics
- Fate/Fudge dice support
- Custom dice tables
- Roll history tracking
- Probability calculations

## Best Practices

### For Users

- Use clear, standard dice notation
- Start with simple rolls before complex ones
- Ask for help with notation if unsure

### For Developers

- All tools return strings (required by MCP)
- Single-line docstrings only
- Empty string defaults, not None
- Comprehensive error handling
- Clear, formatted output
