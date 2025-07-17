import { useState } from 'react'
import './App.css'
import axios from 'axios'



const Batch = () => {
    const [error,setError] = useState('')
    const [response, setResponse] = useState(null);
    const [file, setFile] = useState(null)


    const handleChange = async(e) =>{
        e.preventDefault()
        setError('')
        setResponse('')
        try{
            const selectedFile = e.target.files[0];
            if(selectedFile && selectedFile.name.endsWith('.csv')){
                setFile(selectedFile)
            }else{
                alert("Please Select a file")
                setFile('')
            }

        }catch(err){
            setError(err.response?.data?.error)
        }
    }



    const handleSubmit = async (e) => {
        e.preventDefault();
        setResponse(null);
        setError('');

        try {
            if (!file) {
            setError("Please select a CSV file before submitting.");
            return;
            }

            const formData = new FormData();
            formData.append("file", file);       // CSV file

            const res = await axios.post('http://localhost:5001/btchdtr', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            }
            });

            setResponse(res.data.message || 'Upload and processing successful!');
            console.log('Response:', res.data);
            // Only reload if user presses Enter after successful upload
            const handleKeyDown = (event) => {
                if (event.key === 'Enter') {
                    window.location.reload();
                }
            };
            window.addEventListener('keydown', handleKeyDown, { once: true });
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.error || 'Upload failed.');;
        }
};
    return (
        <div className='container'>
            <h1 className='title'>Automatic Reservation</h1>
            <div>
                <h2 className='title-csv'>Select a CSV file</h2>
                <input className="csv-input" type='file' accept='.csv' onChange={handleChange}/>
                {file && file.name ? <p className='title-res'>Selected File: {file.name}</p> : null}
                <button type='submit' className='manual-btn' onClick={handleSubmit}>Submit</button>
            </div>

                {response && <div className="success">{response}</div>}
                {error && <div className="error">{error}</div>}
                <div>
                    <button className="back-btn" onClick={() => window.location.href = '/'}>Back</button>
                </div>
        </div>
    )
}

export default Batch