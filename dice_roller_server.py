#!/usr/bin/env python3
"""
Simple Dice Roller MCP Server - Roll dice, flip coins, and handle D&D mechanics
"""
import os
import sys
import logging
import random
import re
from datetime import datetime, timezone
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("dice-roller-server")

# Initialize MCP server - NO PROMPT PARAMETER!
mcp = FastMCP("dice-roller")

# === UTILITY FUNCTIONS ===

def parse_dice_notation(notation):
    """Parse dice notation like '3d6', '1d20+5', '2d8-1'"""
    # Remove spaces and convert to lowercase
    notation = notation.replace(" ", "").lower()
    
    # Match patterns like 3d6, 1d20+5, 2d8-1
    pattern = r'^(\d+)?d(\d+)([+-]\d+)?$'
    match = re.match(pattern, notation)
    
    if not match:
        return None
    
    num_dice = int(match.group(1)) if match.group(1) else 1
    die_sides = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0
    
    return num_dice, die_sides, modifier

def roll_dice(num_dice, die_sides):
    """Roll multiple dice and return individual results"""
    return [random.randint(1, die_sides) for _ in range(num_dice)]

def format_roll_result(rolls, modifier, notation):
    """Format dice roll results nicely"""
    total = sum(rolls) + modifier
    rolls_str = " + ".join(map(str, rolls))
    
    if modifier > 0:
        return f"🎲 {notation}: [{rolls_str}] + {modifier} = **{total}**"
    elif modifier < 0:
        return f"🎲 {notation}: [{rolls_str}] - {abs(modifier)} = **{total}**"
    else:
        return f"🎲 {notation}: [{rolls_str}] = **{total}**"
# === MCP TOOLS ===

