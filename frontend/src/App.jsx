// import React, { useState } from 'react';
// import axios from 'axios';
// import { Pie } from 'react-chartjs-2';
// import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

// ChartJS.register(ArcElement, Tooltip, Legend);

// const App = () => {
//   const [url, setUrl] = useState('');
//   const [sentimentData, setSentimentData] = useState(null);
//   const [error, setError] = useState('');

//   const handleAnalyze = async () => {
//     setError('');
//     setSentimentData(null);
//     try {
//       const response = await axios.post('http://127.0.0.1:5001/predict', { url }, {
//         headers: {
//           'Content-Type': 'application/json',
//         },
//       });

//       const sentimentCounts = response.data.sentiment_counts;
//       if (sentimentCounts && sentimentCounts.Positive !== undefined && sentimentCounts.Negative !== undefined) {
//         setSentimentData(response.data);
//       } else {
//         throw new Error('Invalid response format from backend');
//       }
//     } catch (err) {
//       console.error('Error details:', err); // Log the full error for debugging
//       setError('Error fetching or analyzing reviews. Please check the URL or try again later.');
//     }
//   };

//   const chartData = sentimentData && {
//     labels: ['Positive', 'Negative', 'Neutral'], // Added Neutral
//     datasets: [
//       {
//         data: [
//           sentimentData.sentiment_counts.Positive,
//           sentimentData.sentiment_counts.Negative,
//           sentimentData.sentiment_counts.Neutral, // Added Neutral
//         ],
//         backgroundColor: ['#4caf50', '#f44336', '#ffeb3b'], // Added color for Neutral
//         hoverBackgroundColor: ['#66bb6a', '#ef5350', '#fff176'], // Added hover for Neutral
//       },
//     ],
//   };

//   const options = {
//     responsive: true,
//     maintainAspectRatio: false,
//     plugins: {
//       legend: {
//         position: 'bottom',
//       },
//     },
//   };

//   return (
//     <div className="p-8 min-h-screen bg-gray-900 text-white">
//       <h1 className="text-3xl font-bold mb-4">Review Sentiment Analysis</h1>
//       <input
//         type="text"
//         value={url}
//         onChange={(e) => setUrl(e.target.value)}
//         placeholder="Enter Product URL (Amazon, Flipkart, etc.)"
//         className="border p-2 w-full mb-4 text-black"
//       />
//       <button
//         onClick={handleAnalyze}
//         className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
//       >
//         Analyze Reviews
//       </button>

//       {error && <p className="text-red-500 mt-4">{error}</p>}

//       {sentimentData && (
//         <div className="mt-8">
//           <h2 className="text-xl font-semibold mb-4">Sentiment Analysis Result</h2>
//           <p>Total Reviews: {sentimentData.total_reviews}</p>
//           <p>Processing Time: {sentimentData.processing_time} seconds</p>
//           <div className="w-full md:w-1/2 h-[400px]">
//             <Pie data={chartData} options={options} />
//           </div>
//         </div>
//       )}
//     </div>
//   );
// };

// export default App;
import React, { useState } from 'react';
import axios from 'axios';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const App = () => {
  const [url, setUrl] = useState('');
  const [sentimentData, setSentimentData] = useState(null);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    setError('');
    setSentimentData(null);
    try {
      const response = await axios.post('http://127.0.0.1:5001/predict', { url }, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const sentimentCounts = response.data.sentiment_counts;
      if (sentimentCounts && sentimentCounts.Positive !== undefined && sentimentCounts.Negative !== undefined) {
        setSentimentData(response.data);
      } else {
        throw new Error('Invalid response format from backend');
      }
    } catch (err) {
      console.error('Error details:', err);
      setError('Error fetching or analyzing reviews. Please check the URL or try again later.');
    }
  };

  const chartData = sentimentData && {
    labels: ['Positive', 'Negative', 'Neutral'],
    datasets: [
      {
        data: [
          sentimentData.sentiment_counts.Positive,
          sentimentData.sentiment_counts.Negative,
          sentimentData.sentiment_counts.Neutral,
        ],
        backgroundColor: ['#4caf50', '#f44336', '#ffeb3b'],
        hoverBackgroundColor: ['#66bb6a', '#ef5350', '#fff176'],
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#ffffff', // White text for legend
        },
      },
    },
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 flex items-center justify-center p-6">
      <div className="max-w-2xl w-full bg-gray-800 rounded-lg shadow-xl p-8">
        {/* Header */}
        <h1 className="text-3xl font-bold text-white text-center mb-6">
          Review Sentiment Analyzer
        </h1>

        {/* Input and Button */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter Product URL (Amazon, Flipkart, etc.)"
            className="flex-1 p-3 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-400"
          />
          <button
            onClick={handleAnalyze}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 font-semibold"
          >
            Analyze
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <p className="text-red-400 text-center mb-6 bg-red-900/20 p-3 rounded-lg">
            {error}
          </p>
        )}

        {/* Sentiment Results */}
        {sentimentData && (
          <div className="mt-6">
            <h2 className="text-xl font-semibold text-white mb-4 text-center">
              Sentiment Analysis Results
            </h2>
            <div className="flex flex-col items-center gap-4">
              <p className="text-gray-300">
                Total Reviews: <span className="font-bold text-white">{sentimentData.total_reviews}</span>
              </p>
              <p className="text-gray-300">
                Processing Time: <span className="font-bold text-white">{sentimentData.processing_time}</span> seconds
              </p>
              <div className="w-full max-w-md h-80">
                <Pie data={chartData} options={options} />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;