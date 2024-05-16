// Main page used for displaying the landing page of the webapp.
import { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function Home() {
  // State variables for storing data, pagination info, and totals
  const [sponsorsData, setSponsorsData] = useState([]);
  const [conditionsData, setConditionsData] = useState([]);
  const [sponsorsPage, setSponsorsPage] = useState(1);
  const [conditionsPage, setConditionsPage] = useState(1);
  const [sponsorsTotal, setSponsorsTotal] = useState(0);
  const [conditionsTotal, setConditionsTotal] = useState(0);
  const limit = 10;

  // Fetch sponsors data whenever sponsorsPage changes
  useEffect(() => {
    async function fetchSponsorsData() {
      const response = await fetch(`/api/sponsors?page=${sponsorsPage}&limit=${limit}`);
      const data = await response.json();
      console.log('Sponsors Data:', data);
      setSponsorsData(data.data);
      setSponsorsTotal(data.total);
    }
    fetchSponsorsData();
  }, [sponsorsPage]);

  // Fetch conditions data whenever conditionsPage changes
  useEffect(() => {
    async function fetchConditionsData() {
      const response = await fetch(`/api/conditions?page=${conditionsPage}&limit=${limit}`);
      const data = await response.json();
      console.log('Conditions Data:', data);
      setConditionsData(data.data);
      setConditionsTotal(data.total);
    }
    fetchConditionsData();
  }, [conditionsPage]);

  // Chart data for sponsors
  const sponsorsChartData = {
    labels: sponsorsData.map((item) => item.sponsor_name),
    datasets: [
      {
        label: 'Number of Trials',
        data: sponsorsData.map((item) => item.trial_count),
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  // Chart data for conditions
  const conditionsChartData = {
    labels: conditionsData.map((item) => item.medical_condition),
    datasets: [
      {
        label: 'Number of Trials',
        data: conditionsData.map((item) => item.trial_count),
        backgroundColor: 'rgba(153, 102, 255, 0.2)',
        borderColor: 'rgba(153, 102, 255, 1)',
        borderWidth: 1,
      },
    ],
  };

  // Chart options
  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Combined Clinical Trials Data',
      },
    },
    scales: {
      x: {
        ticks: {
          autoSkip: false,
          maxRotation: 90,
          minRotation: 90,
        },
      },
    },
  };

  return (
    <div className="min-h-screen text-white">
      <div className="container mx-auto py-10">
        <h1 className="text-4xl font-bold text-center mb-10">Combined Clinical Trials Data (US and EU)</h1>

        {/* Section for displaying trials by sponsor */}
        <section className="mb-10">
          <h2 className="text-2xl font-semibold mb-5">Trials by Sponsor</h2>
          <div className="p-5 rounded-lg shadow-lg">
            <Bar data={sponsorsChartData} options={options} />
          </div>
          <div className="flex justify-between mt-5">
            <button 
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50" 
              disabled={sponsorsPage <= 1} 
              onClick={() => setSponsorsPage(sponsorsPage - 1)}>
              Previous
            </button>
            <button 
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50" 
              disabled={sponsorsPage * limit >= sponsorsTotal} 
              onClick={() => setSponsorsPage(sponsorsPage + 1)}>
              Next
            </button>
          </div>
          <br></br>
          <hr></hr>
        </section>

        <br></br>
        <br></br>

        {/* Section for displaying trials by condition */}
        <section>
          <h2 className="text-2xl font-semibold mb-5">Trials by Condition</h2>
          <div className="p-5 rounded-lg shadow-lg">
            <Bar data={conditionsChartData} options={options} />
          </div>
          <div className="flex justify-between mt-5">
            <button 
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50" 
              disabled={conditionsPage <= 1} 
              onClick={() => setConditionsPage(conditionsPage - 1)}>
              Previous
            </button>
            <button 
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50" 
              disabled={conditionsPage * limit >= conditionsTotal} 
              onClick={() => setConditionsPage(conditionsPage + 1)}>
              Next
            </button>
          </div>
        </section>
      </div>
    </div>
  );
}
