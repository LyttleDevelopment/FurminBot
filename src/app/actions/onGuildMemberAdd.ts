import { actionPrefix } from './index';
import { GuildMember } from 'discord.js';
import { GuildMember as ClientGuildMember } from '../../types';
import { executor } from '../../utils';
import welcoming from '../../modules/welcoming';

// This file's prefix
const prefix: string = actionPrefix + 'onGuildMemberAdd.';

// The execute function
export async function onGuildMemberAdd(
  guildMember: ClientGuildMember,
  member: GuildMember,
): Promise<void> {
  // All actions that should be executed
  const actions: Promise<() => void>[] = [executor(welcoming, guildMember)];

  // If no actions, return
  if (actions.length < 1) return;

  // Execute all actions
  await Promise.all(actions);
}
