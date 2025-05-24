import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [form, setForm] = useState({
    age: '',
    location: 'Urban',
    income: '',
    interaction_count: '',
    interest_score: ''
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    const payload = {
      age: Number(form.age),
      location: form.location,
      income: Number(form.income),
      interaction_count: Number(form.interaction_count),
      interest_score: parseFloat(form.interest_score)
    };

    console.log("Sending payload:", payload);

    try {
      const response = await axios.post('http://127.0.0.1:5000/predict', payload);
      setResult(response.data);
    } catch (error) {
      console.error("Prediction error:", error.response?.data || error.message);
      alert('Prediction failed. Please check inputs or try again later.');
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h1>💡 FinArva Lead Scoring System</h1>
      <p className="subtitle">Predict how likely your lead is to convert in seconds 🚀</p>

      <form className="form" onSubmit={handleSubmit}>
        <input
          type="number"
          name="age"
          placeholder="Age"
          value={form.age}
          onChange={handleChange}
          required
        />

        <select name="location" value={form.location} onChange={handleChange} required>
          <option value="Urban">Urban</option>
          <option value="Rural">Rural</option>
          <option value="Suburban">Suburban</option>
        </select>

        <input
          type="number"
          name="income"
          placeholder="Monthly Income"
          value={form.income}
          onChange={handleChange}
          required
        />

        <input
          type="number"
          name="interaction_count"
          placeholder="Interaction Count"
          value={form.interaction_count}
          onChange={handleChange}
          required
        />

        <input
          type="number"
          step="0.01"
          name="interest_score"
          placeholder="Interest Score (0 to 1)"
          value={form.interest_score}
          onChange={handleChange}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? 'Predicting...' : 'Predict Lead Score'}
        </button>
      </form>

      {result && (
        <div className="result">
          <h3>🧠 Prediction Result</h3>
          <p><strong>Will Convert?</strong> {result.converted_prediction === 1 ? '✅ Yes' : '❌ No'}</p>
          <p><strong>Conversion Probability:</strong> {(result.conversion_probability * 100).toFixed(2)}%</p>
        </div>
      )}
    </div>
  );
}

export default App;
