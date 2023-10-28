import React from 'react';
import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';

function Result() {

    // Temporary URL
    const eval_url = 'http://localhost:1111'

    const location = useLocation();

    // Access the state variables from the location object
    const { state } = location;
    const { user_problem, user_answer } = state || {};
    const [result, setResult] = useState();
    const [success, setSuccess] = useState();

    useEffect(() => {
    
        async function fetchResult() {
          try {
            const post_data = {
              user_code: user_answer,
              problem: user_problem,

            };

            const response = await axios.post(eval_url, post_data); // Replace with your API endpoint
            //console.log(response)
            const result = response.data['result']
            const success = response.data['success']
            // const response_data = 'TRUE'
            setResult(result);
            setSuccess(success);
            // console.log(result)
            // console.log(success)
          } catch (error) {
            console.error(`Error while retrieving problems: ${error.message}`);
          }
        }
    
        fetchResult();
      }, []);
    
    return (

        <div>
            <h1 className='h1'>Your result:</h1>
            <h3>{result}</h3>
            <p>{success ? 'SUCCESS' : 'FALSE'}</p>
        </div>
    );
}

export default Result;