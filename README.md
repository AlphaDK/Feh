# AlphaDK's Feh for Discord

Hey, this is Feh. Originally made for Mike's Discord to link tweets, the bot evolved to be more interactive and useful.

Invite link is here: https://discordapp.com/oauth2/authorize?client_id=366885945846267906&scope=bot&permissions=0
The bot does not set up its own permissions, and it only requires Send Messages and Attach Files

YouTube guide/tutorial for the bot: Coming soon

Here's the current full list of features;

# Passive
-Will post any tweet made by @FEHeroes\_News or @FEHGauntletBot to #feheroes in Mike's Discord (Planned: Allow multiple channels)

-Will post at the daily reset time of 7AM UTC with a reminder of such to #feheroes (Also planned: Multiple channels)

-Will react to any post with the nerd emoji with the feh emoji. Very important feature.


# Active
-Quick info for Skills, Weapons, and Units\*! Type {{Quickened Pulse}} to get information on Quickened Pulse

\*Not all units supported yet but I'm getting there. Also planned: Listing units each skill is available from + inheritance restrictions

-!fehhelp: Basic help and information. (Planned: accept commands as arguments for specialised help)

-!report: Feedback command, this will message me with a copy of your message. This will also track your username and the channel it was reported in.

-@Feh what x: Saying "@Feh what " and then A Skill/Slot, B Skill/Slot, C Skill/Slot, or (Sacred) Seal, with any more message optional, will respond with a random one of those skills. ie AlphaDK: @Feh what seal should i put on hector. Feh: @AlphaDK Brash Assault 3

-!pet, !pat, !headpat, !halfpet: Pets Feh. Feh will thank you. It will also track the number of pats you've made. Half petting will add half a pat to your total. That's the difference.

-!checkpets, !checkpats: Tells you how many times you've pat Feh. Fairly simple.

-!sit: Copypasta about sitting for a few days before spending orbs.

-!6k: Copypasta about reaching 6,000 points in Tempest Trials

-!30k: Copypasta about reaching 30,000 points in Tempest Trials

-!selena: Copypasta about using Selena because you freaking like her

-!didntgetqp: Copypasta about missing Quickened Pulse by less than 100 points

-!draug, !knowyourdraug: Posts draug.jpg, an image informing you about the varities of Draug


# Most recent changelog

v1.4:

-Improved backend, preparing for useful public release

-Added comments like everywhere

-Moved auth codes out of main.py and into secret.py lol

-Changed !feh to !fehhelp for clarity

-Made the bot actually post at 7AM UTC instead of 6PM AEDT
