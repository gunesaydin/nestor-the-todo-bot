# nestor-the-todo-bot
A Telegram todo bot to my own liking. I didn't setup a DB for it since this was just a practice project to try out some libraries. Maybe I'll keep developing if I find it handy.

## Commands
- /start - Begin interaction
- /help - List commands and their descriptions
- /add - Add a new task (e.g. /add Buy stamps)
- /remove - Remove a task by index (e.g. /remove 2)
- /insert - Insert a task at a specific index (e.g. /insert 3 Wash the dishes)
- /list - List current tasks
- /whatnow - Show current task
- /done - Mark current task done
- /clear - Clear all tasks

## Setup
- You will need a Telegram Bot API token. You can get it from @BotFather in Telegram app by just messaging it.
- Project is setup to use dotenv for various credentials etc. You may want to add yours on your own.
- I am hosting the bot from my own computer via Ngrok. If you also choose to do so, you need to configure WEBHOOK_URL env variable. Or you can just host it (:
