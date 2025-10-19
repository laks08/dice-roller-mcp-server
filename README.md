# 🎲 Dice Roller MCP Server

A comprehensive Model Context Protocol (MCP) server that brings tabletop gaming dice mechanics directly to Claude Desktop. Roll dice, flip coins, and handle D&D 5e mechanics with natural language commands.

## ✨ Features

### 🎯 Core Dice Rolling

- **Standard Notation**: Roll using familiar formats like `3d6`, `1d20+5`, `2d8-1`
- **Custom Dice**: Roll any die from 2 to 1000 sides
- **Percentile Rolls**: d100 with contextual flavor text

### 🪙 Coin Flipping

- Single or multiple coin flips (up to 100)
- Automatic statistics for multiple flips

### 🐉 D&D 5e Mechanics

- **Ability Score Generation**: 4d6 drop lowest method
- **Advantage/Disadvantage**: Roll twice, take higher/lower
- **Complete modifier calculations**

### 🎨 Rich Output

- Emoji-enhanced results (🎲, 🪙, ⭐, 💀)
- Bold formatting for important numbers
- Detailed breakdowns of individual rolls
- Contextual flavor text for percentile rolls

## 🚀 Quick Start

### Prerequisites

- Docker Desktop
- Claude Desktop
- Docker MCP Toolkit

### Installation

1. **Clone and build the server:**

   ```bash
   git clone <your-repo>
   cd dice-roller-mcp-server
   docker build -t dice-roller-mcp .
   ```

2. **Set up MCP configuration:**

   Create or update `~/.docker/mcp/registry.yaml`:

   ```yaml
   registry:
     dice-roller:
       ref: "dice-roller-mcp:latest"
   ```

   Create or update `~/.docker/mcp/catalogs/custom.yaml`:

   ```yaml
   version: 2
   name: custom
   displayName: Custom MCP Servers
   registry:
     dice-roller:
       description: "Roll dice, flip coins, and handle D&D mechanics"
       title: "Dice Roller"
       type: server
       image: dice-roller-mcp:latest
       tools:
         - name: roll_dice_notation
         - name: flip_coin
         - name: roll_dnd_stats
         - name: roll_percentile
         - name: roll_advantage
         - name: roll_disadvantage
         - name: roll_custom_die
       metadata:
         category: productivity
         tags: [gaming, dice, dnd, rpg]
   ```

3. **Configure Claude Desktop:**

   Update `~/Library/Application Support/Claude/claude_desktop_config.json`:

   ```json
   {
     "mcpServers": {
       "mcp-toolkit-gateway": {
         "command": "docker",
         "args": [
           "run",
           "-i",
           "--rm",
           "-v",
           "/var/run/docker.sock:/var/run/docker.sock",
           "-v",
           "/Users/[YOUR_USERNAME]/.docker/mcp:/mcp",
           "docker/mcp-gateway",
           "--catalog=/mcp/catalogs/custom.yaml",
           "--registry=/mcp/registry.yaml",
           "--transport=stdio"
         ]
       }
     }
   }
   ```

   Replace `[YOUR_USERNAME]` with your actual username.

4. **Restart Claude Desktop**

## 🎮 Usage Examples

Once configured, you can use natural language with Claude:

### Basic Dice Rolling

- _"Roll 3d6 for damage"_
- _"Roll a d20 for initiative"_
- _"Roll 2d8+3 for healing"_

### D&D Character Creation

- _"Generate ability scores for my new character"_
- _"Roll stats using 4d6 drop lowest"_

### Combat Mechanics

- _"Roll a d20 with advantage for my attack"_
- _"Roll stealth with disadvantage"_
- _"Roll a percentile for wild magic"_

### Utility Rolls

- _"Flip a coin to decide"_
- _"Roll a d100"_
- _"Flip 5 coins and tell me the results"_

## 🛠️ Available Tools

