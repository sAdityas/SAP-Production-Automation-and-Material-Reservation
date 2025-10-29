import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css'; // Make sure this file exists
import './Batch'
import { useNavigate } from 'react-router-dom';

const PrdOrder = () => {
  const [orderNumber, setOrderNumber] = useState('');
  const [shift, setShift] = useState('');
  const [quantity, setQuantity] = useState('');
  const [operationType, setOperationType] = useState('A');
  const [operation, setOperation] = useState('');
  const [response, setResponse] = useState(null);
  const [error, setError] = useState('');
  const [availableOperations, setAvailableOperations] = useState([]);
  const [material, setMaterial] = useState([])
  const navigate = useNavigate();

  // Function to handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setResponse(null);
    setError('');

    try{
      const payload = {
        order_number: orderNumber,
        shift,
        quantity,
        operation_type: operationType,
        ...(operationType === 'B' && { operation }),
      };


      const res = await axios.post('http://localhost:5001/process', payload);
      console.log('Response:', res.data);
      if (operationType === 'B' && res.data.operations) {
        setAvailableOperations(res.data.operations);
        console.log(payload)
      }
      else {
        setAvailableOperations([]);
      }
      setResponse(res.data.message.status +' for order number ' + res.data.order_number);
      setMaterial(res.data.message.material)

      // setTimeout(() => {
      //   window.location.reload();
      // },3000);
    } catch (err) {
      setError(err.response?.data?.error);
    }
  };
  useEffect(() => {
  if (operationType === 'B' && orderNumber.trim() !== '') {
    axios.post('http://localhost:5001/getOperations', { order_number: orderNumber })
      .then(res => {
        const ops = Array.isArray(res.data.operations) ? res.data.operations : [];
        console.log('Operation Response:', res.data);

        setAvailableOperations(ops);
        setOperation('');
      })
      .catch(err => {
        setAvailableOperations([]);
        setError(err.response?.data?.error);
      });
  } else {
    setAvailableOperations([]);
    setOperation('');
  }
}, [operationType, orderNumber]);


const btchDtr = (e) => {
  e.preventDefault();
  setError('');
  try {
    navigate('/Batch');
  } catch (err) {
    setError('Failed to redirect.');
  }
};

  return (
    <div className="container">
      <h1 className="title">SAP CO11N Processor</h1>
      <form className="form" onSubmit={handleSubmit}>
        <input
          className='inpt'
          minLength={12}
          maxLength={12}
          type="text"
          placeholder="Production Order Number"
          value={orderNumber}
          onChange={(e) => setOrderNumber(e.target.value)}
          required
        />
        <select value={shift} onChange={(e) => setShift(e.target.value)} required>
          <option value="">Select Shift</option>
          <option value="A">Shift A</option>
          <option value="B">Shift B</option>
          <option value="C">Shift C</option>
          <option value="G">Shift G</option>
        </select>
        <input
          className='inpt'
          type="text"
          placeholder="Quantity"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
          required
        />
        <div className="radio-group">
          <label>

            <input
              className='radio-btn'
              type="radio"
              value="A"
              checked={operationType === 'A'}
              onChange={() => setOperationType('A')}
            /> Automatic
          </label>
          <label>
            <button
              className='manual-btn'
              type="submit"
              value="B"
              checked={operationType === 'B' && orderNumber.length === 12}
              onClick={() => setOperationType('B')}
            > Manual</button>
          </label>
        </div>
       {operationType === 'B' && availableOperations.length > 0 && (
        <select
          className="select"
          value={operation}
          onChange={(e) => setOperation(e.target.value)}
          required
        >
          <option value="">-- Select Operation --</option>
          {availableOperations.map((op) => (
            <option key={op} value={op}>
              {op}
            </option>
          ))}
        </select>
      )}

        <button className='auto-btn' type="submit">Submit</button>
      </form>

      {response && <div className="success">{response}</div>}
      {
        material ? (
          material.map((mats,idx) => (
            <div key={idx}>
              <h3>Material With No Batch :</h3>
              <p><span>{idx +1+"."} {" "}</span>{mats}</p>  
            </div>
          ))
        ) : null
      }
      {error && <div className="error">{error}</div>}
      <div>
        <button className='route-btn' type='submit' onClick={btchDtr}>Material Reservation</button>
      </div>
    </div>
  );
};

export default PrdOrder;
 
 
