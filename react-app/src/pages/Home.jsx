import React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import Button from '@mui/material/Button';
import { styled } from "@mui/material/styles";
import { Link } from 'react-router-dom';

function Home() {
  const [problems, setProblems] = useState([]);
  // const [selectedProblem, setSelectedProblem] = useState('');

  // Temporary URL
  const database_url = 'http://localhost:7432'

  useEffect(() => {
    // Fetch all available problems from the server when the component mounts
    async function fetchProblems() {
      try {
        const response = await axios.post(database_url + '/get_all_problems'); // Replace with your API endpoint
        const problems = response.data["problems"];
        // const problems = ['binary_search', 'koko_eating_bananas', 'contains_duplicates']
        console.log("problems", problems)
        setProblems(problems);
      } catch (error) {
        console.error(`Error while retrieving problems: ${error.message}`);
      }
    }
    fetchProblems();
  }, []);

  const getName = (problem) => {

    const words = problem.split('_');
    const capitalizedWords = words.map((word) => {
      return word.charAt(0).toUpperCase() + word.slice(1);
    });
    const result = capitalizedWords.join(' ');
  
    return result;
  };

  const StyledButton = styled(Button)({
    color: 'black',
    padding: '10px 20px',
    borderRadius: '10px',
    cursor: 'pointer',
    fontSize: '20px',
    backgroundColor: '#FFF8DC',
    margin: '1em',
    borderColor: 'black',
  });

  const StyledH1 = styled('h1')({
    fontSize: '56px',
    fontWeight: '30px',

  });

  const StyledH3 = styled('h3')({
    fontSize: '24px',

  });

  // const StyledButtonGroup = styled(ButtonGroup)({
  //   backgroundColor: 'lightblue',
  // });

  return (
    <div>
      <StyledH1 >Welcome to Algorithm Arena!</StyledH1>
      <StyledH3>Select a problem to get started</StyledH3>
      <div>
        {problems.map((problem, index) => (
            <StyledButton key={index} component={Link} to={`/solve/${problem}`}>{getName(problem)}</StyledButton>
        ))}
      </div>
      <div></div>
      {/* <ButtonGroup variant="soft" aria-label="text button group">
        {problems.map((problem, index) => (
          <StyledButton key={index}>{getName(problem)}</StyledButton>
        ))}

      </ButtonGroup> */}
    </div>
  );
}


export default Home;
