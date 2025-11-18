import discord, asyncio, os
from discord.ext import commands, tasks

TOKEN = os.environ["TOKEN"]

ROLE_NAMES = ["💅Csajos💅", "⚠️IMPOSTOR⚠️", "👀"]
WAIT_TIME = 86400  # alapértelmezett: 24 óra
LOG_CHANNEL_ID = 1434206542131101810  # ide írd a szoba ID-ját

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True  # Parancsok olvasásához szükséges!
bot = commands.Bot(command_prefix="!", intents=intents)

@tasks.loop(hours=5)
async def auto_check_members():
    """Automatikusan ellenőrzi az összes tagot 5 óránként"""
    print("🔄 Automatikus tag-ellenőrzés indítása...")
    
    for guild in bot.guilds:
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        
        kicked_count = 0
        safe_count = 0
        error_count = 0
        
        for member in guild.members:
            if member.bot:
                continue
                
            has_role = any(
                discord.utils.get(guild.roles, name=role_name) in member.roles
                for role_name in ROLE_NAMES
            )
            
            if not has_role:
                try:
                    await member.kick(reason="Nincs megadott szerepe (automatikus ellenőrzés)")
                    kicked_count += 1
                    msg = f"❌ {member.mention} ki lett léptetve (automatikus ellenőrzés - nem volt szerepe)."
                    print(msg)
                    if log_channel:
                        await log_channel.send(msg)
                except discord.Forbidden:
                    error_count += 1
                    warn = f"⚠️ Nincs jogom kirúgni: {member}"
                    print(warn)
                except Exception as e:
                    error_count += 1
                    print(f"⚠️ Hiba történt {member} kirúgása közben: {e}")
            else:
                safe_count += 1
        
        summary = f"""
🔄 **Automatikus ellenőrzés befejezve** ({guild.name})
👥 Megtartott tagok: {safe_count}
❌ Kirúgott tagok: {kicked_count}
⚠️ Hibák: {error_count}
"""
        print(summary)
        if log_channel and (kicked_count > 0 or error_count > 0):
            await log_channel.send(summary)

@auto_check_members.before_loop
async def before_auto_check():
    """Megvárja, amíg a bot teljesen bejelentkezik"""
    await bot.wait_until_ready()

@bot.tree.command(name="pingg", description="Válaszol Pong!")
async def pingg(interaction: discord.Interaction):
    """Slash parancs: /pingg - Válaszol Pong!"""
    await interaction.response.send_message("Pong!")

@bot.event
async def on_ready():
    print(f"✅ Bot bejelentkezett: {bot.user}")
    print(f"⏳ Jelenlegi várakozási idő: {WAIT_TIME/60:.1f} perc")
    print(f"🔄 Automatikus ellenőrzés: 5 óránként")
    
    # Slash parancsok szinkronizálása
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} slash parancs szinkronizálva")
    except Exception as e:
        print(f"⚠️ Hiba a slash parancsok szinkronizálása során: {e}")
    
    if not auto_check_members.is_running():
        auto_check_members.start()

@bot.command()
@commands.has_permissions(administrator=True)
async def time(ctx, percek: int):
    """Kick idő beállítása percben (pl. !time 10)"""
    global WAIT_TIME
    WAIT_TIME = percek * 60
    await ctx.send(f"✅ Kick idő módosítva: {percek} perc ({WAIT_TIME} másodperc).")

