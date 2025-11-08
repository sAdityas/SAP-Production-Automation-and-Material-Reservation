import React from 'react'
import { Route, Routes } from 'react-router-dom'
import PrdOrder from './PrdOrder copy'
import Batch from './Batch'

const App = () => {
  return (
    <Routes>
      <Route path='/' element={<PrdOrder />}></Route>
      <Route path='/batch' element={<Batch />}></Route>
    </Routes>
  )
}

export default App
 
 
