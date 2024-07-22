import { MessageReaction, TextChannel, User } from 'discord.js';

const roleId = '848677582065106944';
const targetChannelId = '848675484611248179';

async function verifyRules(
  reaction: MessageReaction,
  user: User,
  action: 'add' | 'remove',
) {
  const { message } = reaction;
  const guild = message.guild;

  if (
    !guild ||
    user.bot ||
    (message.channel as TextChannel).id !== targetChannelId
  )
    return;

  const member = await guild.members.fetch(user.id);
  const role = guild.roles.cache.get(roleId);
  if (!role) return;

  if (action === 'add') {
    await member.roles.add(role);
  } else if (action === 'remove') {
    await member.roles.remove(role);
  }
}

export default verifyRules;
