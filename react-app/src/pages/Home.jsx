import React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import Button from '@mui/material/Button';
import { styled } from "@mui/material/styles";
import { Link } from 'react-router-dom';
import Split from 'react-split';
import { useCookies } from 'react-cookie';
import Login from './login';

function Home() {
  const [easy_problems, setEasyProblems] = useState([]);
  const [medium_problems, setMediumProblems] = useState([]);
  const [hard_problems, setHardProblems] = useState([]);
  const [selectedProblem, setSelectedProblem] = useState('');
  const [cookies, setCookies] = useCookies(['user']);
  const [loginStatus, setLoginStatus] = useState([]);

  console.log(cookies.username)

  // Temporary URL
  const database_url = 'http://127.0.0.1:7432'

  useEffect(() => {
    // Fetch all available problems from the server when the component mounts
    async function fetchProblems() {
      try {
        // post request without data
        const response = await axios.post(database_url + '/get_all_problems'); // Replace with your API endpoint
        const easy_problems = response.data["easy_problems"];
        console.log(easy_problems)
        const medium_problems = response.data["medium_problems"];
        console.log(medium_problems)
        const hard_problems = response.data["hard_problems"];
        console.log(hard_problems)
        setEasyProblems(easy_problems);
        setMediumProblems(medium_problems);
        setHardProblems(hard_problems);
      } catch (error) {
        console.error(`Error while retrieving problems: ${error.message}`);
      }
    }
    fetchProblems();
  }, []);

  useEffect(() => {
    if (cookies.username){
      setLoginStatus(true)
    }
    else {
      setLoginStatus(false)
    }
  }, [cookies.username]);

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

  const LeaderboardButton = styled(StyledButton) ({
    position: "fixed",
    top:"10px", 
    left:"10px", 
    fontSize:"1.4em"
  });

  const StyledH1 = styled('h1')({
    fontSize: '56px',
    fontWeight: '30px',

  });

  const StyledH2 = styled('h2')({
    fontSize: '30px',

  });

  const StyledH3 = styled('h3')({
    fontSize: '26px',

  });
  

  const SettingsButton = styled(StyledButton) ({
    position: "fixed",
    top:"10px", 
    right:'10px', 
    fontSize:"1.4em"
  });

  const LoginButton = styled(StyledButton) ({
    position: "fixed",
    top:"10px", 
    right:'10px', 
    fontSize:"1.4em"
  });

  // const StyledButtonGroup = styled(ButtonGroup)({
  //   backgroundColor: 'lightblue',
  // });

  return (
    <div>
      <StyledH1 >Welcome to Algorithm Arena!</StyledH1>
      <StyledH2>Select a problem to get started</StyledH2>
      <div>
        {
          loginStatus ? 
            <SettingsButton component={Link} to={'/settings'}>Settings</SettingsButton>
            :
            <LoginButton component={Link} to={'/login'}>Login</LoginButton>
        }
      </div>
      <LeaderboardButton component={Link} to={`/leaderboard`}>Leaderboard</LeaderboardButton>
      {/* <SettingsButton component={Link} to={'/settings'}>Settings</SettingsButton> */}
      <Split
          sizes={[33, 33,33]} // Initial sizes of the panes in percentages
          minSize={100} // Minimum size for a pane
          expandToMin={false} // Whether to expand to the minimum size when resizing
          gutterSize={50} // Size of the dividers (gutters)
          direction='horizontal'
          mode='horizontal'
          className='solve-container'
        >
        <div>
          <StyledH3>Easy</StyledH3>
          <div>
            {easy_problems.map((easy_problem, index) => (
                <StyledButton key={index} component={Link} to={`/solve/${easy_problem}`}>{getName(easy_problem)}</StyledButton>
            ))}
          </div>
        </div>
        <div>
          <StyledH3>Medium</StyledH3>
          <div>
            {medium_problems.map((medium_problem, index) => (
                <StyledButton key={index} component={Link} to={`/solve/${medium_problem}`}>{getName(medium_problem)}</StyledButton>
            ))}
          </div>
        </div>
        <div>
          <StyledH3>Hard</StyledH3>
          <div>
            {hard_problems.map((hard_problem, index) => (
                <StyledButton key={index} component={Link} to={`/solve/${hard_problem}`}>{getName(hard_problem)}</StyledButton>
            ))}
          </div>
        </div>

      </Split>
    </div>
  );
}


export default Home;
