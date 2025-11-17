import React, { useState } from 'react';
import axios from 'axios';
import './PrdOrder.css';
import './Batch';
import { useNavigate } from 'react-router-dom';

const PrdOrder = () => {
  const [loading, setLoading] = useState(false);
  const [orderNumber, setOrderNumber] = useState('');
  const [shift, setShift] = useState('');
  const [quantity, setQuantity] = useState('');
  const [operationType, setOperationType] = useState('A');
  const [operation, setOperation] = useState('');
  const [response, setResponse] = useState(null);
  const [error, setError] = useState('');
  const [availableOperations, setAvailableOperations] = useState([]);
  const [material, setMaterial] = useState([]);
  const [status, setStatus] = useState(false);
  const isDisabled = availableOperations.length === 0 && operationType === 'A';

  const navigate = useNavigate();

  // Automatic Operation
  const handleAutoSelect = () => {
    setOperationType('A');
    setAvailableOperations([]);
    setOperation('');
    setMaterial([]);
    setResponse(null);
    setError('');
  };

  // Manual Operation
  const handleManualSelect = () => {
    setResponse(null);
    setError('');
    setOperationType('B');
    setAvailableOperations([]);
    setOperation('');
    setMaterial([]);
    let cancel = false;
    if (orderNumber.length === 12){
      setLoading(true);
    setStatus(true);
    axios.post('http://localhost:5001/getOperations', { order_number: orderNumber })
    .then((res) => {
            if (cancel) return;
            const ops = Array.isArray(res.data.operations) ? res.data.operations : [];
            setAvailableOperations(ops);
          })
          .catch((err) => { setError(err.message)} )
          .finally(() => {
            if (!cancel) {
              setLoading(false);
              setStatus(false);
            }
          });
    }
    return () => { cancel = true };

  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setStatus(true);
    setResponse(null);
    setError('');
    setMaterial([])
    try {
      // Prepare payload
      const payload = {
        order_number: orderNumber,
        shift,
        quantity,
        operation_type: operationType,
        ...(operationType === 'B' && { operation }),
      };
  
      // Send to backend
      const res = await axios.post('http://localhost:5001/process', payload);
  
      // Safely access fields
      const msgData = res.data?.message || {};
      const status = res.data?.status || msgData.status || '';
  
      // Extract data safely with fallbacks
      const displayMsg =
        status === 'success' ? res.data?.msg  :
        msgData.msg
      const orderNum =
        msgData.order_number || res.data?.order_number || orderNumber;
      const opNum =
        msgData.operation || res.data?.operation || operation;
  
      // Handle available operations
      if (operationType === 'B' && res.data?.operations) {
        setAvailableOperations(res.data.operations);
      } else {
        setAvailableOperations([]);
      }
  
      // Show final output to user
      setResponse(`${displayMsg} ${orderNum} with operation ${opNum}`);
      setMaterial(res.data.message.material)
      console.log(res.data)
    } catch (error) {
      console.log('Error:', error);
      setError('Something went wrong while processing the request.');
    } finally {
      // Always reset loaders
      setLoading(false);
      setStatus(false);
    }
  };
  
  const btchDtr = (e) => {
    e.preventDefault();
    navigate('/Batch');
  };


  return (
    <div className='container-prd'>
      <div className='form-container'>
      <div className='heading-container'>
        <h2 className='main-heading'>Punch In Material</h2>
        <p className='sub-heading'>Enter Order Details below to complete the process</p>
      </div>

      <p className='breaker'></p>

      <div>
        <form className='details-container' onSubmit={handleSubmit}>
          <div className='order-container'>
            <label htmlFor="ordernumber" className='ordernumber-label'>Order Number</label>
            <input
              type="text"
              name="ordernumber"
              className="ordernumber"
              placeholder='►  e.g, 100000000024'
              value={orderNumber}
              onChange={(e) => setOrderNumber(e.target.value)}
              minLength={12}
              maxLength={12}
              required
            />
          </div>

          <div className='shift-container'>
            <label htmlFor="shift" className='shift-label'>Shift</label>
            <select
              className='select-shift'
              value={shift}
              onChange={(e) => setShift(e.target.value)}
              required
            >
              <option value="">Select Shift</option>
              <option value="A">Shift A</option>
              <option value="B">Shift B</option>
              <option value="C">Shift C</option>
              <option value="G">Shift G</option>
            </select>
          </div>

          <div className='quantity-container'>
            <label htmlFor="quantity" className='quantity-label'>Quantity</label>
            <input
              type="text"
              name="quantity"
              className='quantity'
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              required
            />
          </div>

          <div className='checkbox-container'>
            <label htmlFor='auto-check'>Automatic</label>
            <input
              type="radio"
              name="checkType"
              className='checkbox-input'
              checked={operationType === 'A'}
              onChange={handleAutoSelect}
            />
          </div>
            <div className='operation-container'>
              <label htmlFor="operation" className={`${availableOperations.length === 0 ? 'A' : '' }`}>Select Operation</label>
              <select
                className={`operation-select ${availableOperations.length === 0 ? 'A' : '' }`}
                value={operation}
                onChange={(e) => setOperation(e.target.value)}
                disabled={isDisabled}
                required
              >
                <option value='' >{isDisabled ? 'Automatic Operation' : '------ Operation ------'}</option>
                {availableOperations.map((op) => (
                  <option key={op} value={op}>{op}</option>
                ))}
              </select>
            </div>
        </form>
      </div>

      <p className='breaker'></p>

      <div className='footer-container'>
        <button type="button" className={`nxtPage ${loading ? 'processing' : ''}`} onClick={btchDtr} disabled={status || loading}>Material Reservation</button>
        <button type="button" className={`manualEntry ${loading ? 'clickedMan' : ''}`} onClick={handleManualSelect} disabled={loading || status}>Manual Entry</button>
        <button type="submit" className={`submitBtn ${loading ? 'clickedSub' : ''}`} onClick={handleSubmit} disabled={loading || status}>{loading ? (<span className='loader'><span>.</span><span>.</span><span>.</span></span>) : (<span>Submit</span>)}</button>
      </div>
      <div className='response-container'>
      <span className={`${response?.includes('not') ? 'error' : 'success'}`}>{response ? response : ''}</span>
      <span className="error">{error ? JSON.stringify(error) : ''}</span>
      </div>
      
    </div>
    {material && material.length > 0 && (
        <div className='material-container'>
          <table>
            <thead>
              <tr>
                <th>Sr no.</th>
                <th>Material</th>
              </tr>
            </thead>
            <tbody>
              {material.map((mat,idx) => (
                <tr key={idx}>
                  <td>{idx + 1}</td>
                  <td>{mat}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
  </div>
  );
};

export default PrdOrder;