| Tool                 | Description            | Example Usage            |
| -------------------- | ---------------------- | ------------------------ |
| `roll_dice_notation` | Standard dice notation | `3d6`, `1d20+5`, `2d8-1` |
| `roll_custom_die`    | Custom sided die       | `d13`, `d47`, `d1000`    |
| `flip_coin`          | Coin flipping          | `1` coin or `10` coins   |
| `roll_percentile`    | d100 with flavor       | Automatic flavor text    |
| `roll_dnd_stats`     | D&D ability scores     | 4d6 drop lowest × 6      |
| `roll_advantage`     | D&D advantage          | Roll twice, take higher  |
| `roll_disadvantage`  | D&D disadvantage       | Roll twice, take lower   |

## 🔧 Development

### Local Testing

```bash
# Test the server directly (requires mcp package)
python3 dice_roller_server.py

# Test with Docker
docker run --rm -i dice-roller-mcp

# Verify MCP tools
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | docker run --rm -i dice-roller-mcp
```

### Adding New Features

1. Add new tool function to `dice_roller_server.py`
2. Decorate with `@mcp.tool()`
3. Update catalog with new tool name
4. Rebuild Docker image
5. Restart Claude Desktop

## 🔒 Security Features

- **No Network Access**: Pure mathematical operations only
- **Input Validation**: Prevents malicious or excessive inputs
- **Resource Limits**: Max 100 dice, 1000 sides per die
- **Non-Root Execution**: Runs as unprivileged user in container
- **No File System Access**: Stateless operation

## 🎯 Dice Notation Reference

| Format  | Description        | Example                       |
| ------- | ------------------ | ----------------------------- |
| `dX`    | Single die         | `d6` = roll 1d6               |
| `NdX`   | Multiple dice      | `3d6` = roll 3 six-sided dice |
| `NdX+Y` | Dice with modifier | `1d20+5` = d20 plus 5         |
| `NdX-Y` | Dice with penalty  | `2d8-1` = 2d8 minus 1         |

**Limits:**

- Maximum 100 dice per roll
- Maximum 1000 sides per die
- Modifiers: -999 to +999

## 🎨 Output Examples

### Standard Roll

```
🎲 3d6+2: [4, 2, 6] + 2 = **14**
```

### Advantage Roll

```
🎲 **Advantage** 1d20+3: [8, 15] → 15 + 3 = **18**
```

### D&D Stats

```
🎲 **D&D Ability Scores** (4d6 drop lowest):

**Strength**: 15 (+2) - Rolled: [6, 5, 4]
**Dexterity**: 12 (+1) - Rolled: [4, 4, 4]
...
📊 **Total Modifier**: +8
```

### Percentile with Flavor

```
🎲 **Percentile Roll**: 95% ⭐ Excellent!
```

## 🐛 Troubleshooting

### Tools Not Appearing

1. Verify Docker image built successfully: `docker images | grep dice-roller`
2. Check MCP configuration files for syntax errors
3. Ensure Claude Desktop config points to correct username path
4. Restart Claude Desktop completely

### Connection Issues

1. Verify Docker MCP Gateway is running: `docker mcp server list`
2. Check Docker socket permissions
3. Validate YAML syntax in config files

### Invalid Dice Notation

- Use standard format: `3d6`, `1d20+5`
- Check for typos in dice notation
- Ensure numbers are within limits

## Acknowledgments

This project was inspired by and built following the excellent tutorial by **NetworkChuck**. His video provided the foundation and guidance for creating MCP servers with Docker integration.

- **NetworkChuck YouTube Channel**: [https://www.youtube.com/@NetworkChuck](https://www.youtube.com/@NetworkChuck)
- **Tutorial Reference**: you need to learn MCP RIGHT NOW!! (Model Context Protocol)

Special thanks to NetworkChuck for making complex concepts accessible and inspiring developers to build cool projects!

## 📄 License

MIT License - Feel free to modify and distribute!

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

---

_Happy rolling! 🎲_

_Built with guidance from NetworkChuck's tutorials_
