import React, { useState, useEffect } from "react";
import { Link } from 'react-router-dom';
import Button from '@mui/material/Button';
import { styled } from "@mui/material/styles";
import axios from 'axios';


function Leaderboard() {
    const [leaderboard, setLeaderboard] = useState([]);
    const database_url = 'http://localhost:7432'

    useEffect(() => {
        // Fetch all available problems from the server when the component mounts

        async function fetchLeaderboard() {
          try {
            const post_data = {
                user_number : 10
            }

            const response = await axios.post(database_url + '/get_top_users', post_data); // Replace with your API endpoint
            console.log(response);
            const data = response.data["get_top_users_result"];
            console.log("leaderboard 2d array: ", data)
            setLeaderboard(data);
          } catch (error) {
            console.error(`Error while retrieving problems: ${error.message}`);
          }
        }
        fetchLeaderboard();

        // const data = [['John', 10], ['Nguyen', 20], ['Kristo', 30], ['Albert', 40], ['Geoff', 50], ['Matt', 60]];
        // setLeaderboard(data);
      }, []);

      const StyledButton = styled(Button)({
        position: 'fixed',
        color: 'black',
        padding: '10px 20px',
        borderRadius: '10px',
        cursor: 'pointer',
        fontSize: '20px',
        backgroundColor: '#FFF8DC',
        margin: '1em',
        borderColor: 'black',
        top: '10px',
        left: '10px'
      });

    return (
        <div className="leaderboard">
            <StyledButton component={Link} to={`/`}>Algorithm Arena</StyledButton>
            <div className="title" style={{
                fontSize:"5em"
            }}>Leaderboard</div>
            <table>
                <thead><tr>
                        <th>Username</th>
                        <th>Score</th>
                </tr></thead>
                <tbody>
                {leaderboard.map((row, index) => (
                    <tr key={index}>
                    <td>{row[0]}</td>
                    <td>{row[1]}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    )
}

export default Leaderboard;