@mcp.tool()
async def roll_dice_notation(dice_notation: str = "") -> str:
    """Roll dice using standard notation like '3d6', '1d20+5', or '2d8-1'."""
    logger.info(f"Rolling dice with notation: {dice_notation}")
    
    if not dice_notation.strip():
        return "❌ Error: Please provide dice notation (e.g., '3d6', '1d20+5', '2d8-1')"
    
    try:
        parsed = parse_dice_notation(dice_notation.strip())
        if not parsed:
            return f"❌ Error: Invalid dice notation '{dice_notation}'. Use format like '3d6', '1d20+5', or '2d8-1'"
        
        num_dice, die_sides, modifier = parsed
        
        if num_dice > 100:
            return "❌ Error: Maximum 100 dice per roll"
        if die_sides > 1000:
            return "❌ Error: Maximum 1000 sides per die"
        
        rolls = roll_dice(num_dice, die_sides)
        return format_roll_result(rolls, modifier, dice_notation.strip())
        
    except Exception as e:
        logger.error(f"Error rolling dice: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def flip_coin(count: str = "1") -> str:
    """Flip one or more coins and return heads/tails results."""
    logger.info(f"Flipping {count} coin(s)")
    
    try:
        num_flips = int(count) if count.strip() else 1
        
        if num_flips < 1:
            return "❌ Error: Must flip at least 1 coin"
        if num_flips > 100:
            return "❌ Error: Maximum 100 coins per flip"
        
        results = []
        heads_count = 0
        
        for _ in range(num_flips):
            result = "Heads" if random.randint(0, 1) else "Tails"
            results.append(result)
            if result == "Heads":
                heads_count += 1
        
        if num_flips == 1:
            emoji = "🪙" if results[0] == "Heads" else "🥈"
            return f"{emoji} **{results[0]}**"
        else:
            tails_count = num_flips - heads_count
            results_str = ", ".join(results)
            return f"🪙 Flipped {num_flips} coins: {results_str}\n📊 Summary: {heads_count} Heads, {tails_count} Tails"
            
    except ValueError:
        return f"❌ Error: Invalid count '{count}'. Please use a number."
    except Exception as e:
        logger.error(f"Error flipping coin: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def roll_dnd_stats() -> str:
    """Roll D&D ability scores using 4d6 drop lowest method."""
    logger.info("Rolling D&D ability scores")
    
    try:
        stats = []
        stat_names = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
        
        for stat_name in stat_names:
            # Roll 4d6, drop lowest
            rolls = roll_dice(4, 6)
            rolls.sort(reverse=True)
            kept_rolls = rolls[:3]
            total = sum(kept_rolls)
            stats.append((stat_name, total, kept_rolls))
        
        result = "🎲 **D&D Ability Scores** (4d6 drop lowest):\n\n"
        total_modifier = 0
        
        for stat_name, total, kept_rolls in stats:
            modifier = (total - 10) // 2
            modifier_str = f"+{modifier}" if modifier >= 0 else str(modifier)
            total_modifier += modifier
            
            result += f"**{stat_name}**: {total} ({modifier_str}) - Rolled: {kept_rolls}\n"
        
        result += f"\n📊 **Total Modifier**: {'+' if total_modifier >= 0 else ''}{total_modifier}"
        return result
        
    except Exception as e:
        logger.error(f"Error rolling D&D stats: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def roll_percentile() -> str:
    """Roll percentile dice (d100) for D&D and other RPG systems."""
    logger.info("Rolling percentile dice")
    
    try:
        result = random.randint(1, 100)
        
        # Add some flavor text for common ranges
        if result == 100:
            flavor = " 🎉 Perfect!"
        elif result >= 95:
            flavor = " ⭐ Excellent!"
        elif result >= 80:
            flavor = " 👍 Great!"
        elif result >= 60:
            flavor = " ✅ Good"
        elif result >= 40:
            flavor = " 😐 Average"
        elif result >= 20:
            flavor = " 👎 Poor"
        elif result <= 5:
            flavor = " 💀 Critical Failure!"
        else:
            flavor = " 😬 Bad"
        
        return f"🎲 **Percentile Roll**: {result}%{flavor}"
        
    except Exception as e:
        logger.error(f"Error rolling percentile: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def roll_advantage(dice_notation: str = "1d20") -> str:
    """Roll with advantage (roll twice, take higher) - common in D&D 5e."""
    logger.info(f"Rolling with advantage: {dice_notation}")
    
    if not dice_notation.strip():
        dice_notation = "1d20"
    
    try:
        parsed = parse_dice_notation(dice_notation.strip())
        if not parsed:
            return f"❌ Error: Invalid dice notation '{dice_notation}'. Use format like '1d20', '1d8+3'"
        
        num_dice, die_sides, modifier = parsed
        
        if num_dice != 1:
            return "❌ Error: Advantage rolls work with single dice only (e.g., '1d20+5')"
        
        # Roll twice
        roll1 = random.randint(1, die_sides)
        roll2 = random.randint(1, die_sides)
        
        # Take the higher roll
        higher_roll = max(roll1, roll2)
        total = higher_roll + modifier
        
        if modifier > 0:
            return f"🎲 **Advantage** {dice_notation}: [{roll1}, {roll2}] → {higher_roll} + {modifier} = **{total}**"
        elif modifier < 0:
            return f"🎲 **Advantage** {dice_notation}: [{roll1}, {roll2}] → {higher_roll} - {abs(modifier)} = **{total}**"
        else:
            return f"🎲 **Advantage** {dice_notation}: [{roll1}, {roll2}] → **{higher_roll}**"
        
    except Exception as e:
        logger.error(f"Error rolling with advantage: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def roll_disadvantage(dice_notation: str = "1d20") -> str:
    """Roll with disadvantage (roll twice, take lower) - common in D&D 5e."""
    logger.info(f"Rolling with disadvantage: {dice_notation}")
    
    if not dice_notation.strip():
        dice_notation = "1d20"
    
    try:
        parsed = parse_dice_notation(dice_notation.strip())
        if not parsed:
            return f"❌ Error: Invalid dice notation '{dice_notation}'. Use format like '1d20', '1d8+3'"
        
        num_dice, die_sides, modifier = parsed
        
        if num_dice != 1:
            return "❌ Error: Disadvantage rolls work with single dice only (e.g., '1d20+5')"
        
        # Roll twice
        roll1 = random.randint(1, die_sides)
        roll2 = random.randint(1, die_sides)
        
        # Take the lower roll
        lower_roll = min(roll1, roll2)
        total = lower_roll + modifier
        
        if modifier > 0:
            return f"🎲 **Disadvantage** {dice_notation}: [{roll1}, {roll2}] → {lower_roll} + {modifier} = **{total}**"
        elif modifier < 0:
            return f"🎲 **Disadvantage** {dice_notation}: [{roll1}, {roll2}] → {lower_roll} - {abs(modifier)} = **{total}**"
        else:
            return f"🎲 **Disadvantage** {dice_notation}: [{roll1}, {roll2}] → **{lower_roll}**"
        
    except Exception as e:
        logger.error(f"Error rolling with disadvantage: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def roll_custom_die(sides: str = "6") -> str:
    """Roll a custom die with specified number of sides."""
    logger.info(f"Rolling custom d{sides}")
    
    try:
        num_sides = int(sides) if sides.strip() else 6
        
        if num_sides < 2:
            return "❌ Error: Die must have at least 2 sides"
        if num_sides > 1000:
            return "❌ Error: Maximum 1000 sides per die"
        
        result = random.randint(1, num_sides)
        return f"🎲 **d{num_sides}**: {result}"
        
    except ValueError:
        return f"❌ Error: Invalid number of sides '{sides}'. Please use a number."
    except Exception as e:
        logger.error(f"Error rolling custom die: {e}")
        return f"❌ Error: {str(e)}"

# === SERVER STARTUP ===
if __name__ == "__main__":
    logger.info("Starting Dice Roller MCP server...")
    
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)