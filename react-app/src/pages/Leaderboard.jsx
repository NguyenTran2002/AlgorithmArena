import React, { useState, useEffect } from "react";
import axios from 'axios';


function Leaderboard() {
    const [leaderboard, setLeaderboard] = useState([]);
    const database_url = 'http://localhost:7432'

    useEffect(() => {
        // Fetch all available problems from the server when the component mounts
        async function fetchLeaderboard() {
          try {
            const response = await axios.post(database_url + '/get_all_problems'); // Replace with your API endpoint
            const problems = response.data["problems"];
            // const problems = ['binary_search', 'koko_eating_bananas', 'contains_duplicates']
            console.log("problems", problems)
            setLeaderboard(problems);
          } catch (error) {
            console.error(`Error while retrieving problems: ${error.message}`);
          }
        }
        fetchProblems();
      }, []);

    return (
        <div>
            {leaderboard}
        </div>
    )
}