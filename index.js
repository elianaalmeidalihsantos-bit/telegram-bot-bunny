const TelegramBot = require('node-telegram-bot-api');
const axios = require('axios');
const FormData = require('form-data');

const bot = new TelegramBot(process.env.BOT_TOKEN, { polling: true });

bot.on('message', async (msg) => {
  try {
    const media =
      msg.video ||
      msg.document ||
      (msg.channel_post && msg.channel_post.video);

    if (!media) {
      bot.sendMessage(msg.chat.id, 'Envie um vídeo 🎥');
      return;
    }

    bot.sendMessage(msg.chat.id, 'Recebi o vídeo. Enviando para o Bunny...');

    const fileId = media.file_id;

    const fileLink = await bot.getFileLink(fileId);

    const videoResponse = await axios.get(fileLink, {
      responseType: 'stream',
    });

    const createVideo = await axios.post(
      `https://video.bunnycdn.com/library/${process.env.BUNNY_LIBRARY_ID}/videos`,
      {
        title: `video-${Date.now()}`
      },
      {
        headers: {
          AccessKey: process.env.BUNNY_API_KEY,
          'Content-Type': 'application/json'
        }
      }
    );

    const videoId = createVideo.data.guid;

    const form = new FormData();
    form.append('file', videoResponse.data);

    await axios.put(
      `https://video.bunnycdn.com/library/${process.env.BUNNY_LIBRARY_ID}/videos/${videoId}`,
      videoResponse.data,
      {
        headers: {
          AccessKey: process.env.BUNNY_API_KEY,
          'Content-Type': 'application/octet-stream'
        },
        maxBodyLength: Infinity,
      }
    );

    bot.sendMessage(
      msg.chat.id,
      `Upload concluído 🚀\nID: ${videoId}`
    );

  } catch (err) {
    console.log(err.response?.data || err.message);

    bot.sendMessage(
      msg.chat.id,
      'Erro ao enviar para o Bunny.'
    );
  }
});
