import express from 'express';
import axios from 'axios';
import mongoose from 'mongoose';

const app = express();
app.use(express.json());

mongoose.connect('mongodb://localhost:27017/sentimentDB');

const sentimentSchema = new mongoose.Schema({
  text: String,
  prediction: String,
});
const Sentiment = mongoose.model('Sentiment', sentimentSchema);

app.post('/analyze', async (req, res) => {
  try {
    const { text } = req.body;
    const response = await axios.post('http://localhost:5001/predict', { text });
    const sentiment = new Sentiment({ text, prediction: response.data.prediction });
    await sentiment.save();
    res.json(sentiment);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(5000, () => console.log('Backend running on port 5000'));
