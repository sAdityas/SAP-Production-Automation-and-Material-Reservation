import { useState } from 'react'
import './Batch.css'
import axios from 'axios'



const Batch = () => {
    const [loading, setLoading] = useState(false)
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
                setLoading(false)
            }else{
                alert("Please Select a file")
                setFile('')
                setLoading(false)
            }

        }catch(err){
            setError(err.response?.data?.error)
        }

    }



    const handleSubmit = async (e) => {
        e.preventDefault();
        setResponse(null);
        setError('');
        setLoading(true)

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
            setLoading(false)
            // Only reload if user presses Enter after successful upload
            const handleKeyDown = (event) => {
                if (event.key === 'Enter') {
                    window.location.reload();
                }
            };
            window.addEventListener('keydown', handleKeyDown, { once: true });
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.error || 'Upload failed.');
            setLoading(false)
        }finally{
            setLoading(false)
        }
};
    return (
        <div className='container-btch'>
            <div className='container-form'>
            <div className='title-container'><h1 className='title'>Material Reservation</h1><p className='breaker'></p></div>

            <div className='file-container'>
                <div className='fileSelect'>
                <h2 className='title-csv'>Select a CSV file</h2>
                <input className="csv-input" type='file' accept='.csv' onChange={handleChange} disabled={loading}/>
                </div>
                <div className='button-container'>
                <button type='submit' className={`submit ${loading ? 'submitted' : ''}`} onClick={handleSubmit} disabled={loading}>
                {loading ? 
                (
                <span className='loader'>
                    <span>.</span>
                    <span>.</span>
                    <span>.</span>
                </span>
                ):
                (
                    <span>Submit</span>
                )}

                </button>
                <button className={`back-btn ${loading ? 'loading' : ''}`} onClick={() => window.location.href = '/'} disabled={loading}>Punch In</button>
                </div>
                
            <p className='breaker'></p>
            </div>
                <div className='res-container'>
                    <span className={`success ${response ? '' : 'noDis' }`}>{response}</span>
                    <span className={`error ${error ? '' : 'noDis'}`}>{error}</span>
                </div>
                    
            </div>
        </div>
    )
}

export default Batch 
 