@bot.command()
@commands.has_permissions(administrator=True)
async def settime(ctx, amount: int, unit: str):
    """Kick idő beállítása időegységgel (pl. !settime 2 óra)"""
    allowed_channel_id = 1434206542131101810
    
    if ctx.channel.id != allowed_channel_id:
        await ctx.send("❌ Ezt a parancsot csak a kijelölt parancs-csatornában használhatod!")
        return
    
    global WAIT_TIME
    unit_lower = unit.lower()
    
    if unit_lower in ["perc", "percek", "minute", "minutes", "min", "m"]:
        WAIT_TIME = amount * 60
        unit_display = "perc"
    elif unit_lower in ["óra", "órák", "ora", "orak", "hour", "hours", "h"]:
        WAIT_TIME = amount * 3600
        unit_display = "óra"
    elif unit_lower in ["nap", "napok", "day", "days", "d"]:
        WAIT_TIME = amount * 86400
        unit_display = "nap"
    elif unit_lower in ["másodperc", "másodpercek", "masodperc", "masodpercek", "second", "seconds", "sec", "s"]:
        WAIT_TIME = amount
        unit_display = "másodperc"
    else:
        await ctx.send(f"❌ Ismeretlen időegység: `{unit}`. Használd: perc, óra, nap, másodperc")
        return
    
    await ctx.send(f"✅ Kick idő módosítva: {amount} {unit_display} ({WAIT_TIME} másodperc)")
    print(f"⏰ Várakozási idő beállítva: {amount} {unit_display} ({WAIT_TIME} mp)")

@bot.command()
@commands.has_permissions(administrator=True)
async def checkall(ctx):
    """Végignézi az összes tagot és kirúgja, akiknek nincs megadott szerepe"""
    await ctx.send("🔍 Ellenőrzés indítása... Végignézem az összes tagot.")
    
    guild = ctx.guild
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    
    kicked_count = 0
    safe_count = 0
    error_count = 0
    
    # Végigmegyünk az összes tagon
    for member in guild.members:
        # Botokat és a parancsot kiadó admint kihagyjuk
        if member.bot:
            continue
            
        # Ellenőrizzük, van-e neki valamelyik szerep
        has_role = any(
            discord.utils.get(guild.roles, name=role_name) in member.roles
            for role_name in ROLE_NAMES
        )
        
        if not has_role:
            try:
                await member.kick(reason="Nincs megadott szerepe (tömeges ellenőrzés)")
                kicked_count += 1
                msg = f"❌ {member.mention} ki lett léptetve (nem volt szerepe)."
                print(msg)
                if log_channel:
                    await log_channel.send(msg)
            except discord.Forbidden:
                error_count += 1
                warn = f"⚠️ Nincs jogom kirúgni: {member}"
                print(warn)
                if log_channel:
                    await log_channel.send(warn)
            except Exception as e:
                error_count += 1
                print(f"⚠️ Hiba történt {member} kirúgása közben: {e}")
        else:
            safe_count += 1
    
    # Összesítés
    summary = f"""
✅ **Ellenőrzés befejezve!**
👥 Megtartott tagok (van szerepük): {safe_count}
❌ Kirúgott tagok: {kicked_count}
⚠️ Hibák: {error_count}
"""
    await ctx.send(summary)
    print(summary)

@bot.event
async def on_member_join(member):
    print(f"👤 {member} belépett a szerverre.")
    await asyncio.sleep(WAIT_TIME)

    has_role = any(
        discord.utils.get(member.guild.roles, name=role_name) in member.roles
        for role_name in ROLE_NAMES
    )

    log_channel = bot.get_channel(LOG_CHANNEL_ID)

    if not has_role:
        try:
            await member.kick(reason=f"Nincs megadott szerepe {WAIT_TIME/60:.1f} perc után.")
            msg = f"❌ {member.mention} ki lett léptetve (nem kapott szerepet {WAIT_TIME/60:.1f} perc alatt)."
            print(msg)
            if log_channel:
                await log_channel.send(msg)
        except discord.Forbidden:
            warn = f"⚠️ Nincs jogom kirúgni: {member}"
            print(warn)
            if log_channel:
                await log_channel.send(warn)
    else:
        ok = f"✅ {member.mention} megtarthatta a helyét (volt szerepe)."
        print(ok)
        if log_channel:
            await log_channel.send(ok)

bot.run(TOKEN)
