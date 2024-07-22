import { executor } from '../../utils';
import { actionPrefix } from './index';
import { MessageReaction, User } from 'discord.js';
import { GuildMember } from '../../types';
import verifyRules from '../../modules/verify-rules';
import roleButtons from '../../modules/role-buttons';

// This file's prefix
const prefix: string = actionPrefix + 'onGuildMessageReactionRemove.';

// The execute function
export async function onGuildMessageReactionRemove(
  guildMember: GuildMember,
  messageReaction: MessageReaction,
  user: User,
): Promise<void> {
  // All actions that should be executed
  const actions: Promise<() => void>[] = [
    executor(verifyRules, messageReaction, user, 'remove'),
    executor(roleButtons, messageReaction, user, 'remove'),
  ];

  // If no actions, return
  if (actions.length < 1) return;

  // Execute all actions
  await Promise.all(actions);
}
