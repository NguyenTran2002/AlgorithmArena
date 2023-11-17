import React from 'react';
import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import { useCookies } from 'react-cookie';

function Result() {

    // Temporary URL
    const eval_url = 'http://localhost:1111'
    const database_url = 'http://127.0.0.1:7432'

    const location = useLocation();

    // Access the state variables from the location object
    const { state } = location;
    const { problem, user_code } = state || {};
    const [result, setResult] = useState();
    const [success, setSuccess] = useState();
    const [cookies, setCookie] = useCookies(['user'])

    useEffect(() => {
    
        async function fetchResult() {
          try {
            const post_data = {
              'user_code': user_code,
              'problem': problem,

            };
            // post request with data
            const response = await axios.post(eval_url, post_data); // Replace with your API endpoint
            //console.log(response)
            const result = response.data['result']
            const success = response.data['success']
            // const response_data = 'TRUE'
            setResult(result);
            setSuccess(success);
            if (success == true){
              const post_data = {
                'username': cookies.username,
                'newly_solved_problem': problem,
              }

              const response = await axios.post(database_url + '/update_leaderboard', post_data)

              const result = response.data['update_leaderboard_result']

              if (result != "Success"){
                console.log("Error: Issue updating leaderboard")
              }
            }

              
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