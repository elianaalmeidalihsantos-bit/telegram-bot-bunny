const TelegramBot = require('node-telegram-bot-api');
const axios = require('axios');

const bot = new TelegramBot(process.env.BOT_TOKEN, { polling: true });

const BUNNY_API_KEY = process.env.CHAVE_API_BUNNY;
const BUNNY_LIBRARY_ID = process.env.ID_DA_BIBLIOTECA_DO_COELHO;

bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id, 'Bot online.');
});

bot.on('message', async (msg) => {
  try {
    if (!msg.video) return;

    await bot.sendMessage(msg.chat.id, 'Recebi o vídeo. Enviando para o Bunny...');

    const fileLink = await bot.getFileLink(msg.video.file_id);
    const title = msg.caption || `video-${msg.message_id}`;

    const create = await axios.post(
      `https://video.bunnycdn.com/library/${BUNNY_LIBRARY_ID}/videos`,
      { title },
      { headers: { AccessKey: BUNNY_API_KEY, 'Content-Type': 'application/json' } }
    );

    const videoId = create.data.guid;

    const videoStream = await axios.get(fileLink, { responseType: 'stream' });

    await axios.put(
      `https://video.bunnycdn.com/library/${BUNNY_LIBRARY_ID}/videos/${videoId}`,
      videoStream.data,
      { headers: { AccessKey: BUNNY_API_KEY, 'Content-Type': 'application/octet-stream' } }
    );

    await bot.sendMessage(msg.chat.id, `Enviado para o Bunny. ID: ${videoId}`);
  } catch (err) {
    console.error(err.response?.data || err.message);
    bot.sendMessage(msg.chat.id, 'Erro ao enviar para o Bunny.');
  }
});
