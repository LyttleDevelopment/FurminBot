import { MessageReaction, TextChannel, User } from 'discord.js';
import { loadJson } from '../utils/load-json';
import client from '../main';

const targetChannelId = '848995808317407252';
const nsfwRoleId = '842873737774235659';
const nsfwEmojiId = '809136459868798976';
const adminChannelId = '802288905599975444';

// Emitted when the client becomes ready to start working.
async function roleButtons(
  reaction: MessageReaction,
  user: User,
  action: 'add' | 'remove',
) {
  const { message, emoji } = reaction;
  const guild = message.guild;

  if (!guild) return;

  const channel = guild.channels.cache.get(message.channelId) as TextChannel;
  if (!channel) return;

  if (
    user.bot ||
    (channel.id !== targetChannelId && channel.id !== adminChannelId)
  )
    return;

  const member = await guild.members.fetch(user.id);
  if (!member) return;

  const adminChannel = client.channels.cache.get(adminChannelId) as TextChannel;

  if (action === 'add') {
    if (message.channelId === adminChannelId) {
      const msg = await channel.messages.fetch(message.id);
      const userIdMatch = msg.content.match(/\|\|ID:(\d+)\|\|/);
      if (userIdMatch) {
        const targetMember = await guild.members.fetch(userIdMatch[1]);
        const role = guild.roles.cache.get(nsfwRoleId);
        if (role) {
          await targetMember.roles.add(role);
          await adminChannel.send(
            `<@${user.id}> gave the NSFW role to <@${userIdMatch[1]}>`,
          );
        }
      }
      return;
    }

    if (emoji.id === nsfwEmojiId) {
      await adminChannel.send(
        `<@${user.id}> requested the NSFW role? Going to give that?` +
          `\nIf yes, react with any emoji to this message. ||ID:${user.id}||`,
      );
      return;
    }

    const roles = loadJson('role_buttons');
    console.log(roles);
    const roleId = roles[emoji.id];
    const role = guild.roles.cache.get(roleId);
    if (role) {
      await member.roles.add(role);
    }
  } else if (action === 'remove') {
    if (emoji.id === nsfwEmojiId) {
      const role = guild.roles.cache.get(nsfwRoleId);
      if (role) {
        await member.roles.remove(role);
      }
      return;
    }

    const roles = loadJson('role_buttons');
    const roleId = roles[emoji.id];
    const role = guild.roles.cache.get(roleId);
    if (role) {
      await member.roles.remove(role);
    }
  }
}

export default roleButtons;
