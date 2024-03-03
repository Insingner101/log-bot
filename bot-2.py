import discord
from discord.ext import commands
import csv
from datetime import datetime

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

def log_to_csv(action, user, moderator):
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    with open('mod_log.csv', 'a', newline='') as csvfile:
        fieldnames = ['Timestamp', 'Action', 'User', 'Moderator']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:  
            writer.writeheader()

        writer.writerow({'Timestamp': timestamp, 'Action': action, 'User': user, 'Moderator': moderator})

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.event
async def on_member_remove(member):
    mod_log_channel_id = 1212741983328542761
    mod_log_channel = bot.get_channel(mod_log_channel_id)

    if member.guild.me.guild_permissions.view_audit_log:
        async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
            if entry.target == member:
                log_message = f"{member.display_name} has been kicked by {entry.user.display_name}"
                log_to_csv('Kick', member.display_name, entry.user.display_name)
                break
    else:
        log_message = f"{member.display_name} left the server (could not retrieve audit log)."

    await mod_log_channel.send(log_message)

@bot.event
async def on_member_ban(guild, user):
    mod_log_channel_id = 1212741983328542761
    mod_log_channel = bot.get_channel(mod_log_channel_id)

    if guild.me.guild_permissions.view_audit_log:
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            if entry.target == user:
                log_message = f"{user.display_name} has been banned by {entry.user.display_name}"
                log_to_csv('Ban', user.display_name, entry.user.display_name)
                break
    else:
        log_message = f"{user.display_name} has been banned (could not retrieve audit log)."

    await mod_log_channel.send(log_message)

@bot.event
async def on_member_unban(guild, user):
    mod_log_channel_id = 1212741983328542761
    mod_log_channel = bot.get_channel(mod_log_channel_id)

    if guild.me.guild_permissions.view_audit_log:
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.unban):
            if entry.target == user:
                log_message = f"{user.display_name} has been unbanned by {entry.user.display_name}"
                log_to_csv('Unban', user.display_name, entry.user.display_name)
                break
    else:
        log_message = f"{user.display_name} has been unbanned (could not retrieve audit log)."

    await mod_log_channel.send(log_message)

@bot.event
async def on_member_update(before, after):
    mod_log_channel_id = 1212741983328542761
    mod_log_channel = bot.get_channel(mod_log_channel_id)

    if not before.guild.me.guild_permissions.view_audit_log:
        return

    async for entry in before.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_update):
        if entry.target == before and before.roles != after.roles:
            if len(before.roles) > len(after.roles):
                log_message = f"{before.display_name} has been muted by {entry.user.display_name}"
                log_to_csv('Mute', before.display_name, entry.user.display_name)
            elif len(before.roles) < len(after.roles):
                log_message = f"{before.display_name} has been unmuted by {entry.user.display_name}"
                log_to_csv('Unmute', before.display_name, entry.user.display_name)
            else:
                return

            await mod_log_channel.send(log_message)
            break
#Replace without your token
bot.run('Place Your Token Here')
