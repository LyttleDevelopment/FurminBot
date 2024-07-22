import { EmbedBuilder, GuildMember, TextChannel } from 'discord.js';
import client from '../main';

// Emitted when the client becomes ready to start working.
async function welcoming(member: GuildMember): Promise<void> {
  if (member.guild.id !== '768870930385469501') {
    return;
  }

  const welcomingChannel = client.channels.cache.get(
    '848670878137057290',
  ) as TextChannel;
  if (!welcomingChannel) {
    console.error('Welcoming channel not found');
    return;
  }

  const embed = new EmbedBuilder()
    .setTitle(
      `Welcome ${member.user.tag} to the Bestie of Friend's discord server!`,
    )
    .setDescription(
      'To begin, read the <#848675484611248179>. ' +
        'If you want any tags go to <#848995808317407252> ' +
        'and assign them to yourself! ' +
        'Good luck and welcome to our nice community.',
    )
    .setColor(0x007db3);
  // .setImage(`https://f.lyttle.it/${nr}.gif`);

  await welcomingChannel.send({ embeds: [embed] });
}

export default welcoming;
