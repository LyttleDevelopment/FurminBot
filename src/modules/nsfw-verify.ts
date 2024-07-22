import { MessageReaction, TextChannel, User } from 'discord.js';

const roleId = '1105151792662188073';
const checkRoleId = '842873737774235659';
const targetChannelId = '1105093487990415440';

async function nsfwVerify(reaction: MessageReaction, user: User) {
  const { message } = reaction;
  const guild = message.guild;

  if (
    !guild ||
    user.bot ||
    (message.channel as TextChannel).id !== targetChannelId
  )
    return;

  // Remove the reaction
  await reaction.users.remove(user.id);

  const member = await guild.members.fetch(user.id);
  const role = guild.roles.cache.get(roleId);
  const checkRole = guild.roles.cache.get(checkRoleId);
  if (!role || !checkRole) return;

  // if emoji is thumbs down add role otherwise remove role
  await member.roles.remove(checkRole);
  if (reaction.emoji.name === '👎') {
    await member.roles.add(role);
  }
}

export default nsfwVerify;
